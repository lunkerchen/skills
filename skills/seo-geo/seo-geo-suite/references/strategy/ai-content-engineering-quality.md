# AI 內容工程與 SEO 品質層

## 適用範圍與定位

本參考文件用於 SEO/GEO 工作臺的內容規劃、研究、撰寫、審核與發布。它是本工作臺採用的可重用內容工程流程，不是 Google 的完整官方規格，也不是排名或 AI 引用的安全豁免。適當使用 AI 或自動化，不會因產製方式本身而違規；Google 關注的是內容是否有價值、原創性與操縱排名意圖。所謂 scaled content abuse，重點在大量產出低價值、缺乏原創性且主要用來操縱排名的內容。

## 發稿前的五問 brief

在研究或生成前，先回答 Ahrefs 提出的五個前置問題：

1. **Reader**：這篇內容服務哪一類讀者？他現在要完成什麼任務？
2. **Promise**：讀者看完後會得到什麼具體答案、決策依據或可執行成果？
3. **Point of view**：內容採取什麼明確角度？哪些判斷不是泛泛重述？
4. **Evidence**：哪些主張需要來源、實測、資料或案例支持？
5. **Information gain**：相較既有結果，新增了什麼可驗證、可使用的資訊？

### 最小 brief 模板

```text
主題／目標查詢：
Reader（讀者與任務）：
Promise（可交付承諾）：
Point of view（角度與取捨）：
Evidence（預計需要的證據）：
Information gain（新增價值）：
發布目的與主要轉換：
具體 owner：
第二位人類審閱者：
```

## 原始材料與 Source of Truth

優先使用能產生第一手差異的材料：訪談、內部知識、專有或自有資料、真實示範、失敗實驗，以及具體案例。Source of Truth 至少分成四類：

- **facts/stats**：事實、統計、定義、時間與口徑。
- **explanations**：由專業者整理的原理、推理與限制。
- **product details**：產品、服務、價格、資格、版本與功能細節。
- **how-to guides**：經實際驗證的步驟、設定、前置條件與例外。

沒有來源或無法追溯的數字，不得進入草稿；只能標為「待補證據」。AI 可以協助整理、比較與提出問題，但不能替 Source of Truth 補空白。

## 分階段工作與四個品質閘門

研究、內容缺口、提綱、證據、草稿分開保存；不要用一份不透明的生成結果取代中間產物。每一閘門都可選擇**繼續、退回修正或終止**：

| 閘門 | 放行問題 | 退回／終止條件 |
|---|---|---|
| Gate 1 題目 | 題目是否對應明確 Reader、Promise、Point of view？ | 讀者不明、承諾空泛或只是追逐關鍵字。 |
| Gate 2 提綱 | 提綱是否能交付承諾，且列出原創角度與待證主張？ | 結構只是拼接排名頁、缺少 Information gain。 |
| Gate 3 證據 | 每個物質性主張是否有可追溯來源、時間、範圍與口徑？ | 無來源數字、來源衝突未解、證據不足。 |
| Gate 4 草稿 | 草稿是否忠實於證據、可被讀者使用，並完成風險與人工審核？ | 虛構引用、重大主張未驗證、無 owner 或第二位審閱者。 |

## 人工與 AI 的責任邊界

每篇內容必須指定具體 owner，並由第二位人類審閱者在發布前確認。人工審核不只是修正文句；審閱者必須能挑戰前提、追問證據、刪除章節、替換角度、要求補充研究，或取消發布。人工審核本身也不是安全豁免：若內容缺乏價值、原創性或證據，經人看過仍不可發布。

AI 可做摘要、分類、草稿變體、缺口提示與格式檢查；人類負責事實責任、取捨、風險判斷、發布與後續更新。保留研究、缺口、提綱、證據紀錄、草稿、審核決定與版本，讓結果可追溯。

## 證據記錄欄位

每筆重要主張至少記錄：

```text
claim：
claim_type（facts/stats | explanations | product details | how-to guides）：
source_url／來源名稱：
source_owner：
published_at／有效期間：
適用範圍與資料口徑：
原始摘錄或實測紀錄：
status（supported | contradicted | unverified）：
審閱者與審閱日期：
```

## 效率再投資

AI 節省的時間，優先投入資料更新、資料分析、免費工具、互動內容、實測與研究，而不是只增加頁面數。內容數量可以增加，但必須先證明每頁有讀者價值、原創資訊與維護責任。

## 發布後量測

至少分開追蹤：

- 搜尋點擊、曝光、CTR、排名；
- 停留表現與後續訪問；
- 工具或模板使用；
- 詢問、註冊與收入；
- 更新成本與內容維護時間。

GSC 的搜尋資料，與 AI citation/crawl signal 必須分開記錄與解讀。AI crawler 存取不等於被引用；引用觀測應保存查詢、引擎、地區、答案快照、引用 URL 與採樣時間。

## 事實邊界與來源

- **已核對**：Google Search Central 說明適當使用 AI 或自動化不因產製方式本身違規，並說明 scaled content abuse 的判斷重點；Google 的垃圾內容政策是合規參考，不是內容成效保證。
- **已核對但需限定**：Ahrefs 的五問（Reader、Promise、Point of view、Evidence、Information gain）是其內容策略建議，不是 Google 政策。Ahrefs 的個案數字或流程時間只能按原文情境引用，不能升格為普遍保證。
- **需限定**：The Verge 對 AI 內容品質、搜尋與出版產業案例的報導可作為背景與案例來源；報導內容不等於 Google 排名規則或整體錯誤率。
- **不可推論**：不要把 AI 偵測率、AI 占比、發文速度、重複率或相似度當成未公開的 Google 處罰門檻；Google 沒有在此文件中公布這些門檻。不要把 CNET 的 41/77 當成整體 AI 錯誤率，也不要把 Ahrefs 的 6–12 分鐘當成一般團隊保證。

## 可追溯來源

以下來源支撐本參考文件的事實邊界；Ahrefs 與 The Verge 的內容仍須按第一方自述或媒體報導理解，不升格為 Google 排名規則：

- Google Search Central，2023-02-08，AI 生成內容說明：<https://developers.google.com/search/blog/2023/02/google-search-and-ai-content>
- Google Search Central，現行垃圾內容政策，`scaled content abuse`：<https://developers.google.com/search/docs/essentials/spam-policies#scaled-content>
- Google，2024-03-05 公告、2024-04-26 更新，低品質與非原創搜尋結果：<https://blog.google/products-and-platforms/products/search/google-search-update-march-2024/>
- Ahrefs，〈How We Use AI for Every Article Without Making AI Slop〉：<https://ahrefs.com/blog/how-we-use-ai-without-making-ai-slop/>
- The Verge，2023-01-25，CNET AI 文章更正案例：<https://www.theverge.com/2023/1/25/23571082/cnet-ai-written-stories-errors-red-ventures>

每次引用都要保存實際 URL、日期、上下文與適用範圍；來源未提供的數字或因果關係不得補寫。
