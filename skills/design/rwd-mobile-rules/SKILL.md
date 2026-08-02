---
name: rwd-mobile-rules
description: RWD 行動版強制規則 — 每次產出 HTML 網頁時自動套用，確保手機體驗一致、不跑版。Covers viewport rules, flex/grid mobile layouts, touch targets (44px minimum), safe area insets, responsive images, font scaling, and mobile-specific CSS patterns. Always applies to every HTML artifact. Use when building any responsive web page, especially mobile-first designs.
---

# RWD 行動版強制規則

## 觸發條件

每次生成新 HTML 頁面、修改既有 HTML、或開發 React/Vue 前端時自動套用。不論是 landing page、工具頁、儀表板、設定指南、還是 SPA 應用，只要會在任何螢幕上顯示，就用這套規則。

## 1. Viewport Meta Tag

禁止使用預設的 `initial-scale=1.0` 裸標籤。必須使用：

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=5.0">
```

- `minimum-scale=1.0` — 使用者不能縮小，版面維持 100%
- `maximum-scale=5.0` — 可以放大到 5 倍，需要看細節沒問題

## 2. 水平滑動鎖定

在 `<html>` 和 `<body>` CSS 都要加上：

```css
html {
  overflow-x: hidden;
  max-width: 100vw;
}
body {
  overflow-x: hidden;
  touch-action: pan-y;  /* 只允許垂直滑動，水平手勢被瀏覽器忽略 */
}
```

- `overflow-x:hidden` — 防止內容超出造成橫向捲軸
- `max-width:100vw` — 根元素不超出版心
- `touch-action:pan-y` — 觸控只允許垂直，避免左右滑動跑版

## 3. Container 寬度

| 項目 | 值 |
|------|-----|
| max-width | **1400px**（不要用 1080px 或 1100px，寬螢幕會太窄） |
| padding | **0 40px** 或 **0 48px**（不要小於 24px） |

螢幕 ≤ 768px 時 padding 可降至 20px。

## 4. 網格 RWD 斷點

所有 `grid-template-columns` 必須有行動版覆寫。三層斷點：

| 斷點 | 規則 |
|------|------|
| **≤768px** | 5 欄 → 2 欄、4 欄 → 2 欄、3 欄 → 1 欄、2 欄 → 1 欄 |
| **≤480px** | 5 欄 → 1 欄、4 欄 → 1 欄 |

**注意：inline style 的 grid 不會被 CSS class media query 覆寫。**
解法：在 @media 中使用 `!important` 加屬性選擇器：

```css
@media(max-width:768px) {
  div[style*="grid-template-columns:repeat(5,1fr)"]{grid-template-columns:repeat(2,1fr)!important}
  div[style*="grid-template-columns:repeat(4,1fr)"]{grid-template-columns:repeat(2,1fr)!important}
  div[style*="grid-template-columns:repeat(3,1fr)"]{grid-template-columns:1fr!important}
  div[style*="grid-template-columns:repeat(2,1fr)"]{grid-template-columns:1fr!important}
}
@media(max-width:480px) {
  div[style*="grid-template-columns:repeat(5,1fr)"]{grid-template-columns:1fr!important}
  div[style*="grid-template-columns:repeat(4,1fr)"]{grid-template-columns:1fr!important}
}
```

## 5. 卡片文字溢出

所有卡片容器（`.glass-card`、`.zine-card`、`.sticky`、`.module-card` 等）必須加上：

```css
overflow-wrap: break-word;
word-wrap: break-word;
```

防止長文字在小螢幕上超出卡片邊界。

## 6. 禁止 grid-column:span

**不要使用 `grid-column:span N`**，特別是在 `auto-fill` / `auto-fit` 的動態網格中。

原因：當網格在行動版折成 1 欄時，`span 2` 或 `span 3` 會讓元素超出或無法正確換行。

替代方案：
- 需要橫跨全寬時使用 `grid-column: 1 / -1`
- 不需要橫跨時直接移除 span，讓 auto-fill 自然排列

## 7. Nav 響應式

導覽列在 ≤768px 必須：
- 隱藏連結列表，顯示 hamburger 按鈕
- 選單打開時占滿螢幕寬度，垂直排列
- backdrop-filter 模糊背景

Nav inner max-width 與 container 一致（1400px）。

### HTML 結構

```html
<nav class="sticky-nav" id="stickyNav">
  <div class="container">
    <button class="hamburger" id="hamburgerBtn" aria-label="選單">☰</button>
    <div class="nav-links" id="navLinks">
      <a href="#step1">01. 安裝</a>
      <a href="#step2">02. 取 Key</a>
      <!-- ... -->
    </div>
  </div>
</nav>
```

`hamburger` 按鈕只能用 `display:none` 隱藏（不能用 `visibility` 或移除 DOM），這樣螢幕閱讀器和 tab 導航在桌面版不會看到它。

### CSS

```css
.hamburger {
  display: none;  /* 桌面版隱藏 */
  width: 32px; height: 32px;
  align-items: center; justify-content: center;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text-muted);
  font-size: 18px; cursor: pointer;
  flex-shrink: 0;
}
@media (max-width: 768px) {
  .hamburger { display: flex; }
  .nav-links { display: none; }
  .nav-links.open { display: flex !important; flex-direction: column; }
}
```

### JavaScript Toggle（選一）

**方法 A — 純 JS（推薦，無依賴）：**
```javascript
document.getElementById('hamburgerBtn')?.addEventListener('click', () => {
  document.getElementById('navLinks').classList.toggle('open');
});
```

**方法 B — 點 hamburger 以外區域關閉（進階）：**
```javascript
const nav = document.getElementById('stickyNav');
document.addEventListener('click', (e) => {
  const isOpen = document.getElementById('navLinks').classList.contains('open');
  if (isOpen && !nav.contains(e.target)) {
    document.getElementById('navLinks').classList.remove('open');
  }
});
```

在現有的 `</body>` 前的 `<script>` 區塊內插入即可。

### ⚠️ 常見陷阱

- **只寫 CSS 沒寫 JS → hamburger 不會動。** CSS 只是樣式，`.open` class 需要 JS 來 toggle。修改既有 HTML 頁面時，務必確認 `<button class="hamburger">` 已存在於 nav 中，且 JS toggle 程式碼已加入。
- **現有的水平滾動 nav 可以留著作為 fallback**，不需要移除。設定 `nav-links { overflow-x: auto; scrollbar-width: none; }` 讓桌面版保持水平排列。
- 不要把 `.hamburger` 設為 `visibility:hidden` — 用 `display:none` 確保它不佔空間也不會被 tab 導航到。

## 8. 快速檢查清單

產出 HTML 後檢查這幾項：

- [ ] viewport 有 `minimum-scale=1.0, maximum-scale=5.0`
- [ ] html/body 有 `overflow-x:hidden`
- [ ] body 有 `touch-action:pan-y`
- [ ] container max-width ≥ 1280px（推薦 1400px）
- [ ] 所有 inline grid 在 @media 中有 `!important` 覆寫
- [ ] 所有卡片有 `overflow-wrap:break-word`
- [ ] 無 `grid-column:span N`（改用 `1/-1` 或移除）
- [ ] hamburger 按鈕 HTML 元素存在 + JS toggle 已加入（不只 CSS）
- [ ] 表格有 `overflow-x:auto` 包裝

---

## 9. Tailwind / React 專案 RWD 規則（取代上方 1-7）

當專案使用 **React + Tailwind CSS**（非單檔案 HTML）時，上方 1-7 節不適用。改用以下 Tailwind 原生模式：

### 9.1 Navbar 行動版選單

使用 React state 控制 hamburger 開關，而非 CSS class toggle：

```tsx
const [menuOpen, setMenuOpen] = useState(false)

// Desktop: hidden md:flex — 桌面顯示完整連結
// Mobile: md:hidden — hamburger 按鈕
// Dropdown: md:hidden — 垂直排列選單
```

**結構要點：**
- Desktop nav 用 `hidden md:flex` 隱藏/顯示
- Hamburger 按鈕用 `md:hidden` 只在手機出現
- Dropdown menu 用 `md:hidden` + React state toggle
- 每個連結點擊後關閉 menu（`onClick={close}`）
- 關閉時 return 到桌面版 view

### 9.2 Container 與間距

```tsx
// 不要用固定 px container — 用 Tailwind utility classes
<div className="max-w-7xl mx-auto px-4">
  // ← sm:px-6 / lg:px-8 非必需，px-4 在手機足夠
```

手機端 padding 保持 `px-4`（16px），桌面端不需要特別加大，`max-w-7xl` 自動居中。

### 9.3 Grid 響應式

Tailwind 的 responsive prefixes 直接處理斷點，不需要 `!important`：

```tsx
// 手機 2 欄 → 平板 3 欄 → 桌面 4 欄
<div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-4">

// 手機 1 欄 → 桌面 2 欄（詳情頁）
<div className="grid md:grid-cols-2 gap-6 sm:gap-8">
```

**規則：**
- 不寫 base class 時 Tailwind 預設 mobile-first（`grid-cols-2` 在手機生效）
- `md:` 斷點是 768px、`lg:` 是 1024px
- `gap` 在手機用小值（`gap-3`），桌面用 `sm:gap-4` 加大

### 9.4 表單篩選列（Explore / Search）

篩選元件手機端需要垂直堆疊：

```tsx
// 手機垂直堆疊 → 桌面水平排列
<div className="flex flex-col sm:flex-row sm:flex-wrap gap-3 mb-6">
  <select className="w-full sm:w-auto border rounded-lg px-3 py-2 text-sm" />
  <input className="w-full sm:flex-1 border rounded-lg px-3 py-2 text-sm" />
</div>
```

- `w-full sm:w-auto` — 手機全寬、桌面 auto
- `sm:flex-row` — 桌面才水平排列
- `sm:flex-1` — 搜尋框桌面自動拉伸

### 9.5 文字大小遞減

手機端文字比桌面小一號：

```tsx
<h1 className="text-xl sm:text-2xl font-bold">    // 手機 XL、桌面 2XL
<p className="text-xs sm:text-sm text-gray-500" /> // 手機 XS、桌面 SM
<p className="text-2xl sm:text-3xl font-bold" />   // 價格
```

### 9.6 Hero 區塊（Landing Page）

按鈕在手機垂直、桌面水平：

```tsx
<div className="flex flex-col sm:flex-row gap-3 justify-center">
  <Link className="... text-center">按鈕</Link>
</div>
```

- `flex-col sm:flex-row` — 手機垂直、桌面水平
- `text-center` — 手機按鈕文字置中
- hero padding 從 `py-20` 降為 `py-16 sm:py-20`

### 9.7 圖片縮圖列

手機縮小縮圖、防止換行壓縮：

```tsx
<div className="flex gap-2 overflow-x-auto pb-1">
  {images.map(img => (
    <img className="w-16 sm:w-20 h-16 sm:h-20 object-cover rounded-lg shrink-0" />
  ))}
</div>
```

- `shrink-0` — 防止 flex 壓縮圖片
- `overflow-x-auto` — 允許橫向滑動
- `pb-1` — 隱藏滾動條裁切（scrollbar 空間）

### 9.8 聊天室（列表 / 對話切換）

手機端：顯示列表或聊天室，不可同時顯示。桌面端：並排（2/3 聊天 + 1/3 列表）。

```tsx
// 列表：手機有 active conversation 時隱藏
<div className={`${activeConv ? 'hidden' : ''} md:block`}>

// 聊天室：手機沒選對話時隱藏
<div className={`${!activeConv ? 'hidden md:flex' : 'flex'}`}>

// 返回按鈕（手機限定）
{activeConv && <button onClick={() => setActiveConv(null)}
  className="md:hidden text-sm text-blue-600">← 返回對話列表</button>}
```

### 9.9 表格（Admin 後台）

Table 元件手機端需要 horizontal scroll + min-width：

```tsx
<div className="overflow-x-auto">
  <table className="w-full text-sm min-w-[600px]">
    {/* ... */}
  </table>
</div>
```

Tab 按鈕也要可橫向滑動：

```tsx
<div className="flex gap-2 overflow-x-auto pb-1">
  {tabs.map(t => (
    <button className="shrink-0 px-4 py-2 rounded-lg text-sm" />
  ))}
</div>
```

- `overflow-x-auto` — 允許橫向滑動
- `min-w-[600px]` — table 不被壓縮，保留欄位可讀性
- `shrink-0` — 防止 tab 按鈕被壓扁
