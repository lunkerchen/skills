---
name: qa-scenario-design
description: 品質證據設計。implement前先設計QA scenarios→edge cases→failure modes。
version: 1.0.0
tags: [quality, QA, scenarios, verification, evidence]
---

# QA Scenario Design — 品質證據循環

**在 implement 之前，先設計怎麼驗證。**

## 核心原則

- **QA scenarios 是準備，不是執行** — 設計 test cases ≠ 跑 test cases
- **Evidence 分離** — 準備（prepared）≠ 觀測（observed）≠ 驗證（verified）
- **MECE coverage** — 每個 failure mode 至少被一個 scenario 覆蓋
- **Blind auditor 驗的是 diff，不是 reasoning** — auditor 看不到 implementer 的推理過程

## 流程

### Step 1：Failure Mode Analysis（implement 之前）

在拆解任務時，同時列出：

```
## Failure Modes

### Technical Execution（一定做）
- Build 失敗（語法、type error、missing import）
- Test 失敗（既有 test 被 break）
- Runtime error（null、undefined、edge case）

### Semantic/Architectural（結構改變時做）
- API contract 被破壞（backward incompatible）
- State management 被污染
- Module boundary 被跨越

### Behavioral（UI/runtime 可檢查時做）
- 互動流程中斷
- 視覺 regression
- 效能退化
```

### Step 2：QA Scenarios（每個 failure mode 一個）

```
## QA Scenarios

| # | Scenario | Failure Mode | Verification | Evidence Type |
|---|----------|-------------|-------------|---------------|
| 1 | 既有 test suite 通過 | Build/Test | `pnpm test` | observed（test output） |
| 2 | 新功能的 happy path | Runtime | 手動觸發 + screenshot | observed（terminal output） |
| 3 | Edge case: 空 array | Runtime | 單元測試 | prepared（scenario designed） |
| 4 | API backward compat | Semantic | 比較 before/after API response | observed（diff） |
```

### Step 3：Blind Auditor Panel Design

根據 failure mode 決定 auditor panel 組成：

| 改動類型 | 必做 | 加做 |
|----------|------|------|
| 任何 3+ 步驟 | Technical Execution | — |
| 結構/架構改變 | Technical Execution | Semantic/Architectural |
| UI/runtime 可見 | Technical Execution | Behavioral |

### Step 4：Evidence Collection

每個 QA scenario 必須產出 one of：

| Evidence 狀態 | 意義 |
|---------------|------|
| `prepared` | Scenario 設計好了，還沒跑 |
| `observed` | Scenario 跑了，有 output 記錄 |
| `verified` | Scenario 通過，有 assertion evidence |

**Claim 規則：** 只有 `verified` 才能 claim「這個 scenario 通過了」。`observed` 只能 claim「跑了但結果未知」。`prepared` 只能 claim「設計好了」。

## 與 implement-and-audit 的整合

```
1. 設計 QA scenarios（本 skill）
2. 拆解任務 + 分配 subagents
3. Implementer 執行
4. Blind auditor 用 QA scenarios 作為驗證清單
5. 每個 scenario 標記 observed/verified
6. 所有 scenario verified → claim done
```

## 快速模板

```markdown
## QA Design — {task name}

### Failure Modes
- [ ] Build: {specific risk}
- [ ] Test: {existing tests at risk}
- [ ] Semantic: {API/contract risk}
- [ ] Behavioral: {UI/runtime risk}

### Scenarios
| # | What to check | How | Evidence |
|---|--------------|-----|----------|
| 1 | {scenario} | {verification method} | {prepared/observed/verified} |

### Auditor Panel
- Technical Execution: ✅ (always)
- Semantic: {yes/no — why}
- Behavioral: {yes/no — why}
```

## 陷阱

- **不要在 scenario 設計階段就跑 test** — 先設計完再統一執行
- **不要讓 implementer 當自己的 auditor** — 必須是獨立 subagent
- **不要省略 edge cases** — 空值、超長輸入、並發是最高頻 bug 來源
- **不要把 observed 當 verified** — 跑了不等於通過
