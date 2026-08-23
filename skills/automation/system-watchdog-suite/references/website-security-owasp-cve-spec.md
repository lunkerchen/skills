---
name: website-security-owasp-cve
description: Scan authorized websites for OWASP and CVE risks.
version: 0.1.0
author: Hermes Agent contributors
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security, web, owasp, cve, vulnerability-scanning]
    related_skills: [repo-risk-audit, requesting-code-review]
---

# Website Security: OWASP + CVE Skill

對已獲授權的網站與其原始碼、依賴、容器映像執行分層資安弱掃，將證據對應到 OWASP Top 10:2025 與 CVE。技能只做偵測、驗證與報告，不自動修漏洞、不利用漏洞、不對未授權目標發送 active traffic。

## When to Use

- 使用者要求網站弱掃、OWASP Top 10、CVE、依賴漏洞或上線前資安檢查。
- 需要掃描 live URL、staging、localhost、網站 repo、package lock、Python requirements、容器映像。

**Don't use for:** 未取得目標所有者明確授權的第三方網站；破壞性 exploit、壓力測試、帳號破解、資料外洩驗證；正式環境的 active scan，除非使用者明確指定範圍與時段。

## Sources and Version Pinning

- 以 OWASP 官方 *Top 10:2025* 為分類基準；不要沿用 2021 類別名稱當成最新版本。
- CVE enrichment 優先使用 NVD CVE API 2.0：`https://services.nvd.nist.gov/rest/json/cves/2.0`。
- 依賴掃描的原始結果才是 finding 證據；NVD、CISA KEV、廠商 advisory 用於補充嚴重度、受影響版本與 exploitability。
- 報告固定記錄掃描時間、工具版本、template/database 版本、OWASP 版本與 API 查詢時間；不要把「目前沒有結果」寫成「沒有漏洞」。

OWASP Top 10:2025 對應表：

| ID | 類別 |
|---|---|
| A01 | Broken Access Control |
| A02 | Security Misconfiguration |
| A03 | Software Supply Chain Failures |
| A04 | Cryptographic Failures |
| A05 | Injection |
| A06 | Insecure Design |
| A07 | Authentication Failures |
| A08 | Software or Data Integrity Failures |
| A09 | Security Logging and Alerting Failures |
| A10 | Mishandling of Exceptional Conditions |

## Official OWASP 2025 Indicators

The source of truth is the [OWASP/Top10 `2025/docs/en/` directory](https://github.com/OWASP/Top10/tree/master/2025/docs/en). Use its prevention guidance, example attack scenarios, references, and complete CWE lists when a finding needs classification. The following baseline metrics are copied from each official 2025 score table (repository state checked 2026-08-20); they describe the Top 10 data set, not this target's risk score:

| ID | Mapped CWEs | Avg incidence | Avg coverage | Operational indicators to check |
|---|---:|---:|---:|---|
| A01 | 40 | 3.74% | 42.93% | server-side deny-by-default; object/tenant ownership; logout invalidation; directory and backup exposure |
| A02 | 16 | 3.00% | 52.35% | hardened repeatable config; unnecessary features; debug/error leakage; security headers; cloud permissions |
| A03 | 6 | 5.72% | 65.42% | SBOM; direct/transitive inventory; CVE/OSV/NVD monitoring; supported versions; trusted sources |
| A04 | 32 | 3.80% | 47.74% | sensitive-data classification; TLS >= 1.2 and HSTS; strong algorithms/key management; no sensitive caching |
| A05 | 37 | 3.08% | 42.93% | parameterized APIs/queries; server-side positive validation; interpreter-specific escaping only as fallback |
| A06 | 39 | 1.86% | 88.76% | threat model; abuse/misuse cases; critical-flow tests; tenant and tier separation; business-limit checks |
| A07 | 36 | 2.92% | 37.14% | MFA; breached-password checks; no default credentials; session timeout/revocation; login throttling |
| A08 | 14 | 2.75% | 78.52% | signed artifacts; trusted repositories; CI/CD segregation; integrity checks for serialized/untrusted data |
| A09 | 5 | 3.91% | 46.48% | security-control success/failure logs; user context; tamper-resistant audit trail; alert playbooks; DAST alert coverage |
| A10 | 24 | 2.95% | 100.00% | centralized error handling; fail-closed rollback; input validation; rate/resource limits; monitoring and alerting |

For each A-category, record `indicator_status: confirmed|suspected|not_assessed`, the checked asset/path, and the exact official page URL. The mapped CWE count is a classification aid, not a requirement to find that many weaknesses. Do not convert the average incidence or coverage into a pass/fail threshold.

## Prerequisites

先向使用者取得並記錄：

1. 掃描目標：URL、repo 路徑、映像名稱；是否為 production。
2. 授權證據：所有者/客戶授權、允許的網域與 IP、允許時間窗、禁止路徑與流量上限。
3. 輸出需求：Markdown、JSON、SARIF 或修復 backlog；是否允許把結果寫入 repo。
4. 技術範圍：登入流程、測試帳號、API spec、lockfile、容器與部署設定；沒有測試帳號就標記 authenticated coverage 為未涵蓋。

沒有授權或範圍不清時只做 repo/依賴的離線掃描，或停止並要求補齊；不得自行猜測授權。

工具採「已安裝才使用」：`nuclei`、OWASP ZAP、`osv-scanner`、`trivy`、`pip-audit`、`npm audit`、`cargo audit`。不要為一次掃描任意安裝新工具；缺少工具時在報告列為 coverage gap。

## Safety Gates

- **Passive first**：先做 repo、lockfile、headers、TLS、robots、公開 metadata 與 ZAP baseline；確認範圍後才 active。
- **No exploit by default**：不使用 destructive、intrusive、dos、credential-stuffing 或資料修改型 template；不提交表單、不建立帳號、不觸發付款/寄信/刪除。
- **Rate limit**：所有 live 掃描設定低併發、固定 request rate、短 timeout；收到 429/5xx/告警就退避或停止，不重試轟炸。
- **Secret hygiene**：結果中的 token、cookie、Authorization、個資只保留遮罩後片段；原始結果放在使用者指定的受限目錄，不貼進聊天。
- **Evidence over claims**：scanner 的 finding 要有 URL/path、時間、工具輸出摘要與重現步驟；未驗證的訊號標為 `suspected`，不得升級成 confirmed。
- **Fail closed**：掃描器錯誤、WAF 阻擋、登入失敗或 template 缺失都寫入 limitations，不得回報「clean」。

## Quick Reference

以下命令一律透過 `terminal` 執行，並把結果導向受限的報告資料夾；先執行 `--help` 確認版本與 flag。

```text
# Dependency / source scan
npm audit --json
pip-audit -f json
osv-scanner scan source -r .
trivy fs --scanners vuln,secret,misconfig --format json .

# Passive live scan
zap-baseline.py -t https://target.example -J zap.json -r zap.html
nuclei -u https://target.example -severity info,low,medium,high,critical -jsonl

# CVE evidence lookup
curl --fail-with-body --get 'https://services.nvd.nist.gov/rest/json/cves/2.0' --data-urlencode 'cveId=CVE-YYYY-NNNN'
```

只在使用者明確批准 active scan 後，才增加合適的 Nuclei non-intrusive templates 或 ZAP active policy；不可直接使用全量 aggressive profile。

## Procedure

### 1. 建立 scope manifest

建立掃描資料夾與 manifest，至少包含 `target`, `environment`, `authorized_by`, `allowed_methods`, `rate_limit`, `started_at`, `tool_versions`。檢查目標 URL 的 scheme、host、port 與排除規則；manifest 不完整就不進 live scan。

**完成條件：** 授權範圍、環境、流量上限與輸出位置可被第三方重讀。

### 2. 盤點網站與依賴

讀取 repo 的 `package-lock.json`、`pnpm-lock.yaml`、`yarn.lock`、`requirements*.txt`、`poetry.lock`、`uv.lock`、`Cargo.lock`、Dockerfile、IaC 與 CI 設定。記錄 framework、runtime、版本、公開 endpoint、auth middleware、CORS、headers、cookie flags、TLS 與 error handling。

執行可用的 dependency scanner，保留原始 JSON。以 lockfile 解析出的實際版本為準，不以 README 或 package name 猜版本。

**完成條件：** 每個可掃描依賴都有 `tool/status/result_file`，缺工具與未掃描範圍明確列出。

### 3. 執行 passive web scan

先做 TLS/certificate、HTTP security headers、cookie flags、redirect、CORS、公開 debug/error response、robots/sitemap、source map、常見 metadata 與 ZAP baseline。Nuclei 僅使用 low-risk、non-intrusive templates；每個 request 保留 host、path、status、時間與 template ID。

**完成條件：** 被動結果可重現，且沒有修改遠端資料或觸發業務副作用。

### 4. 依 OWASP Top 10:2025 分類審查

把靜態、依賴與 passive evidence 分類到 A01–A10；沒有證據的類別標成 `not_assessed`，不是 `pass`。最低檢查面：

- A01/A07：authorization scope、tenant isolation、session、MFA、reset、登入錯誤與 rate limit。
- A02/A04：安全 headers、CORS、debug、TLS、secret、加密儲存、cookie flags。
- A03/A08：lockfile、transitive dependency、CI/CD artifact、pinning、簽章與 supply-chain boundary。
- A05：SQL/NoSQL/OS/template/HTML injection 的資料流與輸入驗證；只做安全 probe，不送 destructive payload。
- A06/A10：不安全流程、狀態機、例外處理、fail-open、resource exhaustion 與 business logic boundary。
- A09：登入、權限失敗、敏感操作與例外是否有可用 audit log、告警與 traceability。

**完成條件：** 每個 A 類別有 `confirmed/suspected/not_assessed`、證據來源與 coverage 說明。

### 5. CVE triage 與去誤報

對每個依賴 finding：

1. 以 package ecosystem、vendor、product、版本與 lockfile 路徑確認 applicability。
2. 查 NVD CVE API 2.0 與廠商 advisory；需要時比對 CISA KEV。
3. 記錄 CVE ID、受影響版本、修復版本、CVSS v4/v3（若有）、CWE、published/modified 日期與 exploit status。
4. 區分 direct/transitive、runtime/dev-only、可達/不可達、已修補但資料庫過期、以及 scanner duplicate。
5. 不因 CVSS 高就直接宣稱可從網站利用；必須另外證明 deployment exposure 與 reachable code path。

**完成條件：** 每個 CVE 都有來源 URL、版本適用性與 `confirmed/suspected/not_applicable` 判定。

### 6. 只在明確批准後做 active verification

若使用者已批准，限制在 manifest 的 host/path、測試帳號與時段內；使用低流量、可回復、non-destructive checks。禁止利用成功後擴大範圍；遇到真實資料、付款、管理操作、檔案寫入或帳號變更立即停止。

**完成條件：** active requests 全部可由 audit log 對應到授權範圍，沒有業務資料變更。

### 7. 產出報告與修復順序

輸出 `security-scan-report.md`，可另輸出 `findings.json` 或 SARIF。每項 finding 固定欄位：`id`, `severity`, `status`, `owasp_2025`, `indicator_status`, `official_owasp_source`, `cve`, `asset`, `evidence`, `impact`, `reproduction_safe`, `remediation`, `fixed_version`, `source_urls`, `confidence`, `owner`, `due_date`。

排序規則：已確認的 internet-facing critical/high、CISA KEV、auth/access-control、可直接修補的 runtime CVE 優先；再排 medium、hardening 與 coverage gaps。修復建議要指向檔案、依賴或設定，不自動改檔。

**完成條件：** 報告包含 executive summary、scope、method、OWASP matrix、CVE table、limitations、原始證據位置與重掃建議。

## Verification

交付前逐項確認：

- 工具 exit code、錯誤與中止原因已保留；沒有以空輸出當成 clean。
- 報告中的 finding 數量、severity totals、OWASP 類別數與 JSON 欄位由腳本計算並互相一致。
- 每個 confirmed finding 有最少一個原始證據檔與來源 URL；每個 suspected finding 明確標記待人工驗證。
- secret/token/cookie/個資已遮罩；原始 artifact 不在 git diff 或聊天內容內。
- 若是 repo 掃描，`git status --short` 僅包含使用者明確允許的報告檔；若是 live scan，重複 passive check 後結果穩定或差異有解釋。
- 報告明確寫出「未掃描」與「無法判定」的範圍；不得使用「已通過 OWASP」或「零漏洞」這類過度承諾。

## Severity and Reporting Rules

嚴重度以 exploitability、exposure、impact、confidence 綜合判定；CVSS 只是輸入，不是最終風險。格式建議：`P0 Critical`（可立即接管/大量資料外洩）、`P1 High`（公開可達的 auth/access/RCE/重大 CVE）、`P2 Medium`（需條件或中等影響）、`P3 Low`（hardening/資訊洩漏）、`Info`（觀察與 coverage gap）。每次掃描都產出 `scan_status: complete|partial|blocked`。

## Pitfalls

- OWASP Top 10 是風險分類與 awareness 文件，不是自動化合規證明；scanner 沒有覆蓋 business logic 就不能宣稱 A06/A10 通過。
- NVD 延遲、CPE 誤配、未有 CVSS 或 vendor advisory 差異都可能造成 false positive/negative；記錄 modified date 與來源。
- dependency scanner 找到 CVE 不代表網站 runtime 可達；反過來，未列 CVE 也不代表自訂程式碼沒有 A01/A05。
- WAF、登入牆、SPA route、rate limit、生成式 endpoint 會讓動態 coverage 變薄；把阻擋當 limitation，不反覆加壓。
- 不要把 `npm audit fix`、自動升版或 scanner 的 `--fix` 當成掃描步驟；它們會修改 lockfile，必須另開變更並測試。

## References

- OWASP Top 10:2025 repository source and indicators: https://github.com/OWASP/Top10/tree/master/2025/docs/en/
- OWASP Top 10:2025: https://owasp.org/Top10/2025/
- NVD CVE API 2.0: https://nvd.nist.gov/developers/vulnerabilities
- CISA Known Exploited Vulnerabilities Catalog: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- OWASP ZAP Baseline Scan: https://www.zaproxy.org/docs/docker/baseline-scan/
- ProjectDiscovery Nuclei: https://docs.projectdiscovery.io/tools/nuclei/overview
