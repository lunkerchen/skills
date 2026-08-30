# 客戶導向 SEO/GEO 報告輸出契約

## 1. 適用範圍與產業 archetype

本契約適用於**客戶專屬 SEO/GEO 診斷或提案報告**。報告必須以實際受檢網站、頁面與可取得證據為基礎，不得只輸出通用分數、通用能力矩陣或沒有對象的建議。

產出前先選定一個產業 archetype：

- **在地服務型**：以地點、服務、設施、到店／預約與評論決策為主，例如寵物旅館、診所、餐飲或門市服務。
- **B2B 產品／製造型**：以產品分類、規格、認證、應用、技術文件與詢價／採購決策為主，例如電子零組件、設備與製造業。

兩種 archetype 的證據欄位、內容模型與實施項目不可混成一份通用能力矩陣。若企業同時有兩種業務，分節呈現並分別驗證。

## 2. 強制報告結構

每份客戶報告至少包含以下六個區段：

### Metadata

以表格列出：

| 欄位 | 內容 |
|---|---|
| Target | `{target}` |
| Ref | `{audit_ref}` |
| Scope | 審計範圍、頁面與資料期間 |
| Auditor | `{auditor}` |
| Archetype | 在地服務型或 B2B 產品／製造型 |
| Audit time | 含時區的測試時間 |

### 01 執行摘要與核心現狀

先用一個 lead box 說明現況、主要風險與決策重點，再列出 3 個優先發現。每個 finding 以 `danger`、`warning` 或 `info` 分層，並附證據與信心等級；不要以抽象分數取代現況描述。

### 02 傳統搜尋與生成式 AI 搜尋差距分析

使用至少四欄的 Gap Matrix：

| 審計維度 | 當前現狀與證據 | 優化方案 | 可驗收指標／驗證方法 |
|---|---|---|---|
| … | … | … | … |

最後一欄必須寫可驗收指標與驗證方法，例如「指定 URL 的 `title`、`canonical` 與 JSON-LD 通過檢查」或「以固定查詢、引擎、地區與採樣時間保存答案快照並比較引用 URL」。不得寫成排名前三、推薦率提升、流量倍增等無證據保證。

### 03 Implementation Artifact

針對真實目標對象提供可落地的程式碼或內容片段，例如 JSON-LD、HTML、`robots.txt`、Markdown twin、FAQ、型錄欄位或技術文件模板。每個示例都必須標示狀態：

- `current`：目前讀回或檢測到的實作。
- `proposed`：本報告提出、尚未部署的版本。
- `deployed`：已部署，且有 URL、狀態碼或讀回內容證明。

不得把 `proposed` 寫成 `deployed`。範例中的企業資料使用 `{target}`、`{official_url}` 等佔位符，或只使用已由證據支持的實際值。

### 04 敏捷 SEO + GEO Roadmap

通常規劃 3–7 個工作天、4 個步驟；此為 quote／estimate 的規劃估算，不是結果保證。每一步都列出：

| 步驟 | 天數 | 交付物 | 負責人 | 相依條件 | 驗證方式 |
|---|---:|---|---|---|---|
| … | … | … | … | … | … |

### CTA、報告邊界與來源

CTA 與事實診斷分開。PoC 範圍、週期、價格、費用、付款條件與聯絡方式若出現，逐項標示 `quote`、`estimate` 或 `client-specific proposal`。清楚列出未檢查項目、資料期間、限制與來源層級。

## 3. 診斷書版面呈現契約

若輸出為 HTML 或可視化報告，沿用既有寵物旅館／電子業診斷書的版面語言：

- **Header**：報告標題、報告類型、`Target`、`Ref`、`Scope`、`Auditor`、`Archetype` 與含時區的審計時間。
- **Lead box**：置於 01 區段開頭，用一段話說明現況、最大風險與本報告要支持的決策。
- **Finding cards**：3 張優先發現卡，依 `danger`、`warning`、`info` 分色；每張卡必須能追溯到實際證據，不用顏色代替信心等級。
- **Gap Matrix**：使用四欄表格；桌面版完整呈現，行動版允許表格容器橫向捲動，不把欄位內容截斷。
- **Implementation Artifact**：使用獨立程式碼／內容區塊，顯示 `current`、`proposed` 或 `deployed` 狀態；`deployed` 必須附讀回證據。
- **Roadmap**：使用 4 格或 4 列 timeline，逐項顯示天數、交付物、負責人、相依條件與驗證方式。
- **CTA box 與 footer**：CTA 獨立於事實診斷；footer 顯示報告機密／使用範圍、資料時間與報告邊界。

視覺版面可以採用深色工程感、紙張卡片或其他既有品牌樣式，但不得以裝飾取代證據、狀態與驗收欄位。

## 4. Finding 欄位契約

每個 finding 必須包含：

1. **問題**：可被處理的明確敘述。
2. **實際觀察證據**：URL、頁面、元素、請求／測試結果與測試時間；沒有實測時寫「未測量」。
3. **影響**：對讀者理解、採購判斷、自然搜尋或轉換流程的影響。
4. **信心等級**：`high`、`medium` 或 `low`，並說明判定依據。
5. **修正動作**：對應到頁面、內容、技術設定或流程的具體改動。
6. **驗收方法**：重測命令、URL、欄位、查詢或時間窗，以及通過條件。

## 5. 產業內容模型

### 在地服務型必查項目

- 分店、服務區域、商圈與地理對象。
- 服務項目、價格／方案（若公開）、特色與設施。
- 營業時間、入住／到店規則、預約流程與聯絡方式。
- 評論、評分、評論來源與更新時間；不得把第三方評論當成官方事實。
- `LocalBusiness`、`Service`、`FAQPage`、地址、電話、地圖與分店頁的一致性。
- 每個地點的可讀內容、照片／設施描述、交通資訊與可驗證預約 CTA。

### B2B 產品／製造型必查項目

- 產品分類、型號、規格、尺寸、材料、性能與適用條件。
- 認證、標準、測試報告與有效期間；區分自述與第三方證明。
- 應用情境、產業別、相容性、限制與替代／比較採購查詢。
- 多語系路由、語言切換、canonical 與各語系內容是否對應。
- 型錄、PDF、下載檔案的文字可讀性、版本、日期、索引與引用入口。
- 技術文件、FAQ、機器可讀欄位、聯絡窗口、MOQ／交期（若公開）與詢價流程。

## 6. 證據邊界與成效用語

- Google 官方政策、Google Search Console、Ahrefs、第三方報導與客戶自有資料分開標示層級與用途。
- Google 官方政策可說明規範或建議，**不能被寫成排名保證**。
- AI crawler／agent 能存取頁面只代表抓取觀測信號，不等於 ChatGPT、Perplexity 或其他引擎已產生 citation。
- 沒有實測就寫「未測量」，不要填入推估值。
- 過去寵物旅館或電子／製造業案例的數字只能作為已標示案例背景，不能複製成普遍基準、預期成效或保證。
- 「預期成效」改寫為可驗收指標／驗證方法；禁止無證據的「排名前三」「推薦率提升」「流量倍增」等保證。
- 任何提案、估算與部署狀態都必須分開標示，並保留測試時間與資料期間。

## 7. 交付前 Checklist

```text
[ ] 已確認 Target、Ref、Scope、Auditor、測試時間與產業 archetype。
[ ] 報告包含 Metadata、01 摘要、02 Gap Matrix、03 Implementation Artifact、04 Roadmap 與 CTA／邊界／來源。
[ ] 每個 finding 都有問題、實際 URL／頁面／元素／時間、影響、信心、動作與驗收方法。
[ ] Gap Matrix 至少四欄，最後一欄是可驗收指標／驗證方法。
[ ] 沒有把排名、推薦率、流量或轉換結果寫成無證據保證。
[ ] 每個程式碼／內容片段都標示 current、proposed 或 deployed。
[ ] deployed 狀態有讀回 URL、狀態碼或內容證據；提案沒有冒充部署。
[ ] Roadmap 每步含天數、交付物、負責人、相依條件與驗證方式。
[ ] 3–7 個工作天、價格與 PoC 已標示為 quote／estimate／client-specific proposal。
[ ] 已依 archetype 完成在地服務型或 B2B 產品／製造型必查項目。
[ ] Google、Ahrefs、第三方與自有資料的證據層級已分開。
[ ] 未實測的 AI citation、流量與成效標為未測量。
[ ] 已列出資料期間、未檢查項目、限制與來源。
[ ] Markdown fence 成對，URL、Schema 與程式碼可解析。
```

## 8. 通用 Markdown Outline Template

`````markdown
# {target} SEO/GEO 診斷／提案報告

| Target | {target} |
|---|---|
| Ref | {audit_ref} |
| Scope | {scope} |
| Auditor | {auditor} |
| Archetype | {local-service 或 b2b-manufacturing} |
| Audit time | {timestamp with timezone} |

> **Lead box：** {一句話現況、主要風險與決策重點}

## 01 執行摘要與核心現狀

### 優先發現 1：{title}（danger）
- 問題：
- 實際觀察證據（URL／頁面／元素／測試時間）：
- 影響：
- 信心等級：
- 修正動作：
- 驗收方法：

### 優先發現 2：{title}（warning）
{same finding fields}

### 優先發現 3：{title}（info）
{same finding fields}

## 02 傳統搜尋 vs 生成式 AI 搜尋差距分析

| 審計維度 | 當前現狀與證據 | 優化方案 | 可驗收指標／驗證方法 |
|---|---|---|---|
| {dimension} | {evidence} | {action} | {acceptance test} |

## 03 Implementation Artifact

### {artifact name}（status: current／proposed／deployed）
```json
{real-target JSON-LD or other artifact}
```
驗證方式：{validator, URL read-back, status code, or content comparison}

## 04 敏捷 SEO + GEO Roadmap

| 步驟 | 天數 | 交付物 | 負責人 | 相依條件 | 驗證方式 |
|---|---:|---|---|---|---|
| 1 | {days} | {deliverable} | {owner} | {dependency} | {test} |
| 2 | {days} | {deliverable} | {owner} | {dependency} | {test} |
| 3 | {days} | {deliverable} | {owner} | {dependency} | {test} |
| 4 | {days} | {deliverable} | {owner} | {dependency} | {test} |

## CTA、報告邊界與來源

- CTA：{next action}
- PoC：{quote／estimate／client-specific proposal}
- 價格／週期／付款：{quote 或 estimate；非結果保證}
- 報告邊界：{unmeasured items, date range, limitations}
- 來源：{Google official / Ahrefs / third-party / first-party, each separated}
`````
