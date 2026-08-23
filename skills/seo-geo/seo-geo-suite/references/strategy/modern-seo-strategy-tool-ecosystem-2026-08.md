## 第五章：工具生態（2026/8 更新）

> 更新日期：2026/8/9（GitHub star 數為當日 API 實測）。GEO 已從新名詞變成月搜 22,000 次的成熟類別，工具分三種任務：引用追蹤、可見度稽核、內容優化。

### 5.1 付費 GEO 工具

| 工具 | 2026/8 現況 | 價格 | 適合誰 |
|---|---|---|---|
| **Profound**（tryprofound.com） | 已成為 GEO 首家獨角獸：2026/2 完成 $96M Series C（Lightspeed 領投），估值 $10 億。客戶含 Figma、Ramp、MongoDB、Plaid 等 | 免費入門方案 + 企業客製報價 | 品牌大廠；要 share of voice + sentiment + prompt 層級排名的企業 |
| **Ahrefs Brand Radar**（ahrefs.com） | 追蹤 6 平台（Google AI Overviews/AI Mode、ChatGPT、Perplexity、Gemini、Copilot），prompt 資料庫已擴至 2.18–2.39 億筆；另延伸 YouTube/TikTok/Reddit 追蹤（beta）。注意：第三方評測指其 ChatGPT/Perplexity 追蹤有準確度落差（關鍵字為本 vs prompt 層級） | 內含於 Ahrefs Lite $129/月起；部分方案加購模組約 $398–699/月（各來源說法不一，未確認） | 已是 Ahrefs 用戶、主戰場在 Google AI Overviews 者 |
| **SEMrush AI Visibility Toolkit**（semrush.com） | 單獨加購 $99/月/domain；Semrush One（SEO+AI 一套）$199–549/月。prompt 庫 1.3 億+，覆蓋 ChatGPT/AIO/Gemini/Claude/Grok/Perplexity/DeepSeek | $99/月起 | 已是 Semrush 用戶，想 SEO 與 AI 可見度一個儀表板搞定 |
| **Otterly.AI**（otterly.ai） | 仍是最低門檻付費工具：追蹤 7 引擎（含 AI Mode、Copilot；Claude/Gemini 低階方案需加購），每日追蹤 + 引用分析 + GEO 稽核 | Lite $29/月（15 prompts）→ Standard $189 → Premium $489/月 | 個人/小團隊，想低成本開始每日追蹤 |
| **OGTool**（ogtool.com） | 2026 竄紅的新玩家（創辦人前 Stanford、bootstrapped 500k+ 自然流量）：ChatGPT 關鍵字可見度 + Reddit 監控與 AI 回文、幻覺偵測。另有代管服務（Reddit Managed $6,000/月、GEO Managed $9,000/月） | Starter $99/月 → Growth $199 → Scale $399 | 想同時經營 Reddit 社群訊號 + AI 可見度的品牌 |
| **其他新面孔** | Gauge（$99/月起，引用率診斷）、ZipTie.Dev（$99/月 400 次檢查）、AIclicks（$59–499/月）、SE Ranking Visible（$49/月起）、Peec AI（約 €75/月）、Writesonic GEO（$199/月） | 見各官網 | 依預算與引擎覆蓋選擇 |

### 5.2 開源 GEO 生態（2026/8/9 GitHub API 驗證）

| 專案 | Stars | 現況 | 用途 |
|---|---|---|---|
| **GEOFlow**（github.com/yaojingang/GEOFlow） | 3,156 ⭐（727 forks，當日仍持續更新） | 開源 GEO 內容工程 + 多站點分發系統：AI 任務、RAG/語意分塊、GEOFlow Agent、WordPress 發佈、Analytics。Apache-2.0、多語言文件、含生產級 docker-compose | 自架內容生產與多站分發流水線 |
| **GEORank**（github.com/yaojingang/GEORank） | 364 ⭐（2026 新專案） | 開源 GEO 排名追蹤平台：Next.js + FastAPI，多模型 Provider 池、額度控管、GEO 診斷規則 | 自架排名/可見度追蹤（補上「測量」環節） |
| **yao-geo-skills**（github.com/yaojingang/yao-geo-skills） | 687 ⭐ | 20 個 GEO 專用 skill，持續更新 | Agent 驅動的 GEO 工作流 |
| **yao-meta-skill**（github.com/yaojingang/yao-meta-skill） | 2,354 ⭐ | Skill OS 框架：把 workflow 編譯為跨平台 agent skill，含 eval、審查門戶、證據帳本 | 把 GEO 流程打包成可重用 skill |
| **GEO/AEO Tracker**（github.com/danishashko/geo-aeo-tracker） | 活躍 | 開源、local-first 可見度儀表板：BYOK、6 模型並行、13 個功能頁（SRO 分析、引用機會、競爭者 battlecard、AEO 稽核）、Vercel 一鍵部署。資料費僅 Bright Data PAYG（約 $1.5/1K 筆） | $0 月費的品牌追蹤 |
| **awesome-generative-engine-optimization**（github.com/amplifying-ai/awesome-generative-engine-optimization） | 442 ⭐ | 2026 持續維護的 GEO 資源清單 | 找工具/研究入口 |

### 5.3 免費手動速測：仍是最務實的入門

2026 年手動法依然成立，業界共識是：**≤30–50 個 prompts、單一市場、每月一次**的規模用手動即可（Google Sheet 追蹤表，每週約 1–2 小時）；但超過 100 prompts、跨 4+ 引擎、要趨勢線與競爭者對比時，手動已結構上不可行，必須自動化。免費資料源別漏：GA4 的 AI referral 流量、GSC 的 AI Overviews 曝光，零成本且是官方數據。

### 5.4 2026/8 推薦組合

- **免費組合（$0）**：GA4 + GSC + 手動速測（每季）→ 需要自動化時自架 GEO/AEO Tracker（BYOK）或 GEORank + GEOFlow
- **輕量付費（$29–99/月）**：Otterly Lite、OGTool Starter、ZipTie 三選一，搭配手動競品抽查
- **中階（$99–299/月）**：Semrush One（SEO+AI 一套）或 Ahrefs Lite（含 Brand Radar 基本）+ Otterly Standard
- **企業（客製報價）**：Profound 或 Ahrefs Brand Radar 全模組，配 OGTool 代管做 Reddit 訊號經營

測量方法論文《From Citation Selection to Citation Absorption》仍為跨平台 GEO 測量的學術基準，詳見 references。
