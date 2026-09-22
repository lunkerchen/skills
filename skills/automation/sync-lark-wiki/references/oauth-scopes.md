# 分階段 per-user OAuth Scope 表（sync-lark-wiki）

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


## 權限邊界（三層判斷）

把三種權限分開判斷：

1. App 是否獲准使用某 scope。
2. 目前 user Token 是否已取得該 scope 且仍有效。
3. 目前使用者是否對指定 space/document 有實際讀寫或管理權。

`+space-list` 成功只證明能列出空間，不證明可以列子節點、建立頁面或覆寫正文。dry-run 只證明請求形狀，不證明遠端已接受寫入；真正的權限結果以 API 回應和 read-back 為準。

若需要組織內連結可讀，先釐清「同事可讀」與「匿名網路可讀」的差異。`tenant_readable` 是組織內範圍；Wiki 節點不支援匿名 `anyone_readable`。空間 setting API 需要 `wiki:setting:write_only` 與空間管理員權限，且不等同於雲文件連結分享；任何 permission/visibility 變更都要另做 preview、確認與 read-back。
lark-cli auth login --scope "wiki:space:retrieve wiki:space:read wiki:node:retrieve wiki:node:read docx:document:readonly"
```

若目前執行環境不能等待瀏覽器授權，使用 `--no-wait --json` 取得驗證流程，將必要的驗證資訊交給使用者私下完成，再以 `--device-code` 接續；不要把 Token 或認證檔案帶回對話。授權完成後，使用 `auth status` 確認目前是 `user`、Token 有效，再用 `auth check` 驗證實際 scope；`auth scopes` 的清單不能單獨證明目前 Token 或目標文件可寫。
