# AEO 實戰手冊（2026/8 版）— 外部 repo 精華萃取

> 萃取來源（皆 MIT/Apache-2.0 開源）：
> - AgriciDaniel/claude-seo v2.2.4（13.8K⭐）— GEO/AEO 方法論與 Google 官方立場
> - harlan-zw/nuxt-seo + nuxt-ai-ready（1.4K⭐）— AEO 技術實作
> - dodopayments/dualmark（Apache-2.0）— Markdown twin + content negotiation spec
> - addyosmani/agentic-seo（289⭐）— 文檔對 AI coding agents 的可讀性評分
> - Auriti-Labs/geo-optimizer-skill（655⭐）— 8 類別 × 47 方法評分框架
> - 學術：AutoGEO（arXiv:2510.11438, ICLR 2026）、E-GEO（arXiv:2511.20867）

---

## 一、核心立場：AEO/GEO 只是 SEO 的換皮

Google 官方《AI Optimization Guide》明言：「針對生成式 AI 搜尋做優化，從 Google 的角度來看**仍然是 SEO**；AEO 與 GEO 只是同一件事的重新命名。」AI Overviews 與 AI Mode 架構在傳統排名的品質系統之上，技術上只有兩層加成：**RAG/grounding** 與 **query fan-out**。**資格門檻**：頁面必須先被收錄且有資格顯示 snippet，才能出現在任何 AI 功能 — 沒有獨立的「AI 索引」。

Google 同時拆穿五個常見迷思：
1. 不需要 llms.txt / AI 專用標記檔
2. 不需要把內容「切塊」
3. 不需要為 AI 改寫特定措辭或長尾關鍵字
4. 不需要追「不真實的品牌提及」
5. 不需要為 AI 過度投資結構化資料

真正重要的是**獨特、非商品化、第一手**的內容（Google 對比範例：「首次購屋的 7 個祕訣」vs「我們為何放棄驗屋並省下錢：下水道管線內部實錄」）。

來源：claude-seo `skills/seo-geo/SKILL.md`、`references/google-ai-optimization-guide.md`

---

## 二、Citability Score（可引用性評分）

| 訊號 | 規則 |
|---|---|
| **Passage 長度** | 最佳 134–167 字（英文）；段落要能單獨被引用 |
| **Front-loading** | ~44% 的 AI 引用來自頁面前 30%；段落**前 40–60 字直接給答案** |
| **定義句型** | 「X 是…」「X 指…」直接定義 |
| **自包含** | 答案塊可獨立抽出、不需上下文 |
| **具體數據** | 含數據、可直接引用的句子；獨特數據點（別處沒有） |
| **來源標註** | 宣稱附具體來源 |
| 弱訊號 | 含糊泛論、無證據意見、結論埋後面、無具體數據 |

---

## 三、Brand Mentions > Backlinks（Ahrefs 2025/12，75,000 品牌）

品牌提及與 AI 可見度的相關性比反向連結**強 3 倍**：

| 訊號 | 與 AI 引用的相關性 |
|---|---|
| YouTube 提及 | ~0.737（最強） |
| Reddit 提及 | 高 |
| Wikipedia 曝光 | 高 |
| LinkedIn 曝光 | 中 |
| Domain Rating（反向連結） | ~0.266（弱） |

只有 **11% 的網域**同時被 ChatGPT 與 Google AI Overviews 引用 → 平台專屬優化是必要而非選配。

---

## 四、平台引用差異

| 平台 | 引用來源特徵 | 優化重點 |
|---|---|---|
| Google AI Overviews | 與排名高度相關（92% 引用來自前 10 名頁面，其中 47% 來自第 5 名之後） | 傳統 SEO + passage 優化 |
| Google AI Mode | 與排名弱相關；引用池更大（每查詢 ~9 網域） | 新鮮度、實體權威、第 5 名後也可被引用 |
| ChatGPT | Wikipedia 47.9%、Reddit 11.3% | 實體曝光、權威來源 |
| Perplexity | Reddit 46.7%、Wikipedia | 社群驗證、討論串 |
| Bing Copilot | Bing 索引 | Bing SEO、IndexNow |

AIO 與 AI Mode 結論相同約 86%，但引用的 URL 只有 **13.7% 重疊**（Ahrefs，54 萬查詢對）→ 兩者都要評分。AI 功能外觀沒有專屬 opt-out 檔，只能用 nosnippet / data-nosnippet / max-snippet / noindex 控制。新訊號：Preferred Sources（Google 正研議當排名訊號）、「Highly Cited」徽章。

---

## 五、llms.txt 證據本位立場

- Google 官方（2026-06-29 更新）：不需要 llms.txt，Google 搜尋**忽略它們**；John Mueller 稱其 discovery 用途是「死路」
- 證據：SE Ranking 30 萬網域研究中，50 個最常被 AI 引用的網域**只有 1 個**有 llms.txt；OtterlyAI 日誌僅 **0.1%** 的 AI 流量打到 llms.txt
- **例外**：AI 寫碼代理（Cursor、Claude Code 等）會讀取 → 開發者工具網站值得發布；一般商業網站僅為零成本防禦性選項
- 審計時回報存在與否，但**不賦予引用權重**

---

## 六、Markdown Twin（內容協商）實作

dualmark 做法：每個頁面有 markdown 分身（twin），依請求端自動決定回傳格式：

- 瀏覽器 → HTML；已知 AI bot UA（GPTBot、ClaudeBot、PerplexityBot 等 24 個）→ markdown；`Accept: text/markdown` → markdown；直接請求 `.md` URL → markdown；其餘 → HTML 帶 `Link rel="alternate"` 廣告 twin
- URL 慣例：`/about` → `/about.md`、`/` → `/index.md`；協商依 RFC 7231 解析 Accept（q-value、wildcard），無可接受格式回 406

| Header | 用途 |
|---|---|
| `Content-Type: text/markdown; charset=utf-8` | markdown 回應（charset 必帶） |
| `Vary: Accept` | 快取鍵含 Accept，防止 CDN 快取錯格式 |
| `X-Markdown-Tokens: <整數>` | body 估計 token 數，供 agent 預算 context |
| `X-Robots-Tag: noindex` | twin 不進索引，避免重複內容 |
| `Link: <url.md>; rel="alternate"; type="text/markdown"` | HTML 頁廣告 twin（RFC 8288） |
| `Cache-Control: public, max-age=3600` | 允許 CDN 以 Vary: Accept 快取 |

llms.txt 延伸（dualmark spec）：「## What We Do Not Do」區塊明確列出品牌「不是什麼」，防止 AI 把同名實體搞混（消歧義）；連結用 HTML URL（agent 靠 Link header 找 twin）；llms-full.txt 建議至少為 llms.txt 的 1.5 倍大；兩者 noindex。

---

## 七、Agent-Readability 評分標準

### 7.1 @vercel/agent-readability（`npx @vercel/agent-readability audit <url>`）

分數 = round(通過 checks / 總 checks × 100)；90+ Excellent、70-89 Good、50-69 Fair。三層檢查：

- **站級**：`/llms.txt`（或 .well-known/docs 路徑）、robots.txt 不擋 GPTBot/ClaudeBot/CCBot/Google-Extended、sitemap.xml + **sitemap.md 雙格式**、AGENTS.md（含 install/config/usage）、所有頁面都能被發現（孤兒頁對 AI 不可見）
- **頁級**：HTTP 200、≤1 次 redirect、無 noindex/noai/noimageai；canonical；meta description + og:title + og:description + html lang；JSON-LD 含 title/description/canonical/dateModified/BreadcrumbList；每頁 3+ 個 h1-h3；text-to-HTML 比例 >15%；code block 帶 language-* class；API 頁連結 openapi.json
- **伺服器**：每頁 .md/.mdx mirror（frontmatter 含 title/description/last_updated）、HTML 內 `<link rel="alternate" type="text/markdown">`、markdown 回應帶 `Link: <html-url>; rel="canonical"`、支援 `Accept: text/markdown`、markdown 頁尾附 `## Sitemap` 區塊

### 7.2 agentic-seo 10 checks（文檔對 AI coding agents 的可讀性）

| 類別 | Check | 配分 | 檢查內容 |
|---|---|---|---|
| Discovery 25 | robots-txt | 10 | AI crawler 沒被擋、有明確 Allow |
| | llms-txt | 10 | 結構化索引，含描述與 token 數 |
| | agents-md | 5 | AGENTS.md/CLAUDE.md 含專案 context |
| Content 25 | content-structure | 15 | 標題階層、語意 HTML、程式範例、表格 |
| | markdown-availability | 10 | 有 markdown 來源、低 HTML 噪音、無 JS 依賴 |
| Token 25 | token-budget | 15 | 每頁 token 數（上限 25,000/頁） |
| | meta-tags | 10 | AI 友善 meta、token 數 meta |
| Capability 15 | skill-md | 10 | skill 檔描述能力、輸入、限制 |
| | agent-permissions | 5 | agent 存取規則與 rate limit |
| UX 10 | copy-for-ai | 10 | Copy-for-AI 按鈕、raw view 連結 |

等級：A 90-100、B 75-89、C 60-74、D 40-59、F 0-39。`agentic-seo init` 可 scaffold llms.txt/AGENTS.md/skill.md；支援 CI（--threshold）。

---

## 八、GeoReady 0–100 評分框架：8 類別

| 類別 | 配分 | 檢查什麼 |
|---|---|---|
| robots.txt | 18 | 4 隻「引用機器人」OAI-SearchBot/ClaudeBot/Claude-SearchBot/PerplexityBot 全放行(13)；存在(5) |
| llms.txt | 18 | 存在(5)；H1+blockquote(3)；H2 區段+連結(4)；深度漸進 1,000/5,000 字(2+2)；llms-full.txt(2) |
| Schema JSON-LD | 16 | 任一有效(2)；5+ 屬性(3)；FAQPage/Article/Organization/WebSite 各 3/3/3/2 |
| Meta Tags | 14 | title(5)、canonical(3)、Open Graph(4)、description(2) |
| 內容品質 | 12 | H1(2)、統計(1)、外部引用(1)、≥300 字(2)、H2/H3(2)、清單/表格(2)、前 30% 前載(2) |
| 品牌與實體 | 10 | 品牌名一致(3)、sameAs 知識圖譜(3)、about/contact(2)、地理身分(1)、主題聚焦(1) |
| Signals | 6 | html lang(3)、RSS/Atom(2)、dateModified 新鮮度(1) |
| AI Discovery | 6 | `/.well-known/ai.txt`(2)、`/ai/summary.json`(2)、`/ai/faq.json`(1)、`/ai/service.json`(1) |

級距：86-100 Excellent、68-85 Good、36-67 Foundation、0-35 Critical。三個設計原則：①**引用機器人優先** — 只放行 GPTBot 不夠，即時引用靠 OAI-SearchBot 等 4 隻；②**漸進式給分** — llms.txt 逐層加分；③**不計分但揭露的 Bonus 檢查**：CDN 封鎖機器人、SPA 無 JS 可讀性、WebMCP 就緒度、8 個反引用訊號（CTA 過載/彈窗/內容稀薄/關鍵字堆砌）、8 種 prompt injection 模式、5 層信任堆疊（A–F 級）。

---

## 九、47 個 research-backed 方法 — 11 個有學術量測

| 方法 | 量測影響 | 執行要點 |
|---|---|---|
| 1. Cite Sources | **+30–115%**（最高） | 事實陳述內嵌連結到權威來源（.gov/.edu/學術/官方文件） |
| 2. Statistics | +40% 平均 | 模糊宣稱換具體數字+來源+年份；避免超過 3 年舊數據 |
| 3. Quotation Addition | +30–40% | 專家直接引述 `"引述" — 姓名、頭銜、機構、年份`；YMYL 必用 |
| 4. Authoritative Tone | +6–12% | 定義→運作→實務意涵；刪 "often/might"，改精確範圍 |
| 5. Fluency | +15–30% | 句子 15–25 字、邏輯連接詞、每段主題句 |
| 6. Easy-to-Understand | +8–15% | 術語先白話再技術；5+ 術語就做詞彙表 |
| 7. Unique Words | +5–8% | 同義詞變化（最低優先） |
| 8. Technical Terms | +5–10% | 首次出現給全名+縮寫（APR、LTV） |
| 9. Keyword Stuffing | ⚠️ 中性或負面 | 學術實測無效、傷流暢度 — GEO 不適用堆砌 |
| 10. Answer-First（AutoGEO） | +25% | 每個 H2 後 150 字內先給結論：Answer→Context→Detail |
| 11. Passage Density（Stanford） | +23% | 段落 50–150 字、每段至少一個具體數據點 |

領域差異：Cite Sources/Statistics/Answer-First 對金融、健康、科學影響最高；Quotation 對歷史有效；Keyword Stuffing 全領域禁用。

---

## 十、學術新基準（2023 KDD 之後）

**AutoGEO（ICLR 2026, arXiv:2510.11438）**：不必靠人猜測 GEO 偏好，可自動萃取 — 用 frontier LLM 解釋「生成引擎偏好什麼」→ 萃取偏好規則 → 餵給 prompt 改寫系統（AutoGEO_API）與低成本模型訓練（AutoGEO_Mini）。實務意涵：可針對自家利基領域「問 LLM 引擎偏好 → 轉成改寫規則」循環驗證。

**E-GEO（arXiv:2511.20867）**：首個電商 GEO 資料集（13,747 條查詢 × 10 listings）。結論：①輕量 prompt meta-optimization 顯著勝過手寫啟發式；②優化 prompt 有穩定跨領域通用模式 → 存在「普遍有效」GEO 策略；③加 in-prompt 防禦後增益仍真實 → **GEO 反映真實內容改善而非操縱**（學術背書）。

---

## 十一、優先實作順序（非技術站）

1. **robots.txt 檢查**（10 分鐘）：確認 GPTBot/ClaudeBot/PerplexityBot 沒被擋 — 最便宜保險
2. **llms.txt + llms-full.txt**：部落格直接「索引＋全文」雙檔架構
3. **每頁 .md twin + Link header**：Astro/Next/Nuxt 皆有現成模組（dualmark、nuxt-ai-ready）
4. **每頁 3+ 標題 + JSON-LD（BreadcrumbList/dateModified）+ text-to-HTML >15%**
5. **sitemap.md**：XML sitemap 多生成一份 markdown 版（成本極低）
6. **驗證迴圈**：`npx @vercel/agent-readability audit` 或 `npx agentic-seo --url` 打分補強

技術站（文件/API）再加：AGENTS.md、skill.md、OpenAPI schema 連結、MCP server。

---

## 十二、Who / How / Why 測試（內容品質門檻）

每頁先過 Google 三問：**Who** 誰寫的（署名、作者頁、專業憑證；YMYL 不可妥協）？**How** 怎麼寫的（AI 輔助要揭露流程、有第一手研究）？**Why** 為何存在（「幫人」而非「騙點擊」）？警戒訊號：湊字數、無專業卻進利基搶流量、假造更新日期、大量內容輪換。

## 十三、Falsifiability 方法論

每條建議附 4 欄位：①賴以成立的**第一性原理觀察**；②**相依關係**；③明確的「**怎麼知道這失敗了？**」檢查；④可監測的**領先指標**。審計流程：PERCEIVE（觀察）→ ANALYZE（思考/連結）→ VALIDATE（接受）→ ACT（創造）。
