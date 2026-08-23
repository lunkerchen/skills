## Use

當你貼上文章內容或提供本地檔案路徑，要求做 GEO/AI 搜索友好化改造時觸發。

**輸入類型自動辨識**：
- **長文**（>800 字，vocus/blog/YouTube→文章）→ 跑完整 12 維度
- **短文**（<800 字，Threads/FB 貼文）→ 僅優化標題+關鍵句+來源標註，不硬塞結構
- **影片腳本**（口播稿/Short 腳本）→ 僅做語義密度與關鍵實體展開，保留口語節奏

**不適用**：從零寫新文章、編造數據/引用、合規審計、排名保證、**Web 應用（網站/平台）的 GEO 優化**（見下方替代方案）。

> **⚠ 不是這份 skill 的任務？**
> - 如果是 **Web 應用／平台網站**（電商、C2C 市集、工具型網站）的 GEO 優化（結構化資料、schema markup、首頁內容、robots.txt/sitemap），請載入 `webapp-geo-optimization`。
> - 如果是 **完整 SEO+GEO 策略規劃**（主題地圖、fan-out query、站外權威），請載入 `modern-seo-strategy`。
> - 如果是純文章改造，就是你正在讀的 `geo-article-friendly` — 繼續。

## Required Reading

執行前載入：
- `skill_view(name='geo-article-friendly', file_path='references/geo-article-transformation-method.md')` — 權重表與改造規則
- `references/geo-output-contract.md` — 輸出模板

## Workflow

### Phase 0：頻道語氣偵測

改造前先確認這篇的語氣歸屬。從原文內容判斷，必要時問你一句：

| 語氣 | 特徵 | 改造限制 |
|------|------|----------|
| **股癌 tone** | 直接、口語、自嘲、數字感、sometimes 粗口 | 保留口語節奏，不套用正式論文結構 |
| **攝影專業** | 技術細節、設備參數、拍攝經驗 | 保留技術精確度，補充來源時以 industry report 為優先 |
| **冷知識/知識型** | 輕鬆但扎實、故事性開頭 | 保留故事鉤子，結構可適度強化 |
| **一般內容** | 無明顯 tone | 標準改造 |

### Phase 1：輸入解析與原文盤點

1. 確認輸入（貼上文字或檔案路徑 + `.md` `.txt` `.html` `.docx` `.pdf`），檔案無法讀取回報 blocker
2. 預設深度：長文=`standard`、短文=`light`、腳本=`light`
3. 建立原文清單：核心論點、既有證據、語氣特徵、結構現狀

### Phase 2：GEO 差距診斷（依類型調整）

對照 12 維度權重表。但**短文與腳本只評估前 5 項**（證據+結構+流暢+語義+權威），跳過專業術語/魯棒性/跨域連接/易懂表達。

### Phase 3：權重驅動改造

按優先級執行。每項改造時問自己：「這會洗掉 the user's voice嗎？」→ 會的話就節制。

**證據引用層（43%）**
- 原文有專家觀點但沒原話 → `[建議補充原文引語：...]`
- 原文有數字但沒口徑 → `[建議補充數據口徑：...]`
- 原文有主張但沒來源 → `[建議補充來源：...]`
- 嚴禁編造任何數據、引用、研究名稱、百分比

**結構規範性（12%）**
- 長文：加 H1/H2/H3 層級 + 3-5 條核心摘要 + 結論 + FAQ
- 短文：最多加 1 層標題 + 1 句摘要，不硬塞結構
- 口播腳本：不動原始結構，僅加段落註解

**表達與語義（10%+8%）**
- 展開重要實體（公司名/產品名/人名首次出現給 context）
- 圍繞真實問題組織（「為什麼...」「如何...」）
- 不為覆蓋率做關鍵詞堆砌

**權威/術語/魯棒性/跨域（剩餘 27%）**
- 長文完整跑，短文跳過
- deep 模式允許 web_search 查證外部來源再補充

### Phase 4：產出與驗證

回傳輸出（格式見 reference），但短文/腳本可跳過評分表，只給改造後版本 + 1 段改造摘要。

**驗證**：
- 原文核心主張保留 ✓
- 語氣未被洗掉 ✓（與 Phase 0 對照）
- 無編造 ✓
- 前 5 項有實質改善 ✓
- 改造後建議跑 `stop-slop` 確保不去 AI 味 ✓

## Evidence Discipline

- `原文支持` — 原文直接有的資訊
- `外部已核驗` — 你透過 web_search 查證過的（僅 deep 模式）
- `建議補充` — 原文無此資訊但你推斷該有的

禁止：編造研究名稱、虛構百分比、樣本量、報告日期、引用或機構。

## 整合建議

改造完成後，在結尾附上：

```
▶ 下一步建議
- [stop-slop] 跑一次去除 AI 寫作味
- [vocus-article-writing-sop] 如果這篇要發方格子
- [modern-seo-strategy] 參考完整 SEO+GEO 整合策略
- 適合發布頻道：[判斷]
```

## 姚金剛 GEO 生態資源

本 skill 方法論源自姚金剛（@yaojingang）開源的 GEO 知識體系。深度使用時可參考：

- **GEOFlow**（2.7k ⭐）：完整 GEO 內容工程與多站點分發系統，PHP/PostgreSQL/Docker。`github.com/yaojingang/GEOFlow`
- **yao-geo-skills**（468 ⭐）：20 個 GEO skill，含內容生產、診斷、歸因追蹤、GEOFlow 運營。`github.com/yaojingang/yao-geo-skills`
- **yao-meta-skill**（1.6k ⭐）：Skill OS 框架，用於創建/評估/打包可復用 Agent Skill。`github.com/yaojingang/yao-meta-skill`
- **GEO 測量框架論文**：《From Citation Selection to Citation Absorption》— 跨平台 GEO 效果測量方法

**注意：vocus-article-writing-sop v1.2.0+ 已內建 GEO 證據規則**（數據口徑、inline 來源、實體展開）。若文章是用 vocus-sop 從零寫成而非改寫既有素材，GEO 差距通常很小 — 跳過完整改造，直接跑 stop-slop 即可。

**策略層面**：如需完整 SEO+GEO 策略規劃（主題地圖、fan-out query 優化、站外權威建立），載入 `modern-seo-strategy` skill。

## Reference Map

- `references/geo-article-transformation-method.md`：方法 + 權重表 + 改造規則
- `references/yao-geo-transformation-methodology.md`：姚金剛 10 項改造任務完整操作細節 + 對應權重 + 改造範例
- `references/geo-output-contract.md`：5 項輸出模板
- `references/case-study-adobe-topaz.md`：實際案例（Adobe 收購 Topaz 改造前後對照 + 字數變化）

## Pipeline 順序

GEO 改造完成後，再接 `stop-slop` 去 AI 味。**不要反過來**——stop-slop 在前會把 GEO 加的證據標註也當 AI 味砍掉。實測：一篇 6,300 字長文，GEO 擴至 9,028 字，stop-slop 縮回 7,632 字（-16%），資訊密度不減反增。

**發方格子的完整管線**（GEO → 貼上 → 發布）：

```text
1. GEO 改造（geo-article-friendly）
2. stop-slop 去 AI 味
3. 清除 markdown 記號 + YAML frontmatter
4. 壓縮空白行（\n\n+ → \n）— 避免 Lexical 編輯器產生過多空段落
5. 刪除尾部「來源：」等 footer 行
6. pbcopy + Cmd+V 貼入方格子的 Lexical 編輯器
7. 走發布流程（vocus-publish-flow.md 參考）
```

步驟 4 是關鍵坑點：Lexical 把每個 `\n\n` 轉成一個空 `<p>`，原始有雙換行 → 貼上後會變三行空白。一次 `\n\n+ → \n` 即可解決。
