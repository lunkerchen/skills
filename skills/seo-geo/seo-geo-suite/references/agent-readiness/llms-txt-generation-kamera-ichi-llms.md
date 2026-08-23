# your-project llms.txt / llms-full.txt 實作範例（靜態站：Vite + CF Pages）

Site: your-app.example.com — 台灣二手攝影器材 C2C 交易平台。
非 Next.js，是 Vite 建置 + CF Pages 部署，商品/行情走 D1+API，指南頁由 `frontend/scripts/generate-guide-pages.mjs` 預渲染成靜態 HTML。這是「無內容管線靜態站用 public/ 手寫 llms 檔」的代表案例。

## 為何不是動態 route
- 無 App Router / route handler；內容集合不是持續增長的部落格
- 指南頁數固定（5 篇），build script 每次重跑
- 商品/行情是 API 驅動動態資料，llms.txt 只描述 API 端點而非窮舉商品

## llms.txt（輕量）結構
```markdown
# your-project your-marketplace — Taiwan
> 一句話定位（含平台本質與地域）

## About
- 平台簡介、核心機制（零手續費、面交、互評）
- 內容更新日期 + 「以公開頁面/API 即時回應為準」聲明

## Key features
| 功能 | 說明 |          ← 表格（AI 引用率高）

## Pages
- [標題](url)：一行說明

## Buying guides (AEO/How-To)
- [指南](url)：一句話總結     ← 讓 AI 直接把指南當答案來源

## API endpoints (for AI agents & tools)
- `GET https://.../api/listings/search?q=&category=&listing_type=`（附參數）
- 依分類品牌、單筆 listing、行情清單、型號統計

## Supported brands / Categories / Condition guide
| Condition | Label | Description |   ← 全都是表格

## Relevant links
- privacy / terms / about
```

## llms-full.txt（全站語料庫）新增重點
- **完整平台概覽**：核心原則（平台僅媒合、面交優先、互評、零手續費）
- **AEO Direct Answer 區塊**：每個指南給「核心結論 + 步驟一/重點一」純文字可引用版，對齊頁面 HowTo JSON-LD
- **動態路由 Schema 標記說明**：listing→Product/Demand+Offer、trends→Dataset、guides→Article+HowTo+BreadcrumbList、Markdown Twin
- **What we do not do**：不鑑定真偽、不代收款、不介入線下糾紛

## 對應的頁面 JSON-LD 升級（同一趟 build 做的）
`generate-guide-pages.mjs` 的 guide detail 注入 `@graph`：
- Article：+ `inLanguage: zh-TW` + `speakable`（cssSelector: ['h1','h2','article > header > p']）
- **HowTo**：`step: guide.sections.map(...)` → 每個 section 一個 `HowToStep{position,name,text}`
- BreadcrumbList

## 陷阱
- llms-full.txt 的 AEO 區塊必須用手寫步驟核心結論，不能只 dump 頁面 HTML
- 兩檔都需「更新日期 + 即時回應為準」聲明，防過期數字當權威
- 靜態手寫檔不會自動跟上內容變化 — 內容管線建立後應升級回動態 route
