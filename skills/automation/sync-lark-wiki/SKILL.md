---
name: sync-lark-wiki
description: 使用 `lark-cli` 與 per-user Lark OAuth 將本機 Markdown 安全同步到既有 Lark/Feishu Wiki：分階段 scope、節點盤點、revision-aware preview、明確確認後原地覆寫、read-back 與權限排錯。當使用者要求更新、同步、發布本機 Markdown 到既有 Lark Wiki，或診斷 Lark Wiki OAuth/scope/權限問題時使用；不適用於未經確認的建空間、建頁面、權限變更或匿名公開。
---

# 同步 Lark Wiki

## 目標與邊界

將本機 Markdown 視為來源，更新既有 Wiki 節點對應的 Docx 正文。預設保留既有 Wiki 結構與分享設定，不刪除、重建、搬移或改變可見性。

遵守以下邊界：

- 外部寫入前先說明來源、目標、覆寫範圍與風險，preview 後取得明確確認；說「同步」不等於已確認。
- OAuth scope、權限、空間可見性或匿名分享是額外變更，分開說明並重新確認，不隨同步一併修改。
- 「公開」≠匿名網路公開；讀回並報告實際 `visibility`／`open_sharing`，本 Skill 預設不改。
- 輸出、日誌與報告不重現 Token、open ID、Cookie、認證檔案或 access-bearing URL；文件/節點 ID 對使用者以名稱與數量回報。
- 不依賴記憶中的 space ID、node token、revision 或上次成功狀態；每次寫入前重新盤點現況。
- 缺 scope、App pending approval、節點不存在或同名歧義 → 停止，不盲目重試、不宣稱已同步。

本 Skill 只處理既有節點的正文同步。若來源頁面無法與現有節點一一對應，先報告差異並請使用者決定，不自動建立新頁面。

## 工作流程

### 1. 盤點來源

先讀取工作區的 `AGENTS.md` 與相關專案說明，確認使用者指定的來源目錄；以磁碟實際檔案為準，不只依賴 `git diff`。至少取得：

- Markdown 檔案清單、相對順序、第一個 H1 標題。
- 每檔行數與 bytes；圖片或附件依賴是否存在。
- 工作樹狀態，以及 preview 後來源是否仍未被改動。

常用檢查：

```bash
rg --files <source-dir>
wc -l -c <source-dir>/*.md
rg -n '^# ' <source-dir>/*.md
```

### 2. 檢查 CLI 與授權

```bash
command -v lark-cli && lark-cli --version
lark-cli auth status
lark-cli auth check --scope "wiki:space:retrieve wiki:space:read wiki:node:retrieve wiki:node:read docx:document:readonly"
```

既有文件正文覆寫通常還需要 `docx:document:write_only`。若缺 scope：列最小 scope 與用途、確認後才授權，完成後重跑 `auth status`／`auth check` read-back（不以畫面或舊記錄代替）。`docs` 命令固定帶 `--api-version v2`；CLI 安裝/升級不屬同步範圍。

#### 2.1 分階段串接 per-user OAuth

預設 `user` identity（bot 需明確要求，`auto` 不得靜默切換）；依階段取最小 scope（發現 → 唯讀盤點 → read-back → 覆寫），建頁面與空間設定 scope 只在使用者另外確認時才請求。每階段授權後以 `auth status` + `auth check` read-back 驗證，`auth scopes` 清單不能單獨證明可寫；Token 與認證檔案不帶回對話。分層 scope 表與 Device Flow 細節：`references/oauth-scopes.md`。

### 2.2 權限邊界

三層分開判斷：App 是否獲准該 scope → 目前 Token 是否持有且有效 → 使用者對目標 space/document 是否有實際讀寫權。`+space-list` 成功不證明可寫，dry-run 只證明請求形狀；權限結果以 API 回應與 read-back 為準。「同事可讀」≠「匿名網路可讀」，permission/visibility 變更一律另做 preview、確認與 read-back。全文判準：`references/oauth-scopes.md`「權限邊界」一節。

### 3. 重新發現目標空間與節點

先列出可存取的空間，再選擇使用者指定的正式空間；不要把測試或 public 空間當成正式目標：

```bash
lark-cli wiki +space-list --page-all --format json
lark-cli wiki +node-list --space-id <SPACE_ID> --page-all --format json
lark-cli wiki +node-list --space-id <SPACE_ID> \
  --parent-node-token <ROOT_NODE_TOKEN> --page-all --format json
```

以來源檔第一個 H1、節點 `title` 與既有階層建立 mapping。`+node-list` 同時回傳 Wiki `node_token` 與文件 `obj_token`；讀寫 Docx 正文時使用 `obj_token`，不要把 Wiki node token 誤傳給 `docs +fetch` 或 `docs +update`。

必須確認：

- 目標空間名稱唯一且符合使用者指定範圍。
- 根節點與所有子頁存在，沒有重複或錯配。
- 現有節點的 `obj_type` 是 `docx`。
- 目標空間當前的 `visibility`、`open_sharing`，以及是否已有同名頁面。

需要解析 JSON 時保留原命令 exit code、分流 stderr，不要固定刪前幾行（詳見 `references/lark-pitfalls.md`）。

### 4. 讀取遠端現況並產生 preview

每檔讀取完整正文與目前 revision：

```bash
lark-cli docs +fetch --api-version v2 \
  --doc <OBJ_TOKEN> \
  --doc-format markdown --scope full --detail simple --format json
```

preview 必含：

| 欄位 | 內容 |
| --- | --- |
| 來源 | 本機 Markdown 路徑、行數、bytes |
| 目標 | Wiki 空間、頁面名稱、對應文件 |
| 現況 | 遠端 revision、目前是否存在 |
| 動作 | `overwrite` 或停止原因 |
| 範圍 | 是否建立/刪除/移動/改分享設定，預設全部為否 |

說明 `overwrite` 會取代遠端正文並等待確認；未取得確認前只讀取與 dry-run，禁呼叫寫入 API。

### 5. 取得確認後原地覆寫

確認後立即重查來源與遠端 revision，避免 preview 期間變更；若 API 支援，用剛讀到的 revision 做衝突防護：

```bash
lark-cli docs +update --api-version v2 \
  --doc <OBJ_TOKEN> \
  --command overwrite \
  --content @<LOCAL_MARKDOWN_FILE> \
  --doc-format markdown \
  --revision-id <CURRENT_REVISION> \
  --format json
```

先 `--dry-run` 檢查請求形狀；寫入後逐頁記錄 `document_id` 與新 revision。任一頁錯誤、衝突或不明確時：

- 先 read-back 判斷是否已提交。
- 不要盲目重試同一個覆寫。
- 回報已完成與未完成的頁面，不能把部分成功說成全部完成。

### 6. Read-back 與稽核

寫入後每頁重跑完整 `docs +fetch`（不只 outline），至少驗證：

- `ok=true`、文件 ID 正確，revision 已前進或符合 API 回應。
- 新 H1 與本次更新的關鍵段落/標記存在；標題層級與非空行數大致吻合（Lark 會正規化空白，不以 bytes hash 要求相同）。
- Wiki 根節點與子頁數量、階層、標題沒有意外增減。
- 目標空間仍是原本的 `visibility` 與 `open_sharing`，本次沒有改分享權限。

報告區分四態：本機盤點、遠端寫入回應、逐頁 read-back、結構稽核；四者齊成才可宣稱同步完成。

## 失敗與停止條件

一律先停止、不盲重試、不虛報完成：App pending approval 或 `missing required scope(s)` → 列最小 scope 等確認；節點不存在/同名重複 → 要求指定目標，不自動建刪；revision 在確認後變更 → 重讀並更新 preview 重新確認；寫入結果不明 → 先 read-back 再處理；要求「公開」→ 先澄清組織內或匿名（本 Skill 不自行調 permission）。症狀對照：`references/lark-pitfalls.md`。

## 已驗證的 Lark 踩坑

高頻根因速記：`node_token` ≠ `obj_token`（文件命令只傳 obj_token）、`Found N node(s)` 摘要在 stderr（JSON 解析保留 exit code 分流）、Lark 正規化空白以標題/行數結構驗收、App pending approval 時停止不重試、permission 變更不混入正文同步。症狀對照表與大型輸出處理：`references/lark-pitfalls.md`。

## 交付格式

以簡潔繁體中文回報：來源檔數／目標頁數、各頁新 revision 或失敗原因、read-back 與結構/可見性稽核結果、有無建立/刪除/搬移/改分享設定（預設明確回報「沒有」）、本機工作樹是否被修改。不輸出 Token、認證資訊、完整遠端文件內容或 access-bearing URL。
