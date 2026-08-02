---
name: deep-interview
description: 結構化目標澄清。模糊需求→一次一問→三個維度全clear→clarified brief。
version: 1.0.0
tags: [clarification, interview, goal-setting, planning, ambiguity]
---

# Deep Interview — 結構化目標澄清

**一次一個問題，直到三個維度全部 clear。**

## 核心原則

- **一次只問一個 blocking question** — 不要一次丟三個問題
- **每個問題必須關聯到一個 missing decision** — 這個 decision 會改變 plan、handoff 或 stop condition
- **先查本地資訊再問人** — repo、file、memory 能回答的不要問
- **產出 clarified brief** — 不是對話紀錄，是可執行的規格文件

## 三個 Clarity Dimension

| # | Dimension | 問什麼 | 什麼算 Clear |
|---|-----------|--------|-------------|
| 1 | **目標與範圍** (Goal & Scope) | 要做什麼、不做什么、邊界在哪 | 能用一句話描述 deliverable，明確列出 non-goals |
| 2 | **約束與取捨** (Constraints & Tradeoffs) | 預算/時間/技術限制、願意犧牲什麼 | 知道哪些選項被排除、為什麼 |
| 3 | **成功標準** (Success Criteria) | 怎麼驗收、什麼算 done、verification 方法 | 有 concrete acceptance criteria + verification command |

## 流程

### Step 0：收集已知事實（不問人）

在問第一個問題之前：
1. 讀 repo 的 AGENTS.md、README、現有結構
2. 查 memory 和 session_search 看有沒有相關歷史
3. 列出你已經知道的事實
4. 找出三個 dimension 中哪些已經 clear、哪些還 ambiguous

### Step 1：問問題（每個 turn 一個）

```
Round N — Dimension: {目標與範圍|約束與取捨|成功標準}

「{一個 blocking question}」

目前 clear 的維度：
✅ 目標與範圍：{一句話}
❓ 約束與取捨：還需要知道...
❓ 成功標準：還需要知道...
```

### Step 2：Soft Check（第 5 輪）

到了第 5 輪，做一次 soft check：
- 哪些維度已經 clear？
- 剩下的 ambiguity 真的會改變 plan 嗎？
- 如果不會改變，標記為 assumption 並繼續

### Step 3：產出 Clarified Brief

當三個維度都 clear 或 round budget 用完：

```markdown
## Clarified Brief

### 目標
{一句話描述 deliverable}

### Non-Goals
- {明確排除的東西 1}
- {明確排除的東西 2}

### 約束
- {技術/時間/預算限制}

### Acceptance Criteria
- [ ] {可驗證的條件 1}
- [ ] {可驗證的條件 2}

### Verification
`{具體的測試/檢查命令}`

### Assumptions（如有）
- {在 round budget 內來不及確認的假設}
```

## 停止條件（任一觸發即停止）

1. 三個 clarity dimension 全部 clear
2. 用戶說「夠了」或「就這樣做」
3. Round budget 到了（建議 max 8 輪）

## 什麼時候不該用

- 需求已經有 concrete scope + acceptance criteria + verification command → 直接做
- 缺的資訊可以從 repo 或 local artifacts 找到 → 先查再問
- 用戶要求立即 read-only analysis，且 ambiguity 不影響答案 → 直接分析

## 陷阱

- **不要假裝在問問題但其實在暗示答案** — 問題要開放式，不要引導
- **不要問可以從 code 找到的東西** — 先 search_files / read_file
- **不要無限問下去** — 8 輪到了就停，剩下標 assumption
- **Clarified brief ≠ plan** — brief 是規格，plan 是怎麼做。brief 完成後才進 planning
