# Cloudflare Agent Readiness 實戰實作指引 (Implementation Guide)

本指引涵蓋不同技術架構（Astro + Cloudflare Pages、Next.js 16 App Router、純靜態站）如何將 Level 5 Agent-Native 模式一次到位落地。

---

## 1. Astro 6 + Cloudflare Pages 實作架構 (如 StarChase 官網)

### (1) Edge 中間件 (`functions/[[route]].ts`)
攔截所有請求，處理 Markdown 內容協商、注入 RFC 8288 Link 標頭與處理靜態 extensionless 端點：

```ts
import { wantsMarkdown } from '../src/lib/accept-negotiation';

interface PagesFunctionContext {
  readonly request: Request;
  readonly next: (input?: Request | string, init?: RequestInit) => Promise<Response>;
  readonly env: {
    readonly ASSETS?: { fetch: (input: Request | URL) => Promise<Response> };
    readonly [key: string]: unknown;
  };
}

const MD_VARY = 'Accept, Accept-Encoding, User-Agent';

function slugFor(pathname: string): string {
  const clean = pathname.replace(/\/+$/, '');
  if (clean === '' || clean === '/index' || clean === '/index.md' || clean === '/home' || clean === '/home.md') {
    return '/home.md';
  }
  if (clean.endsWith('.md')) return clean;
  return `${clean}.md`;
}

async function fetchAsset(context: PagesFunctionContext, path: string): Promise<Response | null> {
  const url = new URL(path, context.request.url);
  const res = await context.env.ASSETS?.fetch(url);
  return res && res.status === 200 ? res : null;
}

function mdHeaders(bodyLength: number, cacheControl: string, origin: string, twinPath: string): HeadersInit {
  return {
    'Content-Type': 'text/markdown; charset=utf-8',
    Vary: MD_VARY,
    'Cache-Control': cacheControl,
    'X-Markdown-Tokens': String(Math.ceil(bodyLength / 4)),
    'X-Robots-Tag': 'noindex, nofollow',
    Link: `<${origin}${twinPath}>; rel="alternate"; type="text/markdown"`,
  };
}

function buildHtmlLinkHeader(origin: string, pathname: string): string {
  const clean = pathname.replace(/\/+$/, '');
  const twin = (clean === '' || clean === '/index' ? '/index' : clean) + '.md';
  return [
    `<${origin}${twin}>; rel="alternate"; type="text/markdown"`,
    `<${origin}/.well-known/api-catalog>; rel="api-catalog"`,
    `<${origin}/llms.txt>; rel="service-doc"`,
    `<${origin}/.well-known/ai-catalog.json>; rel="ai-catalog"`,
    `<${origin}/.well-known/mcp/server-card.json>; rel="service-desc"`,
  ].join(', ');
}

export const onRequest = async (context: PagesFunctionContext): Promise<Response> => {
  const { request } = context;
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    return context.next();
  }

  const url = new URL(request.url);
  const pathname = url.pathname;

  if (pathname.startsWith('/assets/') || pathname.startsWith('/_astro/')) {
    return context.next();
  }

  // 1. API Health
  if (pathname === '/api/health') {
    return new Response(JSON.stringify({ status: 'ok', service: 'official', timestamp: new Date().toISOString() }), {
      status: 200,
      headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-cache' },
    });
  }

  // 2. RFC 9727 API Catalog
  if (pathname === '/.well-known/api-catalog') {
    const catalog = await fetchAsset(context, '/.well-known/api-catalog.json');
    if (catalog) {
      const text = await catalog.text();
      return new Response(text, {
        status: 200,
        headers: { 'Content-Type': 'application/linkset+json; charset=utf-8', 'Cache-Control': 'public, max-age=3600', Vary: 'Accept' },
      });
    }
  }

  // 3. Web Bot Auth JWKS
  if (pathname === '/.well-known/http-message-signatures-directory') {
    const jwks = await fetchAsset(context, '/.well-known/jwks.json');
    if (jwks) {
      return new Response(jwks.body, { status: 200, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'public, max-age=86400' } });
    }
  }

  // 4. OAuth PRM (RFC 9728) & OAuth Auth Server
  if (pathname === '/.well-known/oauth-protected-resource') {
    const prm = await fetchAsset(context, '/.well-known/oauth-protected-resource.json');
    if (prm) return new Response(prm.body, { status: 200, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'public, max-age=86400' } });
  }

  if (pathname === '/.well-known/oauth-authorization-server' || pathname === '/.well-known/openid-configuration') {
    const file = await fetchAsset(context, pathname);
    if (file) return new Response(file.body, { status: 200, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'public, max-age=86400' } });
  }

  // 5. MCP / A2A API Stubs
  if (pathname === '/api/mcp') {
    const card = await fetchAsset(context, '/.well-known/mcp/server-card.json');
    if (card) return new Response(card.body, { status: 200, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'public, max-age=3600' } });
  }
  if (pathname === '/api/a2a') {
    const card = await fetchAsset(context, '/.well-known/agent-card.json');
    if (card) return new Response(card.body, { status: 200, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'public, max-age=3600' } });
  }

  if (pathname.startsWith('/api/')) return context.next();

  const accept = request.headers.get('Accept');
  const isDirectMd = pathname.endsWith('.md');
  const shouldServeMd = isDirectMd || wantsMarkdown(accept);

  // 6. Markdown Twin 內容協商
  if (shouldServeMd) {
    const mdAsset = await fetchAsset(context, `/__md__${slugFor(pathname)}`);
    if (mdAsset) {
      const text = await mdAsset.text();
      const clean = pathname.replace(/\/+$/, '');
      const twinPath = (clean === '' || clean === '/index' ? '/index' : clean) + (clean.endsWith('.md') ? '' : '.md');
      return new Response(text, { status: 200, headers: mdHeaders(text.length, 'public, max-age=0, must-revalidate', url.origin, twinPath) });
    }

    if (!isDirectMd && !/\.[a-z0-9]+$/i.test(pathname)) {
      const tpl = await fetchAsset(context, '/__md__/404.md');
      const body = tpl ? (await tpl.text()).replaceAll('{PATH}', pathname) : `# 404 Not Found\n\n\`${pathname}\` does not exist.\n`;
      return new Response(body, { status: 404, headers: mdHeaders(body.length, 'public, max-age=300', url.origin, '/404.md') });
    }
  }

  // 7. HTML Passthrough 注入 Link 標頭與 Vary
  const res = await context.next();
  const headers = new Headers(res.headers);
  const contentType = headers.get('content-type') || '';
  if (contentType.includes('text/html') || !contentType.includes('/')) {
    headers.set('Link', buildHtmlLinkHeader(url.origin, pathname));
  }
  headers.set('Vary', MD_VARY);
  return new Response(res.body, { status: res.status, headers });
};
```

### (2) Astro Layout 標頭與 WebMCP (`BaseLayout.astro`)
在 HTML `<head>` 區段注入所有機器發現 Link 與 WebMCP 註冊腳本：
```astro
<!-- Search Engine & AI Answer Engine Indexing -->
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
<link rel="alternate" hreflang="zh-TW" href={canonical} />
<link rel="alternate" type="text/markdown" href={`${siteUrl}${pathname === '/' ? '/index' : pathname.replace(/\/$/, '')}.md`} title="Markdown Version" />
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLMs Context" />
<link rel="alternate" type="text/plain" href="/llms-full.txt" title="Full LLMs Context" />
<link rel="api-catalog" type="application/linkset+json" href="/.well-known/api-catalog" title="API Catalog (RFC 9727)" />
<link rel="ai-catalog" type="application/json" href="/.well-known/ai-catalog.json" title="ARD AI Catalog" />
<link rel="service-desc" type="application/json" href="/.well-known/mcp/server-card.json" title="MCP Server Card (SEP-1649)" />
<link rel="service-doc" type="text/plain" href="/llms.txt" title="Service Documentation" />
<meta name="ai-agent-instructions" content="AI agents: request Markdown via Accept: text/markdown or fetch https://www.yourdomain.com/llms.txt" />

<script is:inline>
  if (typeof navigator !== 'undefined' && 'modelContext' in navigator && navigator.modelContext?.registerTool) {
    try {
      navigator.modelContext.registerTool({
        name: 'getBrandInfo',
        description: '獲取品牌公司簡介、五大核心服務與聯絡資訊',
        inputSchema: { type: 'object', properties: {} },
        execute: async () => ({
          company: 'Brand Official',
          website: 'https://www.yourdomain.com',
          services: ['服務A', '服務B', '服務C'],
          llms_txt: 'https://www.yourdomain.com/llms.txt',
          contact: { email: 'info@yourdomain.com', line: 'https://page.line.me/brand' }
        })
      });
    } catch (_) {}
  }
</script>
```

---

## 2. Next.js 16 App Router 實作架構

### (1) `middleware.ts` 內容協商與標頭
```ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const accept = request.headers.get('accept') || '';

  if (
    accept.includes('text/markdown') &&
    !pathname.startsWith('/api') &&
    !pathname.startsWith('/_next') &&
    !pathname.endsWith('.txt') &&
    !pathname.endsWith('.md') &&
    !pathname.endsWith('.xml') &&
    !pathname.endsWith('.json')
  ) {
    const target = pathname === '/' ? '/llms.txt' : `${pathname}.md`;
    const response = NextResponse.rewrite(new URL(target, request.url));
    response.headers.set('Content-Type', 'text/markdown; charset=utf-8');
    response.headers.set('Vary', 'Accept, Accept-Encoding, User-Agent');
    response.headers.set('X-Robots-Tag', 'noindex, nofollow');
    return response;
  }

  const response = NextResponse.next();
  response.headers.set('Vary', 'Accept, Accept-Encoding, User-Agent');
  return response;
}
```

### (2) `next.config.ts` 標頭設定
```ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'Vary', value: 'Accept, Accept-Encoding, User-Agent' },
          {
            key: 'Link',
            value: [
              '</llms.txt>; rel="service-doc"; type="text/plain"',
              '</.well-known/api-catalog>; rel="api-catalog"',
              '</.well-known/ai-catalog.json>; rel="ai-catalog"',
              '</.well-known/mcp/server-card.json>; rel="service-desc"',
            ].join(', '),
          },
        ],
      },
    ];
  },
};

export default nextConfig;
```

---

## 3. 自動化測試套件範本 (`tests/agentic-readiness.test.ts`)

新專案建立後，直接加入此單元測試檔（相容 Bun test / Vitest / Node test），確保 CI/CD 門戶自動驗證：

```ts
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';

const root = process.cwd();

describe('Cloudflare Agent-Readiness Protocols', () => {
  it('API Catalog (RFC 9727) is valid linkset+json', () => {
    const raw = readFileSync(resolve(root, 'public/.well-known/api-catalog'), 'utf8');
    const json = JSON.parse(raw);
    assert.ok(Array.isArray(json.linkset) && json.linkset.length > 0);
  });

  it('MCP Server Card (SEP-1649) has serverInfo and tools', () => {
    const raw = readFileSync(resolve(root, 'public/.well-known/mcp/server-card.json'), 'utf8');
    const json = JSON.parse(raw);
    assert.ok(json.serverInfo?.name);
    assert.ok(Array.isArray(json.tools));
  });

  it('A2A Agent Card is valid per A2A protocol spec', () => {
    const raw = readFileSync(resolve(root, 'public/.well-known/agent-card.json'), 'utf8');
    const json = JSON.parse(raw);
    assert.ok(json.name);
    assert.ok(Array.isArray(json.skills));
  });

  it('Agent Skills index matches schema and file digests', () => {
    const raw = readFileSync(resolve(root, 'public/.well-known/agent-skills/index.json'), 'utf8');
    const json = JSON.parse(raw);
    assert.equal(json.$schema, 'https://schemas.agentskills.io/discovery/0.2.0/schema.json');
    for (const skill of json.skills) {
      const filePath = resolve(root, 'public', skill.url.replace(/^\//, ''));
      assert.ok(existsSync(filePath));
      const content = readFileSync(filePath);
      const hash = 'sha256:' + createHash('sha256').update(content).digest('hex');
      assert.equal(skill.digest, hash);
    }
  });

  it('auth.md and oauth-authorization-server agent_auth are consistent', () => {
    const md = readFileSync(resolve(root, 'public/auth.md'), 'utf8');
    assert.match(md, /^#\s+.*auth\.md/im);
    const authServer = JSON.parse(readFileSync(resolve(root, 'public/.well-known/oauth-authorization-server'), 'utf8'));
    assert.ok(authServer.agent_auth?.claim_uri);
    assert.ok(authServer.agent_auth?.register_uri);
  });

  it('ARD AI Catalog is valid JSON per ARD 1.0 spec', () => {
    const raw = readFileSync(resolve(root, 'public/.well-known/ai-catalog.json'), 'utf8');
    const json = JSON.parse(raw);
    assert.equal(json.specVersion, '1.0');
    assert.ok(Array.isArray(json.entries));
  });
});
```

---

## 4. 上線後終端機驗證指令

```bash
curl -s -X POST https://isitagentready.com/api/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.yourdomain.com"}' | jq '{level, levelName, checks: {discoverability, contentAccessibility, botAccessControl, discovery}}'
```
回傳確認評級為 **`level: 5` (`Agent-Native`)** 即代表全站一次到位。
