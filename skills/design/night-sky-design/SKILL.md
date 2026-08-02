---
name: night-sky-design
description: 夜空風格單檔 HTML — 簡報或網頁。深色星空+品牌漸層。
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [html, design, deck, presentation, landing, brand-gradient, dark-theme]
    category: design
    related_skills: [html-artifact, rwd-mobile-rules, popular-web-designs]
---

# Night Sky Design Skill

夜空風格單檔 HTML 設計系統。深色夜空背景 + 星星 + 品牌漸層 accent，
可輸出兩種形態：**deck**（全螢幕投影片，鍵盤導航）或 **page**（一般捲動網頁）。

源自企業品牌簡報專案。

## When to Use

- 使用者要「好看的簡報 / deck / 提案」且接受深色系
- 使用者要深色科技感 / 星空感的網頁（landing、說明頁、報告）
- 有品牌色漸層可抓（`curl` logo SVG 找 `<linearGradient>` stop 色）
- 需單檔自包含、離線可開、無外部依賴的 HTML

## Prerequisites

- 品牌漸層色：`curl -s <logo.svg-url>` 找 `<stop offset stop-color>`，取 2-3 色
- 無品牌色時用預設漸層 `#73c8e5 → #d8bad8 → #e6398d`

## 兩種模式

| 模式 | 用途 | 檔案 | 結構 |
|------|------|------|------|
| `deck` | 投影片簡報（方向鍵/點擊導航） | `templates/deck.html` | 11 張以內，每張 `.slide` 全螢幕 |
| `page` | 一般捲動網頁 | `templates/page.html` | `.section` 區塊，可長捲動 |

## Procedure

1. **抓品牌色**：有 logo 就先 `curl` 抓漸層色；沒有就用預設或問使用者主色
2. **選模式**：要翻頁簡報 → deck；要捲動網頁 → page
3. **載入模板**：`skill_view(name="night-sky-design", file_path="templates/deck.html")`（或 page）
4. **改 `:root` token**：把 `--sky / --lav / --pink` 換成品牌色；`--grad` 會自動跟
5. **填內容**：deck 每張 slide 一個 `<section class="slide">`；page 用 `.section` + 卡片
6. **RWD 套用**：viewport 用 `minimum-scale=1.0, maximum-scale=5.0`；卡片要 `overflow-wrap: break-word`；表格包 `overflow-x:auto`；`@media(max-width:860px)` 折疊
7. **驗證**（強制，見 Verification）

## 設計系統

### Token（模板已含，改色即可）

```css
:root {
  --night-0: #070B16;   /* 夜空最深 */
  --night-1: #0B1120;   /* 夜空主色 */
  --night-2: #101A30;   /* 夜空漸層底 */
  --panel: rgba(16,26,48,.66);          /* glass 卡片 */
  --line: rgba(203,213,225,.14);        /* 細邊框 */
  --title: #e2e8f0;     /* 標題色（固定，別改） */
  --label: #cbd5e1;     /* 內文色（固定，別改） */
  --muted: #8494ad;     /* 次要文字 */
  --sky: #73c8e5;       /* 品牌漸層第 1 色 ← 改這裡 */
  --lav: #d8bad8;       /* 品牌漸層第 2 色 ← 改這裡 */
  --pink: #e6398d;      /* 品牌漸層第 3 色 + accent ← 改這裡 */
  --grad: linear-gradient(100deg, var(--sky), var(--lav), var(--pink));
}
```

### 語義色

- `--pink`（品牌 accent）＝ 焦點 / P0 / 高亮 / 導覽點 active
- `--gold #f4c98d` ＝ KPI 數字 / 產品化機會標記
- `--olive #9fc77a` ＝ 成功 / 正面（表格 tick、P2 標籤）
- `--rust #ff6b6b` ＝ 錯誤 / 負面
- `--sky` ＝ 一般強調 / 標籤邊框 / timeline 起點

### 字體三層

- `--serif`（Songti TC / Georgia）→ h1-h3 標題，`text-shadow` 一定要
- `--sans`（system-ui / PingFang TC）→ 內文
- `--mono`（SF Mono / Menlo）→ eyebrow / 標籤 / KPI / 頁碼

### 夜空背景（兩個 fixed div）

```html
<div class="sky"></div>   <!-- 品牌色 radial-gradient 光暈 + 夜空漸層 -->
<div class="stars"></div> <!-- 星星 = 多個 radial-gradient 點 -->
```

CSS 見模板，直接複製。星星密度/位置可調 background-image 的百分比。

### 常用元件

- `.card` — glass 卡片（hover 上浮 2px）
- `.card.hot` — 品牌色強調卡（P0 / 重點）
- `.dept` — 部門條（左標籤 + 右內容，移動版折疊成單欄）
- `.tag.p0/.p1/.p2` — 優先級標籤
- `.timeline .tl-item` — 時間軸（`::before` 垂直 rail + 圓點，`.live` 發光）
- `.quote` — 粉紅左框引文
- `.check-list` — 勾選清單（CSS 畫勾）
- `.table-wrap` — 表格（必包，防移動版爆版）
- `.pill` — 藥丸標籤

## Pitfalls

- **標題必須有 `text-shadow`** — 夜空深底上無陰影的標題會發虛。`text-shadow: 0 1px 24px rgba(226,232,240,.18)`
- **背景 `pointer-events: none`** — `.sky` / `.stars` 是 fixed 全螢幕，沒設會擋所有點擊
- **`--title / --label` 別改成品牌色** — 品牌色只做 accent，文字色固定 `#e2e8f0 / #cbd5e1`，否則對比崩壞
- **deck 模式必須有無 JS fallback** — 沒 JS 時 `.slide` 垂直堆疊可捲動（body 不加 `deck-mode` class 即可）
- **`.slide` 用 `min-height: 100vh`** 不是 `height`，避免內容超長被裁
- **移動版 `grid-template-columns` 要覆寫** — 4/3 欄 → 1 欄，用 media query（不要用 `grid-column: span`）
- **RWD viewport**：禁止裸 `initial-scale=1.0`，要 `minimum-scale=1.0, maximum-scale=5.0`
- **色弱安全**：不要只靠顏色傳達（優先級標籤要有 P0/P1/P2 文字，不只顏色）

## Verification

強制視覺驗證循環（deck 尤其，導航/隱藏邏輯容易出錯）：

1. `browser_navigate(url="file://<絕對路徑>")`
2. `browser_console` 執行：
   ```js
   JSON.stringify({
     deckMode: document.body.classList.contains('deck-mode'),
     activeSlide: document.querySelector('.slide.active')?.dataset.title,
     visibleSlides: [...document.querySelectorAll('.slide')].filter(s => s.offsetParent !== null).length,
     totalSlides: document.querySelectorAll('.slide').length,
     horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
   })
   ```
   deck 期望：`deckMode:true, visibleSlides:1, horizontalOverflow:false`
3. 逐張翻頁（dispatch KeyboardEvent 或 `browser_click`）確認每張內容 `offsetParent !== null`
4. 確認無 JS 時可讀：移除 `<script>` 檢查頁面仍垂直排列顯示全部內容
5. 修到乾淨為止

## 快速檢查清單

- [ ] 品牌漸層已替換（`--sky/--lav/--pink`）
- [ ] 標題有 text-shadow
- [ ] `.sky/.stars` 有 `pointer-events:none`
- [ ] viewport 有 `minimum-scale=1.0, maximum-scale=5.0`
- [ ] 所有卡片有 `overflow-wrap:break-word`
- [ ] 表格包在 `.table-wrap`（`overflow-x:auto`）
- [ ] 移動版 grid 折疊成 1 欄
- [ ] deck 模式無 JS fallback 正常
- [ ] 視覺驗證循環已跑、無水平溢出
