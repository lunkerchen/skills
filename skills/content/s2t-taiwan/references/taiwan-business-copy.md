# Taiwan Business/Marketing Copy Conversion (China → Taiwan)

Worked example: rewriting 8 FDE (Forward Deployed Engineer) infographic cards from
Xiaohongshu-style Chinese marketing copy into Taiwan Traditional Chinese typeset copy.
Source: 2026-08 session rewriting 8 image cards (暖白/深海軍藍/金黃 editorial style).

## Golden rule

China business copy favors verbs like 落地/上線 as punchy closing lines; Taiwan
prefers the same punch but with 導入 (adoption) or 實際上線 (going live). Keep the
rhetorical structure (主標 → 引言 → 卡片 → 金句), translate the *tone*, not just chars.

## Conversion set used (beyond character-level s2t)

| Source | Taiwan | Context |
|---|---|---|
| 落地 | 導入 | "輸在落地" → "輸在導入"; "落地能力" → "導入能力" |
| 落不了地 | 導入不了 | "項目總落不了地" → "專案總導入不了" |
| 員工 | 團隊成員 | "員工不願用" → "團隊成員不願用" |
| 演示 | 示範 | "只會演示" → "只會示範"; "演示｜方案｜PPT" → "示範｜方案｜簡報" |
| 接口 | 介面 | "調接口" → "串接介面" |
| 寫代碼 | 寫程式 | keep 程式碼 if noun form |
| 數據 | 資料 | business copy ("接數據" → "接資料"); stats contexts keep 數據 |
| 算法 | 演算法 | |
| 項目 | 專案 | |
| 合同 | 合約 | "贏得合同" → "贏得合約" |
| 口徑不一 | 標準不一 | |
| 最後一公里 | 最後一哩路 | |
| 前線/駐紮 | 第一線/進駐 | "駐紮在客戶一線" → "進駐客戶第一線" |
| 鴻溝 | 落差 | "填補產品能力和客戶需求之間的鴻溝" → "落差" |
| 反哺 | 回饋 | "反哺產品" → "回饋產品" |
| 主人翁意識 | 當責意識 | |
| 合規 | 法規遵循 | |
| 頭銜 | 職稱 | |
| 業務一線 | 業務第一線 | |

## Verification pitfalls hit live

- `台` in 台灣: OpenCC s2t flags it (→臺) but it's the standard Taiwan spelling — false positive.
- `只` in 不只/只是: flags as 隻 — false positive (隻 is only the measure word).
- `看`: identical in both scripts — false positive.
- File read: OCR/txt sources may be flagged binary by read_file (UTF-16-ish BOM or stray bytes);
  read via `iconv -f UTF-16LE -t UTF-8` or terminal `cat` fallback before giving up.

## Locating "user-provided images" not in context

When a delegated task references attached images/cards that aren't in the agent's context:
1. `session_search` the parent session (look for the task phrase, e.g. "八張圖文繁中重製").
2. Parent session tool calls usually reveal the source dir (e.g.
   `$IG_SOURCE_DIR/素材/xiaohongshu-<id>/`) containing
   `image-01..08.jpg`, `ocr.txt`, `ocr-zh-Hant.txt`, `caption.txt`.
3. OCR text files already exist there — reuse them instead of re-OCR'ing.
