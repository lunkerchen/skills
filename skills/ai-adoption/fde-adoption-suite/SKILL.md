---
name: fde-adoption-suite
description: 前置部署工程師（FDE）與企業 AI 導入全能旗艦：結構化目標澄清（deep-interview）、QA 品質證據設計、子代理平行調度、PSF/MVD 交付框架與組織無阻力變革管理。
version: 1.0.0
author: Community
license: MIT
read_when:
  - User asks about enterprise AI adoption, FDE (Forward-Deployed Engineer) workflows, or AI delivery playbooks
  - User needs requirements clarification, deep-interview (1Q-at-a-time), or goal deconstruction
  - User needs QA scenario design, edge-case formulation, or failure mode definitions before coding
  - User wants to optimize subagent delegation (subagent-efficiency) to prevent token waste
  - User wants change-management strategies to reduce employee fear and drive peer adoption
metadata:
  hermes:
    tags: [ai-adoption, fde, interview, qa-design, orchestration, change-management, suite]
---

# FDE 企業 AI 導入全能旗艦（FDE Adoption Suite）

整合前置部署工程師（Forward-Deployed Engineer, FDE）現場交付方法論、結構化需求訪談、品質證據設計、多代理調度與企業變革管理的一體化實戰工作台。

---

## 核心認知：FDE 落地五大支柱

```
                             ┌──────────────────────────────────────────────┐
                             │          FDE 企業 AI 落地全能架構            │
                             └──────────────────────┬───────────────────────┘
                                                    │
         ┌──────────────────┬───────────────────────┴───────────────────────┬──────────────────┐
         ▼                  ▼                                               ▼                  ▼
【1. 結構化目標澄清】  【2. 品質證據設計】                           【3. 子代理調度決策】   【4. 變革與現場交付】
 • 1Q-at-a-time        • QA Scenarios 先行                           • 平行加速 (3+ 獨立)     • PSF / MVD 交付
 • 3 維度全 Clear      • 邊界條件與極限測試                          • 避免 Token 浪費        • 成果計價與同儕槓桿
```

---

## 旗艦模組一覽

### 模組 1：結構化目標澄清（Deep Interview）
- **單問紀律（1Q-at-a-time）**：每次只問一個關鍵問題，嚴禁一次拋出 5 個問題壓垮使用者。
- **三維度收斂**：
  1. 核心目標（Goal & Expected Outcome）
  2. 硬性約束（Constraints & Boundaries）
  3. 驗收標準（Verifiable Acceptance Criteria）
- **產出成果**：結構化《Clarified Brief》，作為後續所有開發與交付的真源（Source of Truth）。

### 模組 2：品質證據設計（QA Scenario Design）
- **實作先行門戶**：在 Implement 之前，先撰寫 QA 測試矩陣。
- **三大失敗防護層**：
  1. 正常路徑驗證（Happy Path Validation）
  2. 極限邊界條件（Edge Cases: 空值、大 payload、逾時、斷網）
  3. 失敗復原模式（Failure Modes: 錯誤訊息結構化、降級備援）

### 模組 3：子代理調度決策矩陣（Subagent Efficiency）
- **派工決策準則**：
  - ✅ **必須派工**：跨 3+ 獨立領域、大量中繼資料會塞爆 Context、長耗時獨立探勘。
  - ❌ **嚴禁派工**：機械式純腳本執行（用 execute_code）、單一工具呼叫、需要與使用者互動的任務。
- **實作與盲審協定**：Implementer（實作端）+ Blind Auditor（盲審端）雙重驗證。

### 模組 4：FDE 現場交付 Playbook（FDE Playbook）
- **PSF（Problem-Solution Fit）**：深入業務現場觀察「影子工作法（Shadowing）」，找出真正卡點。
- **MVD（Minimum Viable Delivery）**：第一週拿出可點擊、可運行的最小交付物，建立客戶信任。
- **成果計價模式**：依節省工時、轉化率提升或錯誤率下降計價，而非賣工時（Time & Material）。

### 模組 5：組織無阻力變革管理（Change Management）
- **證明業務價值**：用真實數據（ROI、工時節省）向決策者匯報。
- **降低同仁恐懼**：將 AI 定位為「外骨骼 / 助手」而非「替代者」。
- **同儕示範槓桿**：先在 1 個關鍵種子員工/部門做出標竿，由同儕帶動全員採用。
