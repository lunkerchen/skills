---
name: geolook-tw
description: >-
  Run GeoLook GEO analysis for Taiwan market. TW fork.
category: seo
---

# GeoLook TW 操作指南

GeoLook 的台灣 fork，專為繁體中文市場設計。

## 與上游差異

| 面向 | 上游 (aigclink/geolook) | GeoLook TW |
|------|------------------------|-------------|
| 市場選項 | cn / global / both | **cn / tw / global / both** |
| TW 引擎 | 無 | Gemini, ChatGPT, Claude, Grok, Perplexity（同 global） |
| 拓詞來源 | 百度下拉（CN）/ Google（global） | Google zh-TW（TW）/ Google en（global） |
| 報告語言 | 簡體中文 | **繁體中文（zh-TW）** |
| UI 語言 | 簡體中文 | 繁體中文 |
| 平台指南 | cn-platforms.md | **tw-platforms.md / tw-source-ranking.md** |
| .env.example | 含國內引擎 Key | 僅 TW/global 引擎 Key，無 CN |

## 啟動儀表板

launchd 常駐（開機自動啟動）：`http://127.0.0.1:8766`

手動啟動：
```bash
cd ~/Dev/Projects/geolook-tw
python3 scripts/geo.py ui --no-open --port 8766
```

## 常用命令

```bash
# 初始化台灣市場專案
python3 scripts/geo.py init --url https://example.com --market tw

# 全自動完整週期
python3 scripts/geo.py new --url https://example.com --market tw

# 逐步執行
python3 scripts/geo.py crawl --slug <專案>
python3 scripts/geo.py audit --slug <專案>
python3 scripts/geo.py report --slug <專案>

# 完整服務週期（已有專案）
python3 scripts/geo.py serve --slug <專案>
```

## TW 市場注意事項

1. **不需要 CN 引擎 Key**：TW 只用到 GEMINI_API_KEY、OPENAI_API_KEY、ANTHROPIC_API_KEY、XAI_API_KEY、PERPLEXITY_API_KEY
2. **問題庫用繁體中文**：台灣口語（推薦/評價/好用嗎/多少錢/地雷），不是簡轉繁
3. **外部信源參考 references/tw-platforms.md**：台灣媒體（UDN/中央社/ETtoday）、論壇（PTT/Dcard/Mobile01）
4. **初次使用建議 --no-sample 跳過採樣**，配好 Key 再補
5. **產生繁體中文報告**：report.py / deliver.py 等已全面繁體化
6. **不要在 TW 環境填入 CN 引擎 Key**，用不到且有混淆風險

## 服務管理

```bash
# 啟動/重啟
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.geolook-tw.dashboard.plist 2>/dev/null
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.geolook-tw.dashboard.plist

# 檢查狀態
launchctl list | grep geolook

# 檢查日誌
cat ~/.local/var/log/geolook-tw.err.log
cat ~/.local/var/log/geolook-tw.log
```

## 目錄結構

```
~/Dev/Projects/geolook-tw/
├── scripts/          CLI + 儀表板（全部繁體中文）
├── references/
│   ├── tw-platforms.md      台灣平台生態
│   ├── tw-source-ranking.md 台灣信源榜
│   └── ...
├── work/<slug>/     各專案資料
└── .env             引擎 Key
```

## 從報告到實作

GeoLook 產出的三份交付物（診斷報告→優化方案→執行方案）不是看看就好，要落地需要兩條並行線：

### 路線 A：官網技術改造（開發）

P0 門票問題，不解掉後面內容投入全部浪費。

| 工單類型 | 典型問題 | 驗收標準 |
|---|---|---|
| SPA 空殼頁 | 靜態 HTML 無正文（純前端渲染） | 重抓後正文詞數 ≥ 120 |
| JSON-LD | 無結構化資料 | 重抓後含 JSON-LD |
| 定義口徑 | 定義句四處不一致 | 四處文本逐字一致（人工核對） |

### 路線 B：外部陣地建設（內容+市場）

**官網只佔 AI 引用的 1.37%**（基於 18.7 萬條引用語料）— 官網是事實源不是引用源。28 個榜單站吃掉 9.1% 引用。資源有限時優先做外部渠道。

### 可抽取塊實測增益

基於 602 條 Prompt / 21,143 條引用：

| 內容特徵 | 被引用機率提升 |
|---|---|
| 含數字 | +61.6% |
| 含定義塊 | +57.3% |
| 含對比表 | +55.3% |
| 含操作步驟 | +41.2% |
| 純 Q&A 排版 | **-5.7%**（反直覺！） |

對題性（r=0.432）是最強預測因子，比權威度還高。高影響力頁面平均 1,943 詞。

### 採樣紀律

- 點名品牌的問題必須剔除（假陽性，100% 提及率）
- 別名漏配會系統性低估提及率（簡稱、英文名、俗稱都算提及）
- 中文題不打海外引擎，英文題不打國內引擎
- **採樣量可以小，口徑必須硬。寧可顯示「未測」，不編數**
- API ≠ 網頁端，兩者在報告各佔一行，絕不合併

### 內容寫作流程

1. 產出初稿（套 content-patterns 模板）
2. `stop-slop` 去 AI 味
3. 人工核實事實（LLM 只從官網抽取，抽不到標「待確認」）
4. 發到對應平台 + 留存官網備份

### 驗收自動化

每條工單帶機器可判定驗收標準。系統重抓站點 + 比對下期採樣，自動判通過/未達標。**「建議」和「服務」的分界線就是能不能自動驗收。**

### 常見問題

- **SPA 空殼頁分數低**：React/Vue SPA → P0，需加 SSR 或預渲染
- **採樣需要哪些 Key**：至少 Perplexity（聯網+引用）或 OpenAI
- **TW 和 CN 引擎不同**：TW 用 global engines，不填 CN Key
- **報告語言**：全部繁體中文
