---
name: sync-lark-wiki
description: 使用 `lark-cli` 與 per-user Lark OAuth 將本機 Markdown 安全同步到既有的 Lark/Feishu Wiki，包含分階段 scope 授權、空間與節點盤點、revision-aware preview、外部寫入前的明確確認、原地覆寫、read-back、權限排錯與結構/可見性稽核。當使用者要求更新、同步、刷新或發布本機 Markdown 到既有 Lark Wiki，或需要診斷 Lark Wiki OAuth/scope/權限問題時使用；不適用於未經另外確認的建空間、建頁面、權限變更或匿名公開。
---

# 同步 Lark Wiki

## 目標與邊界

將本機 Markdown 視為來源，更新既有 Wiki 節點對應的 Docx 正文。預設保留既有 Wiki 結構與分享設定，不刪除、重建、搬移或改變可見性。

遵守以下邊界：

- 外部寫入前先說明來源、目標、覆寫範圍與風險，完成 preview 後取得使用者明確確認。單純說「同步」不等於已確認本次覆寫。
- OAuth scope、權限、空間可見性或匿名分享是額外變更；必須分開說明並重新確認，不要隨同步一併修改。
- 「公開」不得自行解讀成匿名網路公開。讀回並報告實際的 `visibility` 與 `open_sharing`；本 Skill 預設不改它們。
- 不在輸出、Skill、日誌或報告中重現 Token、open ID、Cookie、認證檔案或 access-bearing URL。文件/節點 ID 僅在必要的本機命令中使用，對使用者以名稱與數量回報。
- 不依賴記憶中的 space ID、node token、revision 或上次成功狀態；每次寫入前都重新盤點現況。
- 缺少 scope、App pending approval、目標節點不存在或同名歧義時停止，不盲目重試、不宣稱已同步。

本 Skill 只處理既有節點的正文同步。若來源頁面無法與現有節點一一對應，先報告差異並請使用者決定，不自動建立新頁面。

## 工作流程

### 1. 盤點來源

先讀取工作區的 `AGENTS.md` 與相關專案說明，再確認使用者指定的來源目錄。不要只依賴 `git diff` 判斷內容；以磁碟上的實際檔案為準。

至少取得：

- Markdown 檔案清單、相對順序、第一個 H1 標題。
- 每檔行數與 bytes；確認圖片或附件依賴是否存在。
- 工作樹狀態，以及 preview 後來源是否仍未被改動。

對常見教材結構，先檢查例如：

```bash
rg --files <source-dir>
wc -l -c <source-dir>/*.md
rg -n '^# ' <source-dir>/*.md
```

### 2. 檢查 CLI 與授權

確認使用的是可用的 `lark-cli`，並只讀取目前授權狀態：

```bash
command -v lark-cli
lark-cli --version
lark-cli auth status
lark-cli auth check --scope "wiki:space:retrieve wiki:space:read wiki:node:retrieve wiki:node:read docx:document:readonly"
```

既有文件正文覆寫通常還需要 `docx:document:write_only`。若缺少 scope：

1. 列出缺少的最小 scope 與用途。
2. 說明 OAuth 會改變授權範圍，取得使用者確認後才啟動授權。
3. 授權完成後重新執行 `auth status`/`auth check`，不要以瀏覽器畫面或舊記錄代替 read-back。

使用 `docs` 命令時固定指定 `--api-version v2`。不要把 `lark-cli update` 或其他 CLI 安裝/升級混入同步範圍。

#### 2.1 分階段串接 per-user OAuth

使用者 OAuth 與 bot identity 的資料範圍、分享權限和稽核責任不同。預設使用 `user` identity；除非使用者明確要求 bot 流程，不要讓 `auto` 靜默選擇另一種 identity。

先檢查目前使用者 Token，再依工作階段逐步請求 scope：

```bash
lark-cli auth status
lark-cli auth scopes
lark-cli auth check --scope "wiki:space:retrieve wiki:space:read wiki:node:retrieve wiki:node:read docx:document:readonly"
```

用以下分層判斷 scope 用途，不要一次要求所有權限：

| 階段 | 最小必要 scope | 用途 |
| --- | --- | --- |
| 空間發現 | `wiki:space:retrieve` | 列出可存取的 Wiki space |
| 空間/節點唯讀盤點 | `wiki:space:read wiki:node:retrieve wiki:node:read` | 讀 space 詳情、根節點與子節點 |
| 既有正文 read-back | `docx:document:readonly` | 讀取現有 Docx 正文 |
| 既有正文覆寫 | `docx:document:write_only` | 使用 `docs +update` 更新現有文件 |
| 建立文件/頁面 | `docx:document:create wiki:node:create` | 只有使用者另外確認建頁面時才請求 |
| 修改空間設定 | `wiki:setting:write_only` 加上空間管理員權限 | 只處理 space setting，不等於匿名連結分享 |

需要新增 scope 時，先說明用途與外部授權風險，再執行 Device Flow：

```bash
lark-cli auth login --scope "wiki:space:retrieve wiki:space:read wiki:node:retrieve wiki:node:read docx:document:readonly"
```

若目前執行環境不能等待瀏覽器授權，使用 `--no-wait --json` 取得驗證流程，將必要的驗證資訊交給使用者私下完成，再以 `--device-code` 接續；不要把 Token 或認證檔案帶回對話。授權完成後，使用 `auth status` 確認目前是 `user`、Token 有效，再用 `auth check` 驗證實際 scope；`auth scopes` 的清單不能單獨證明目前 Token 或目標文件可寫。

### 2.2 權限邊界

把三種權限分開判斷：

1. App 是否獲准使用某 scope。
2. 目前 user Token 是否已取得該 scope 且仍有效。
3. 目前使用者是否對指定 space/document 有實際讀寫或管理權。

`+space-list` 成功只證明能列出空間，不證明可以列子節點、建立頁面或覆寫正文。dry-run 只證明請求形狀，不證明遠端已接受寫入；真正的權限結果以 API 回應和 read-back 為準。

若需要組織內連結可讀，先釐清「同事可讀」與「匿名網路可讀」的差異。`tenant_readable` 是組織內範圍；Wiki 節點不支援匿名 `anyone_readable`。空間 setting API 需要 `wiki:setting:write_only` 與空間管理員權限，且不等同於雲文件連結分享；任何 permission/visibility 變更都要另做 preview、確認與 read-back。

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

CLI 可能把 `Found ...` 寫到 stderr。需要解析 JSON 時保留原命令 exit code，再將 stderr 分流；不要用固定 `tail -n` 盲刪輸出前幾行來解析。

### 4. 讀取遠端現況並產生 preview

對每個既有文件讀取完整正文與目前 revision：

```bash
lark-cli docs +fetch --api-version v2 \
  --doc <OBJ_TOKEN> \
  --doc-format markdown --scope full --detail simple --format json
```

preview 必須讓使用者能核對：

| 欄位 | 內容 |
| --- | --- |
| 來源 | 本機 Markdown 路徑、行數、bytes |
| 目標 | Wiki 空間、頁面名稱、對應文件 |
| 現況 | 遠端 revision、目前是否存在 |
| 動作 | `overwrite` 或停止原因 |
| 範圍 | 是否建立/刪除/移動/改分享設定，預設全部為否 |

明確說明 `overwrite` 會取代遠端正文，並在 preview 後等待使用者確認。未取得確認前只能讀取與 dry-run，不可呼叫寫入 API。

### 5. 取得確認後原地覆寫

確認後立即重新檢查來源與遠端 revision，避免 preview 期間發生變更。若 API 支援，使用剛讀到的 revision 作為 optimistic-concurrency guard：

```bash
lark-cli docs +update --api-version v2 \
  --doc <OBJ_TOKEN> \
  --command overwrite \
  --content @<LOCAL_MARKDOWN_FILE> \
  --doc-format markdown \
  --revision-id <CURRENT_REVISION> \
  --format json
```

先用 `--dry-run` 檢查請求形狀；真正寫入後逐頁記錄回應中的 `document_id` 與新 revision。批次中任何一頁回傳錯誤、衝突或不明確時：

- 先 read-back 判斷是否已提交。
- 不要盲目重試同一個覆寫。
- 回報已完成與未完成的頁面，不能把部分成功說成全部完成。

### 6. Read-back 與稽核

所有寫入完成後，對每頁重新執行完整 `docs +fetch`，不可只讀 outline。至少驗證：

- `ok=true`、文件 ID 正確，revision 已前進或符合 API 回應。
- 新 H1 與本次更新的關鍵段落/標記存在。
- 標題層級與非空行數大致吻合；Lark 可能正規化 Markdown 空白、表格與換行，不以 bytes hash 要求完全相同。
- Wiki 根節點與子頁數量、階層、標題沒有意外增加或減少。
- 目標空間仍是原本的 `visibility` 與 `open_sharing`，本次沒有改分享權限。

可用以下命令做結構稽核：

```bash
lark-cli wiki +space-list --page-all --format json
lark-cli wiki +node-list --space-id <SPACE_ID> --page-all --format json
lark-cli wiki +node-list --space-id <SPACE_ID> \
  --parent-node-token <ROOT_NODE_TOKEN> --page-all --format json
```

完成報告要區分四種狀態：本機來源盤點、遠端寫入回應、逐頁 read-back、空間/結構稽核。只有四者都成功，才能宣稱同步完成；不要因 CLI 回傳成功就跳過 read-back。

## 失敗與停止條件

- `authorization failed: Unable to authorize. The app is pending approval.`：停止，不重試寫入，不宣稱頁面已建立或已公開。
- `missing required scope(s)`：停止並列出最小 scope，等待使用者確認授權。
- 空間、根節點、子頁不存在或名稱重複：停止，要求指定目標；不要自動建立或刪除。
- 遠端 revision 在確認後變更：重新讀取並更新 preview，必要時重新取得覆寫確認。
- 寫入結果不明確：先 read-back，再決定是否需要人工處理；不盲重試。
- 使用者要求「公開」但未指定組織內或匿名網路：先澄清範圍；本 Skill 不自行調整 permission。

## 已驗證的 Lark 踩坑

保留以下症狀與處理方式，避免把一次成功的局部命令誤當成完整流程：

| 症狀 | 根因與處理 |
| --- | --- |
| `missing required scope(s): wiki:node:retrieve` | 空間清單可以成功，但根節點/子節點盤點仍缺 scope；先補 `wiki:node:retrieve`，再重新做唯讀盤點。 |
| `missing required scope(s): docx:document:create` | 這是建立新文件的 scope；同步既有文件不應因此自動建立或刪除頁面，只有確實要建頁面時才另行授權。 |
| `authorization failed: Unable to authorize. The app is pending approval.` | Lark App 尚未核准該 scope；停止 OAuth/寫入重試，標記遠端發布未完成，等待 App 管理者處理。 |
| 用 Wiki `node_token` 呼叫 `docs +fetch`/`docs +update` | Wiki node token 與文件 `obj_token` 不同；先用 `+node-list` 取得對應 `obj_token`，文件命令只傳 `obj_token`。 |
| `+node-get` 對 raw token 要求 `--obj-type` | CLI 可能把 raw token 當成文件 object token；使用 `+node-list`，或傳入帶 `/wiki/`/`/docx/` 的 typed URL，避免猜測 token 類型。 |
| `--detail with-ids` 搭配 `--doc-format markdown` 失敗 | block IDs 只支援 XML；Markdown read-back 用 `--detail simple`，需要 block IDs 時改用 XML。 |
| JSON 前面出現 `Found 1 node(s)` | CLI 把摘要寫到 stderr；解析 JSON 時保留 exit code、分流 stderr，不要固定刪除 stdout 前幾行。 |
| 寫入回傳成功但遠端內容仍未證明 | API response 不是完整驗收；重新 `docs +fetch --scope full`，核對 H1、關鍵新增段落、revision，並稽核 Wiki 階層。 |
| 遠端 Markdown bytes/hash 與本機不同 | Lark 會正規化 Markdown 空白、表格和換行；以標題、行數/heading 結構和關鍵標記做語意驗證，不要求原始 bytes 相同。 |
| 直接用舊 space ID 或節點 ID | 遠端結構可能已變；每次先列出 space/root/children，並重新建立來源檔到 obj token 的 mapping。 |
| 看到 `public` 或使用者說「公開」就改分享 | `public`、組織內可讀和匿名可讀是不同範圍；先讀回 `visibility`/`open_sharing`，不把 permission 變更混入正文同步。 |

遇到大筆二進位、圖片或完整文件輸出時，只取必要欄位、`scope outline` 或 `detail simple`；不要把大型 tool output 原樣塞進上下文，也不要將其中的認證資料或 access-bearing URL 寫入報告。

## 交付格式

以簡潔繁體中文回報：

1. 已同步的來源檔數與目標頁數。
2. 各頁新 revision 或失敗原因。
3. read-back 驗證結果與結構/可見性稽核結果。
4. 是否建立、刪除、搬移或改變分享設定；預設明確回報「沒有」。
5. 本機工作樹是否被修改。

不輸出 Token、認證資訊、完整遠端文件內容或 access-bearing URL。
