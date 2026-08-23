---
name: frontend-design-suite
description: 前端設計與 RWD 打磨旗艦：夜空深色星空美學（night-sky-design）、科技品牌風格模式（popular-web-designs）、行動端 RWD 強制防錯規則（rwd-mobile-rules）與靜態 HTML 現代化翻新（static-html-polish）。
version: 1.0.0
author: Community
license: MIT
read_when:
  - User wants to design a landing page, portfolio, or web app with dark mode, night-sky, or Stripe/Linear/Vercel aesthetic
  - User needs strict mobile RWD hardening (44px touch targets, viewport overflow prevention, zero layout shift)
  - User wants to audit, modernize, or polish an existing static HTML page with modern CSS and accessibility
metadata:
  hermes:
    tags: [design, frontend, rwd, dark-mode, css, a11y, ui-ux, suite]
---

# 前端設計與 RWD 打磨旗艦（Frontend Design Suite）

整合現代科技美學設計系統、嚴格行動端 RWD 規範、微互動與無障礙網頁打磨的一體化前端旗艦技能。

---

## 旗艦模組一覽

### 模組 1：設計系統與視覺語彙（Design Systems）
- **夜空星空風格（Night Sky Design）**：深色畫布 (`#0a0d14`)、星空微粒子背景、玻璃擬物（Glassmorphism: `backdrop-filter: blur(24px)`）、品牌漸層霓虹。
- **科技品牌極簡美學（Tech Brand Aesthetics）**：對齊 Stripe / Linear / Vercel 的高質感細邊框 (`border: 1px solid rgba(255,255,255,0.08)`)、精準字階與負空間運用。

### 模組 2：行動端 RWD 強制規範（Strict Mobile RWD Rules）
- **44px 觸控靶區**：所有按鈕、超連結、表單控制項最小點擊區域 $\ge 44 	imes 44	ext{ px}$。
- **零水平溢出**：全站強制 `max-width: 100vw; overflow-x: hidden;`，圖片與容器一律 `max-width: 100%`。
- **防佈局偏移（Zero CLS）**：所有圖片與媒體顯式標註 `width` / `height` 或 `aspect-ratio`。

### 模組 3：靜態 HTML 現代化翻新（Static HTML Polish）
- **語意標籤補齊**：`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>` 取代 div-soup。
- **無障礙（a11y）加固**：100% 可互動元素具備 Accessible Name、表單帶關聯 `<label>`、色彩對比度通過 WCAG AA。
