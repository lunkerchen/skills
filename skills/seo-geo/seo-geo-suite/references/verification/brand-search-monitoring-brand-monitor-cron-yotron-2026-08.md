# 已驗證 Recipe：優創品牌搜尋每日驗證與優化（2026-08-19）

Client: 優創智能（YOTRON）, repo `$DEV_PROJECTS/yotron-website`, live site https://yotron-ai.com
GSC property: `sc-domain:yotron-ai.com` · Token: `$HOME/.hermes/google_token_starchase.json`（星創/yotron 帳號，scope `webmasters`，有 refresh token）

## Created job（cronjob API 參數）
- name: `優創品牌搜尋每日驗證與優化`
- schedule: `40 9 * * *`（09:40 Asia/Taipei）— 避開既有 09:00/09:15 報告群
- skills: `["google-search-console-api", "site-seo-geo-audit", "yotron-website"]`
- deliver: `origin`, attach_to_session=true, continuity=true
- enabled_toolsets: `["terminal", "file", "web"]`
- workdir: `$DEV_PROJECTS/yotron-website`
- model/provider: 未釘（沿用全域設定）

## Create 前後順序（重要）
1. 建立前一行驗證 token：`python3 -c 'import json,pathlib; d=json.loads((pathlib.Path.home()/".hermes/google_token_starchase.json").read_text()); print({"scope":d.get("scope"),"has_refresh_token":bool(d.get("refresh_token"))})'` → 確認 scope 含 `webmasters` 且 refresh token 存在才排程（cron 無互動授權路徑）。
2. `cronjob create`... 之後同一 turn 立即 `cronjob action=run job_id=<id>` 觸發測試執行，附註：「首次測試執行：額外確認 GSC OAuth refresh 是否成功；若失敗，精確指出缺少哪個 client credential 或 API 回應，不得用公開搜尋資料冒充 GSC。output 會自行 re-enter conversation。

## 驗證過的 prompt 骨幹（直接改專案名/domain 即可重複用）

> 你是 {品牌法定名}（{英文品牌}）的每日品牌搜尋 SEO 驗證代理。專案：{repo 絕對路徑}；正式站：{url}；GSC property：{sc-domain:...}；專用 OAuth token：{絕對路徑}。
> 每天依序：
> 1. 先讀 git status；本任務預設唯讀，不修改、不 commit、不 push、不部署。工作樹有未提交內容只記錄。
> 2. 用 google-search-console-api skill 的 refresh-token 流程拿 GSC 資料，最近 28 天 vs 前 28 天，追蹤查詢：{泛詞、品牌全名、品牌+英文、英文品牌、品牌+服務詞}。回報 clicks/impressions/CTR/avg position/趨勢；資料未達門檻要明說，不可臆測。
> 3. 檢查首頁、/about、/contact、/privacy、robots、sitemap 的 HTTP/title/canonical/可索引性/品牌法定名稱一致性。
> 4. 公開搜尋抽查查詢詞的可見結果與主要混淆實體。公開搜尋只能當抽樣，正式排名以 GSC 為準，不得宣稱固定名次。
> 5. 檢查 Organization/WebSite/LocalBusiness JSON-LD 的 name/alternateName/url/logo/sameAs；確認社群帳號實際存在（實測：schema 寫 yotron_ai，實際是 yotron.ai），失效或錯指列 P0。
> 6. 與前次輸出比較（continuity 提供），只報真正變化，避免每天重複同一建議。
> 7. 只有問題連續 ≥3 次出現或屬 P0 技術錯誤才提具體優化；每天最多 3 項，附 證據/影響/建議改法/如何驗證。
> 輸出：結論一句話 → 品牌查詢趨勢精簡表 → 今日異常（無則「無新增異常」）→ 建議優化（≤3，否則「今天不改」）→ 下一觀察點（1 項）。
> 禁止：自動發布、push、部署、購買連結、修改 Google Business Profile、建立外部承諾。需實作只給精確檔案與變更草案，等 the user 在本對話核准。

## 診斷結論（本案例，僅供方法參考，專案數據會過時）
- 根因 = 品牌實體未收斂：名稱混用（有限公司/股份有限公司）、Organization.sameAs 錯指（yotron_ai vs 實際 yotron.ai）、泛詞「優創」歧義。
- 建議路徑不是改首頁，而是：修 sameAs → 全站法定名稱統一 → Google Business Profile → 母公司官網 YOTRON 介紹頁 → 第三方品牌提及 → 品牌查詢階梯（優創智能 > 優創智能 YOTRON > 優創智能 AI 導入 > 優創）穩定後再打泛詞。