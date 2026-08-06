---
name: obsidian-vault-organizer
description: Use when organizing or restructuring an Obsidian vault.
---

# Obsidian Vault Organizer

將混亂的 Obsidian vault 整理成可搜尋、可連結、可長期維護的知識系統。核心流程是：只讀盤點 → 提案 → 人工批准 → 小批次執行 → 驗證。

## 核心原則

- 先讀後寫；先分析後改動。
- 不把使用者的 vault 直接套成通用 PARA、Zettelkasten 或其他框架；由現有內容反推最小可行架構。
- 不刪除原始內容，不猜測筆記意義，不為了增加數量建立無意義連結。
- 不確定的分類、合併、刪除、重命名一律列為人工確認。
- 資料夾表達筆記目前的角色；tags / properties 表達主題、狀態或 metadata，避免重複表達。
- 使用 `[[wikilinks]]` 連接 vault 內的筆記；外部來源使用 Markdown URL。
- 重要永久筆記通常至少有兩個有意義的 wikilinks；找不到實質關係時不要硬加。
- 每個筆記以一個主要概念或目的為中心。
- 每次批次操作都留下可回溯的變更紀錄。

## Phase 0：確認範圍與安全條件

在讀取 vault 前確認：

1. vault 絕對路徑或目前可存取的工作目錄。
2. 是否允許讀取全部內容，或只允許特定資料夾。
3. 是否已有 Git、Time Machine、雲端版本或其他可還原備份。
4. 使用者希望只產生建議，還是批准後實際修改。

若使用者沒有明確批准修改，預設為只讀模式。

## Phase 1：只讀盤點

讀取並報告：

- 主要資料夾、用途與檔案數量。
- 常見主題與內容類型。
- 重複或高度相似筆記。
- 空白、過短、未完成、暫存或疑似過時筆記。
- 沒有 wikilink 的孤立筆記。
- 斷掉的 wikilink。
- 檔名、資料夾、tags、frontmatter / properties 的不一致。
- 可能屬於 capture、永久知識、MOC、專案、資源、每日筆記或封存的內容。

不要在此階段移動、刪除、重命名或改寫檔案。

## Phase 2：提出 vault 架構與規則

根據盤點結果提出最簡單的架構。可考慮，但不可盲套：

```text
00-CAPTURE       尚未整理的快速輸入
01-PERMANENT     已消化、可長期引用的知識
02-MAPS          主題索引與 Map of Content
03-PROJECTS      進行中的專案
04-RESOURCES     外部資料與參考文件
05-INTELLIGENCE  綜合、連結、分析報告
06-DAILY         每日筆記
07-ARCHIVE       已完成或不再活躍的內容
08-SYSTEM        模板與 vault 規則
```

若建議不同架構，說明它如何對應現有內容，以及為什麼比上述架構更簡單。

同時提出：

- 資料夾與檔名規則。
- Properties 欄位與資料型別。
- tags 的命名與階層規則。
- 何時建立獨立筆記、何時保留在原筆記。
- 何時建立 MOC。
- 重複筆記的處理規則。
- 專案結束後的封存規則。
- wikilink 的品質標準。

## Phase 3：產生待批准的整理計畫

將筆記分為：

- 可批次處理。
- 需要人工判斷。
- 建議保留原樣。
- 建議封存。
- 疑似重複、可能合併。
- 有資料遺失或語意誤判風險。

產出以下報告，等待使用者批准：

1. 建議 vault 架構。
2. 分類、命名、Properties、tags、連結規則。
3. 模板草案。
4. 筆記移動 / 重命名 / 合併對照表。
5. 風險與人工確認清單。
6. 分批執行順序。

不得將「提出建議」視為「批准修改」。

## Phase 4：批准後安全執行

只有使用者明確批准後才修改 vault。執行順序：

1. 確認備份或可還原版本。
2. 建立已批准的資料夾與模板。
3. 先處理分類最明確的筆記。
4. 分批移動與重命名；每批完成後停止並回報。
5. 統一已批准的 Properties / frontmatter。
6. 只補上有實質關係的 wikilinks。
7. 建立必要的 MOC。
8. 將已完成或過時內容移到 Archive。
9. 對不確定項目保留原狀並列入人工清單。
10. 產生變更紀錄。

不要覆寫原始內容，除非使用者明確批准；不要把未列入計畫的檔案順手重構。

## Phase 5：驗證

修改後必須檢查：

- 所有原始筆記是否仍可找到。
- 是否有斷掉的 wikilinks。
- 是否有重複檔名或無效路徑。
- Properties / frontmatter 是否格式一致、型別正確。
- 是否仍有空白筆記與孤立筆記。
- 新增 wikilinks 是否具有實質關係。
- Obsidian 是否能正常開啟與渲染 Markdown。
- 移動、重命名、合併、修改的檔案是否都有紀錄。

## 建議模板欄位

只在 vault 實際需要時採用，不要為了完整而增加欄位。

### 快速捕捉

```markdown
---
type: capture
created: YYYY-MM-DD
status: unprocessed
---

# 標題

IDEA:

CONNECTS TO:

MIGHT USE FOR:
```

### 永久知識

```markdown
---
type: permanent
created: YYYY-MM-DD
tags: []
---

# 標題

## 核心理解

## 為什麼重要

## 關鍵張力

## Connections
- [[相關筆記]] — 具體連結原因

## 來源
```

### Map of Content

```markdown
---
type: map
topic:
updated: YYYY-MM-DD
---

# 主題 — Map of Content

## 核心問題

## 基礎筆記

## 複雜性與衝突

## 應用

## 未解問題

## 相關 Maps
```

### 每日筆記

```markdown
---
date: YYYY-MM-DD
type: daily
---

# YYYY-MM-DD

## Captures

## Done

## Notes

## Tomorrow
```

## 回報格式

每次執行或驗證後，用以下結構回報：

```markdown
# Obsidian Vault 整理報告

## 狀態
- 模式：只讀盤點 / 計畫 / 執行 / 驗證
- 範圍：
- 是否有備份：

## 已完成
-
## 變更
- 移動：
- 重命名：
- 修改：
- 新增連結：
- 新增 MOC：

## 未處理
-
## 需要人工確認
-
## 驗證結果
- 原始內容仍存在：PASS / FAIL
- 斷鏈檢查：PASS / FAIL
- Properties 檢查：PASS / FAIL
- 重複與孤立筆記檢查：PASS / FAIL

## 下一批
-
```

## 常見錯誤

- 直接把所有筆記按關鍵字丟進資料夾，卻沒有理解筆記目的。
- 用 tags 取代資料夾，或讓資料夾與 tags 重複描述同一件事。
- 為了讓 Graph View 好看而大量互連。
- 自動合併只有部分相似的筆記，導致觀點或來源遺失。
- 先批量改檔名，後續才發現 wikilink 已經斷掉。
- 沒有備份就執行跨檔案移動或合併。
- 把 AI 的整理報告混在永久知識筆記裡，造成來源與推論混淆。
- 一次處理整個 vault，失去錯誤隔離與回滾能力。

## 完成標準

只有同時符合以下條件才算完成：

- vault 架構有明確用途且沒有不必要的層級。
- 重要筆記可透過資料夾、Properties、搜尋與 wikilinks 找到。
- 原始內容可回溯，沒有未批准的刪除或合併。
- 斷鏈與格式問題已驗證，或已列出明確剩餘項目。
- 每個未確定判斷都已交給人工確認。
- 變更紀錄足以讓使用者理解並回復本次整理。