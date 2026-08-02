/**
 * MCP 2026-07-28 Stateless Worker Template
 *
 * Template for building an MCP server on Cloudflare Workers.
 * Replace the TOOLS, ENDPOINT_MAP, and tavilyCall function
 * with your own API integration.
 *
 * Endpoints:
 *   POST /mcp    — JSON-RPC 2.0 (tools/list, tools/call)
 *   GET  /health — Health check (no auth)
 */

const TOOLS = [
	{
		name: "example_tool",
		description: "Describe what this tool does.",
		inputSchema: {
			type: "object",
			properties: {
				query: { type: "string" },
				limit: { type: "number", default: 5 },
			},
			required: ["query"],
		},
	},
];

const ENDPOINT_MAP = {
	example_tool: "/api/endpoint",
};

function loadKeys(env) {
	const keys = [];
	for (const v of ["API_KEY", "API_KEY_BACKUP1"]) {
		if (env[v]) keys.push(env[v]);
	}
	return keys;
}

async function apiCall(endpoint, body, keys) {
	let lastError = null;
	for (let i = 0; i < keys.length; i++) {
		body.api_key = keys[i];
		try {
			const resp = await fetch(`https://api.example.com${endpoint}`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify(body),
			});
			if (resp.ok) return await resp.json();
			if (resp.status === 429 || resp.status === 402) {
				lastError = { status: resp.status, keyIndex: i };
				continue;
			}
			throw new Error(`API error ${resp.status}`);
		} catch (err) {
			if (err.message?.startsWith("API error")) throw err;
			lastError = { status: 0, keyIndex: i };
			continue;
		}
	}
	throw new Error(`All keys exhausted. Last: ${JSON.stringify(lastError)}`);
}

function jsonRpc(id, result, isError = false) {
	const body = { jsonrpc: "2.0", id };
	isError ? (body.error = result) : (body.result = result);
	return new Response(JSON.stringify(body), {
		headers: {
			"Content-Type": "application/json",
			"Access-Control-Allow-Origin": "*",
			"Access-Control-Allow-Methods": "POST, OPTIONS",
			"Access-Control-Allow-Headers": "Content-Type, Authorization, MCP-Protocol-Version",
		},
	});
}

async function handleMCP(body, env) {
	const { id, method, params } = body;
	const keys = loadKeys(env);

	switch (method) {
		case "tools/list":
			return jsonRpc(id, { tools: TOOLS });

		case "tools/call": {
			const { name, arguments: args } = params || {};
			const endpoint = ENDPOINT_MAP[name];
			if (!endpoint)
				return jsonRpc(id, { code: -32601, message: `Unknown tool: ${name}` }, true);
			try {
				const result = await apiCall(endpoint, { ...args }, keys);
				return jsonRpc(id, {
					content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
				});
			} catch (err) {
				return jsonRpc(id, { code: -32000, message: err.message }, true);
			}
		}

		default:
			return jsonRpc(id, { code: -32601, message: `Unknown method: ${method}` }, true);
	}
}

export default {
	async fetch(request, env) {
		const url = new URL(request.url);

		// Auth check — Bearer token required for all non-OPTIONS, non-health
		const auth = request.headers.get("Authorization") || "";
		const expected = env.BEARER_TOKEN || "";
		if (request.method !== "OPTIONS" && url.pathname !== "/health") {
			if (!auth.startsWith("Bearer ") || auth.slice(7) !== expected) {
				return new Response(JSON.stringify({ error: "Unauthorized" }), {
					status: 401,
					headers: {
						"Content-Type": "application/json",
						"Access-Control-Allow-Origin": "*",
						"WWW-Authenticate": "Bearer",
					},
				});
			}
		}

		if (request.method === "OPTIONS")
			return new Response(null, {
				headers: {
					"Access-Control-Allow-Origin": "*",
					"Access-Control-Allow-Methods": "POST, OPTIONS",
					"Access-Control-Allow-Headers":
						"Content-Type, Authorization, MCP-Protocol-Version, Mcp-Method, Mcp-Name",
					"Access-Control-Max-Age": "86400",
				},
			});

		if (request.method === "GET" && url.pathname === "/health")
			return new Response(JSON.stringify({ status: "ok" }), {
				headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
			});

		if (request.method === "POST" && url.pathname === "/mcp") {
			let body;
			try {
				body = await request.json();
			} catch {
				return jsonRpc(null, { code: -32700, message: "Parse error" }, true);
			}
			if (body.jsonrpc !== "2.0" || !body.method)
				return jsonRpc(body?.id ?? null, { code: -32600, message: "Invalid Request" }, true);
			return await handleMCP(body, env);
		}

		return new Response("Not found", { status: 404 });
	},
};
