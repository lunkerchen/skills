---
name: brand-search-monitoring
description: 品牌字搜尋上不了首頁時診斷 + 排每日自動驗證 cron。觀察多於改動。
---

# 品牌搜尋監控（Brand Query Visibility）

## Trigger
- 用戶問「在 Google 搜尋 XXX 兩個字，第一頁沒有我們公司，怎麼改善？」
- 用戶要求「可以每天都排程去驗證優化嗎？」
- 任何「品牌字 vs 公司官網」的可見度診斷與後續追蹤

## 核心原則
1. **先診斷實體，不要先改頁面** — 品牌查詢上不了首頁通常是品牌訊號問題（名稱不一致、實體零散、第三方證據不足），不是頁面數量或 title 關鍵字問題。
2. **驗證優先、觀察多於改動** — 監控 job 預設 read-only，每天只報「新增/惡化」項目；只有問題連續 ≥3 次出現或屬 P0 技術錯誤才提具體修改。單日排名波動不得建議改 title/正文。
3. **拆查詢階梯** — 泛詞（「優創」）命中多家公司 = 實體歧義，難短期控制；長尾精準詞（「優創智能 AI 導入」）才是自己可控制的戰場。分開追蹤，不可混成一個指標。
4. **誠實規則** — 公開搜尋只能當抽樣，正式排名以 GSC 平均值為準；GSC 資料未達門檻要明說，不可臆測、不可用公開搜尋冒充 GSC 數據。

## 診斷步驟（品牌實體收斂盤點）
1. **Name 一致性 audit**：比對 Schema `Organization.name`/`alternateName`、全站 footer/About/Contact/Privacy 用語、法定名稱（公司登記平台查詢，注意「有限公司」vs「股份有限公司」舊文案殘留）、社群顯示名。
2. **sameAs 驗證**：`Organization.sameAs` 必須指向實際存在且活躍的帳號。用 web_search/web_extract 驗證 handle 存在，**不要信任寫在 code 裡的值**——實測案例：schema 寫 `instagram.com/yotron_ai`，實際帳號是 `yotron.ai`。Threads 是 `threads.com/@handle`。
3. **第三方實體**：Google Business Profile、母公司官網正式介紹頁、LinkedIn 公司頁、FINDIT/公司資料平台——全部統一同一組 品牌名／法定名／URL／電話／地址。需要的是可信網站自然提及，不是垃圾反向連結。
4. **確認底線已在位**：SSR 首頁、sitemap、robots、Organization/WebSite/LocalBusiness JSON-LD。都在了，就把力氣花在實體收斂與第三方提及。
5. **不要浪費時間**：繼續堆 keywords、重複塞品牌詞、大量無證據 AI 文章、重做 sitemap——都不是品牌查詢上不了首頁的主因。

## 每日監控 cron 設定
完整已驗證 recipe（job 名稱、schedule 09:40、prompt 全文、安全界線、輸出格式）見 `references/brand-monitor-cron-yotron-2026-08.md`。重點：

- `continuity=true`：下一次 run 會帶前一次輸出，能 diff 並只報新增/惡化——沒有它每天會重複同一批建議。
- `attach_to_session=true` + `deliver: origin`：用戶可以直接回覆報告，形成「監控 → 回報 → 核准 → 實作」迴圈。
- `workdir` 釘在專案根目錄；skills 在 create 時掛上（google-search-console-api + site-seo-geo-audit + 專案 skill）。
- create 後立刻 `cronjob action=run` 一次測試執行，要求 run 內「特別驗證 OAuth/API 憑證」——cron 沒有互動授權路徑，憑證 scope/refresh token 要在建立前用 json.load 一行確認。
- prompt 內建安全守則：禁止 publish/push/deploy/買連結/改 Google Business Profile；需實作時只給檔案位置+修改草案，等用戶核准。

## 輸出格式（已驗證）
結論一句話 → 品牌查詢趨勢表（28d vs 前 28d：clicks/impressions/CTR/position）→ 今日異常（只列新增/惡化）→ 建議優化（≤3，附證據/影響/改法/驗證方式）→ 下一觀察點（1 項）。

## 相關
- `google-search-console-api` — GSC 資料取得與 token 位置（$HERMES_HOME/google_token_starchase.json 為星創/yotron 帳號，scope webmasters）
- `site-seo-geo-audit` — 一次性全站審計工作流（監控 job 的每天檢查可視為它的輕量版）
- `hermes-cron-operations` — cron 生命週期 pitfall 大全

## Boundary & Exclusions

- **Do not trigger** for unrelated general queries or non-matching tasks.
