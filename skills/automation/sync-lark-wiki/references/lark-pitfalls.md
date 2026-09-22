# 已驗證的 Lark 踩坑（sync-lark-wiki）

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
