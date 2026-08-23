---
version: alpha
name: Blueprint Concrete (Hsiang Architects Visual Identity)
description: Architectural minimalism, raw concrete tones, blueprint grid precision, and monospaced technical typography for modern architectural and high-end engineering portfolios.
colors:
  primary: "#38bdf8"
  secondary: "#94a3b8"
  tertiary: "#0ea5e9"
  neutral: "#f8fafc"
  surface: "#0a0c10"
  surface-charcoal: "#12151c"
  surface-card: "#181b24"
  border: "#272b38"
  border-subtle: "#1e293b"
  muted: "#64748b"
  text-dim: "#cbd5e1"
  text-bright: "#ffffff"
typography:
  display-lg:
    fontFamily: "Plus Jakarta Sans"
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  display-md:
    fontFamily: "Plus Jakarta Sans"
    fontSize: 36px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  headline-architect:
    fontFamily: "Plus Jakarta Sans"
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0.2em"
  headline-md:
    fontFamily: "Plus Jakarta Sans"
    fontSize: 20px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0em"
  body-lg:
    fontFamily: "Plus Jakarta Sans"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "0em"
  body-md:
    fontFamily: "Plus Jakarta Sans"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "0em"
  body-sm:
    fontFamily: "Plus Jakarta Sans"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0em"
  label-mono:
    fontFamily: "Space Mono"
    fontSize: 12px
    fontWeight: 700
    lineHeight: 1.0
    letterSpacing: "0.15em"
  caption:
    fontFamily: "Plus Jakarta Sans"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "0.05em"
rounded:
  none: 0px
  xs: 2px
  sm: 4px
  md: 8px
  lg: 12px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  4xl: 96px
  grid-unit: 24px
  grid-large: 40px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.sm}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.sm}"
    padding: 12px
  button-secondary:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.sm}"
    padding: 12px
  button-secondary-hover:
    backgroundColor: "{colors.border}"
    textColor: "{colors.text-bright}"
    rounded: "{rounded.sm}"
    padding: 12px
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.secondary}"
    rounded: "{rounded.sm}"
    padding: 8px
  card-project:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.md}"
    padding: 24px
  card-project-hover:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.md}"
    padding: 24px
  tag-mono:
    backgroundColor: "{colors.surface-charcoal}"
    textColor: "{colors.secondary}"
    rounded: "{rounded.xs}"
    padding: 6px
  tag-mono-active:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.xs}"
    padding: 6px
  badge-muted:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.muted}"
    rounded: "{rounded.xs}"
    padding: 4px
  container-framed:
    backgroundColor: "{colors.border-subtle}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.sm}"
    padding: 16px
  input-field:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.sm}"
    padding: 12px
  nav-glass:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.none}"
    padding: 16px
---

## Overview

**Blueprint Concrete** is a high-precision design system derived from the modern redesign of HSIANG TEN CHUN ARCHITECTS (向登群建築師事務所). 

Rooted in the philosophy of *"Architecture is a vessel for living — seeking equilibrium between structural rationality and the play of light"*, this visual language combines raw cast concrete tones, fine blueprint drafting grids, monospaced engineering metadata, and electric cyan interactive accents.

### Core Character
- **Monolithic Brutalism with Technical Restraint**: Massive dark surfaces layered in subtle slate steps (`#0a0c10` to `#181b24`) convey gravity and physical permanence without visual noise.
- **Architectural Drafting Aesthetic**: 40px gridlines, hairline 1px borders, and monospaced technical readouts (`Space Mono`) evoke CAD drawings, structural calculation sheets, and blueprint drafting tables.
- **Atmospheric Glass & Light**: Frosted glass navigation (`rgba(10,12,16,0.88)` with 16px backdrop blur) and smooth GSAP 3 parallax motion provide a modern, tactile edge.

**The Concrete Monolith Rule.** Visual hierarchy is conveyed through stepped surface brightness (`surface` -> `surface-charcoal` -> `surface-card`), never through blurry drop shadows or artificial glows.

---

## Colors

The palette is engineered around high-contrast deep slates, cool stone grays, and a single high-voltage architectural blueprint cyan.

- **Primary (`#38bdf8` / Sky-400):** Blueprint Cyan. Used strictly for interactive focal points, active category indicators, focus rings, and milestone statistics.
- **Secondary (`#94a3b8` / Slate-400):** Concrete Cold Gray. Used for body captions, structural metadata, secondary icons, and architectural dimension lines.
- **Tertiary (`#0ea5e9` / Sky-500):** Deep Blueprint Blue. Interactive hover and pressed state for primary controls.
- **Neutral (`#f8fafc` / Concrete-50):** Off-White / Pure Chalk. Core headline text and high-contrast content on dark substrates.
- **Surface (`#0a0c10`):** Arch Black. Deep background substrate representing shadow and raw slate foundation.
- **Surface Charcoal (`#12151c`):** Intermediate platform background for section separation.
- **Surface Card (`#181b24`):** Cast concrete card containers and modal backdrop.
- **Border (`#272b38`):** Subtle 1px structural framing line.
- **Muted (`#64748b`):** De-emphasized footnotes, inactive pagination, and copyright notices.

**The Cyan Rarity Rule.** Blueprint Cyan (`#38bdf8`) must never exceed 5% of any screen surface. Its exclusivity is what drives immediate user orientation.

---

## Typography

The typographic hierarchy utilizes a deliberate tension between modern humanistic geometric sans (`Plus Jakarta Sans` / `Noto Sans TC`) and monospaced engineering type (`Space Mono`).

- **Display & Large Headlines:** `Plus Jakarta Sans` / `Noto Sans TC` (Bold 700, tight line height `1.1` to `1.2`, subtle negative tracking `-0.02em`) provides an institutional and authoritative architectural presence.
- **Architectural Titles (`headline-architect`):** Wide-tracked uppercase/title typography with `0.2em` letter spacing (`letter-spacing: 0.2em`), creating geometric tension across section headers.
- **Body Text:** Regular weight 400 at 16px (`line-height: 1.6`) on slate backgrounds ensures effortless reading across long project narratives and philosophy essays.
- **Technical Metadata (`label-mono`):** `Space Mono` at 12px (Bold 700, `letter-spacing: 0.15em`) is used for GPS coordinates, square meterage, structural specs, project IDs, and filter chips.

**The Dual-Type Tension Rule.** Narrative descriptions must use sans-serif type, while dimensional specs, years, and project IDs must strictly use monospaced fonts with uppercase styling.

---

## Layout

Layouts follow an asymmetric architectural grid system based on 24px structural intervals with a 40px blueprint backdrop.

- **Blueprint Grid Substrate:** Full-viewport or container background patterned with a 40px × 40px grid (`linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px)`).
- **Container Max-Widths:** Standard desktop content caps at `1280px` (`max-w-7xl`), with hero and project showcases expanding to `1536px` (`max-w-screen-2xl`).
- **Responsive Layout:**
  - Mobile (360px–640px): 1-column stacked flow, sticky bottom CTA bar, compact 16px edge padding.
  - Tablet (768px–1024px): 2-column masonry or balanced split grids with 24px gutters.
  - Desktop (1280px+): Asymmetric 3-column / 4-column project showcase with sticky metadata sidebars.

**The Blueprint Alignment Rule.** All interactive cards, modal dialogs, and section dividers must snap to 1px hairline borders (`border-[#272b38]`) aligned with grid intervals.

---

## Elevation & Depth

Visual depth is achieved through **Tonal Stacking** and **Frosted Glass Diffusion** rather than simulated drop shadows:

- **Layer 0 (Substrate - `#0a0c10`):** Base canvas with 40px 3% white blueprint gridlines.
- **Layer 1 (Plinth - `#12151c`):** Grouped sections, secondary bands, and filter bar containers.
- **Layer 2 (Monolith - `#181b24`):** Project cards, dialog surfaces, and form containers framed in 1px `#272b38`.
- **Layer 3 (Overlay / Glass - `rgba(10, 12, 16, 0.88)`):** Fixed header navigation and image lightbox modal with `backdrop-filter: blur(16px)`.

---

## Shapes

Shapes reflect **Precision Joinery** and structural sharpness:

- **Corner Radii:**
  - `none (0px)`: Navbars, full-bleed images, table borders, and structural dividing rules.
  - `xs (2px)`: Monospace metadata badges, tag chips, and custom scrollbar thumbs.
  - `sm (4px)`: Primary buttons, text input fields, and small controls.
  - `md (8px)`: Project cards, image preview containers, and modal dialogs.
  - `full (9999px)`: Circular status dots and icon-only floating buttons.

---

## Components

### Buttons
- **`button-primary`:** Blueprint Cyan background (`#38bdf8`) with dark ink text (`#0a0c10`), 4px corner radius, bold font. High emphasis single-action per view.
- **`button-secondary`:** Concrete card background (`#181b24`) with 1px border (`#272b38`), off-white text (`#f8fafc`).
- **`button-ghost`:** Transparent background with Slate-400 text (`#94a3b8`), transitioning to `#38bdf8` on hover.

### Cards & Project Items
- **`card-project`:** Raw concrete card surface (`#181b24`), 1px hairline border (`#272b38`), 8px radius. Features 16:10 or 4:3 architectural photo frame with subtle zoom (`scale-105`) on container hover, monospaced year/category badge, and wide-spaced title.

### Chips & Filter Tags
- **`tag-mono`:** Monospaced 12px pill/box with charcoal background (`#12151c`), 1px border, slate text.
- **`tag-mono-active`:** Solid Blueprint Cyan background (`#38bdf8`) with dark ink text (`#0a0c10`).

### Input Fields & Forms
- **`input-field`:** Dark container (`#181b24`), 1px border (`#272b38`), light text, focus ring transitioning to `border-[#38bdf8]` with zero offset.

### Navigation
- **`nav-glass`:** Fixed top header with `rgba(10, 12, 16, 0.88)` background, 16px blur, bottom border `1px solid #272b38`, housing monospaced bilingual navigation links.

---

## Do's and Don'ts

### Do's
- **Do** maintain the 40px blueprint grid background on top-level pages to preserve the architectural drafting atmosphere.
- **Do** pair every project title or section header with a monospaced metadata label (`01 / PROJECT`, `113+ BUILT WORKS`, `LAT 25.0936`).
- **Do** use `letterSpacing: 0.2em` for main section titles (`.tracking-architect`) to evoke stone carving and architectural blueprints.
- **Do** ensure all cards and modal dialogs have a visible 1px hairline border (`#272b38`) against dark backgrounds.
- **Do** include GSAP scroll-triggered smooth reveals with `clearProps: 'transform,opacity'` after animation completion.

### Don'ts
- **Don't** introduce warm pastels, saturated warm reds, or playful rounded bubbles (corner radius > 12px on content cards).
- **Don't** use heavy blurry CSS box shadows (`shadow-2xl`); use stepped background lightness and hairline borders instead.
- **Don't** overuse the cyan accent color across large content areas or card backgrounds.
- **Don't** mix more than two font families; stick to geometric sans for editorial copy and monospaced for metadata.
