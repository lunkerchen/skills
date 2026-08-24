# Google Search Console 健康度例行巡檢手冊 (GSC Health Check)

本手冊規範網站於上線後、例行維護或重大架構改造後的 GSC 完整健康度檢查標準流程與指標門檻。

---

## 一、 快速巡檢清單 (Checklist)

| 巡檢維度 | 檢驗指標 | 正常標準 | 異常處置路徑 |
|---|---|---|---|
| **索引涵蓋率 (Coverage)** | `未涵蓋 (Excluded)` 原因分析 | 排除頁面均為預期內（如 noindex 或 301） | 檢查是否有非預期 `已探索 - 目前尚未編入索引` |
| **Sitemap 狀態** | `Sitemap 提交與讀取` | 狀態為「成功」，讀取時間 3 日內 | 檢查 sitemap.xml 格式、路徑與 robots.txt 宣告 |
| **體驗指標 (Page Experience)** | `Core Web Vitals (CWV)` | 良好網址比例 ≥ 90% (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1) | 壓縮圖片、移除阻塞渲染 JS/CSS、啟用快取 |
| **行動裝置可用性** | `Mobile Usability` | 0 個錯誤 | 檢查點擊目標大小 (44×44px)、可視區域 viewport |
| **結構化資料 (Schema)** | `增強功能 (Rich Results)` | 0 個無效項目 (Errors) | 依 Schema.org 修正必要欄位缺失與型態錯誤 |
| **安全性與人工作業** | `Manual Actions & Security` | 顯示「未偵測到任何問題」 | 若有警示立即排查惡意程式碼、釣魚標記或違規反向連結 |

---

## 二、 常見索引排除原因與根因排查

### 1. `已探索 - 目前尚未編入索引 (Discovered - currently not indexed)`
- **現象**：Google 知道 URL 存在，但尚未安排爬取。
- **可能原因**：
  - 新站或新頁面提交初期，爬取配額 (Crawl Budget) 尚未建立。
  - 站內內部連結權重不足（孤島頁面 Orphan Page）。
  - 伺服器回應過慢，Google 主動降低爬取頻率。
- **改善對策**：
  - 於首頁、分類頁或熱門文章增加內部連結指向該頁。
  - 檢查 `sitemap.xml` 是否包含該 URL 且 lastmod 準確。
  - 透過 GSC 網址審查工具 (URL Inspection) 手動請求編入索引。

### 2. `已檢索 - 目前尚未編入索引 (Crawled - currently not indexed)`
- **現象**：Google 爬取了頁面，但評估後決定不納入索引庫。
- **可能原因**：
  - 內容品質或原創性不足（Thin Content / AI 套話）。
  - 與站內其他頁面高度重複（Duplicate Content）。
  - 頁面缺少結構化問答與實質資訊價值。
- **改善對策**：
  - 重構內容結構：倒金字塔首段 40-60 字精準回答，增加原創數據/案例。
  - 注入權威 Schema（如 FAQPage、Article、TechArticle）。
  - 去除 AI 模板化用語，提升文本資訊密度。

### 3. `重複網址；Google 選擇的標準網址與使用者不同`
- **現象**：Google 判定的 Canonical 與 `<link rel="canonical">` 宣告不一致。
- **改善對策**：
  - 確保所有內部連結指向唯一規範網址（統一結尾斜線、統一小寫、統一協定 https）。
  - 檢查 301 轉址路徑是否乾淨，避免多重跳轉。

---

## 三、 API 自動化健康度掃描腳本範例

可透過 Search Console API 自動化拉取指定站點最近 28 天的數據：

```python
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account

def get_gsc_health(site_url: str):
    # 支援透過 Service Account 或 Application Default Credentials 授權
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
    )
    service = build("searchconsole", "v1", credentials=credentials)
    
    # 查詢點擊、曝光、CTR 與排名
    request = {
        "startDate": "2026-07-25",
        "endDate": "2026-08-22",
        "dimensions": ["date"],
        "rowLimit": 30
    }
    response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()
    return response.get("rows", [])
```

---

## 四、 週期性巡檢時程表

1. **每日 (Daily)**：監控伺服器 5xx / 4xx 錯誤日誌。
2. **每週 (Weekly)**：查看 GSC 涵蓋率圖表，追蹤新增的排除或無效網址。
3. **每月 (Monthly)**：檢視 CWV 欄位數據與 AI 搜尋引用份額（AI SOV），調整結構化標記。
