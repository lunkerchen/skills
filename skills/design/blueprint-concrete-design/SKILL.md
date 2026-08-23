---
name: blueprint-concrete-design
description: Use when building architectural blueprint dark websites.
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [design, architecture, dark-mode, blueprint, concrete, gsap, tailwind, tokens]
    related_skills: [design-md, cjk-web-typography, modern-css-patterns, popular-web-designs]
---

# Blueprint Concrete Design System (建築藍圖與清水模設計系統)

A high-precision, architectural-grade visual design system derived from modern architectural studio portfolio standards (向登群建築師事務所 HSIANG TEN CHUN ARCHITECTS).

Combines monolithic raw concrete dark tones (`#0a0c10` to `#181b24`), fine 40px blueprint drafting grid lines, monospaced CAD-style metadata (`Space Mono`), wide-tracked editorial typography (`0.2em`), and electric blueprint cyan accents (`#38bdf8`).

## 1. Quick Start Boilerplate

When building a single-page or multi-page architectural / engineering site, embed this Tailwind CDN config and base CSS:

```html
<!-- Google Fonts: Plus Jakarta Sans + Noto Sans TC + Space Mono -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Noto+Sans+TC:wght@300;400;500;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">

<!-- Tailwind Custom Configuration -->
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    darkMode: 'class',
    theme: {
      extend: {
        colors: {
          arch: {
            black: '#0a0c10',     // Base canvas (Substrate)
            charcoal: '#12151c',  // Platform / Band background
            card: '#181b24',      // Cast concrete cards & modals
            border: '#272b38',    // Hairline structural framing line
            borderSubtle: '#1e293b',
            accent: '#38bdf8',    // Blueprint Cyan (Sky-400)
            accentHover: '#0ea5e9',
            slate: '#94a3b8',     // Concrete cold gray (Metadata)
            muted: '#64748b',     // Secondary caption / footnote
          }
        },
        fontFamily: {
          sans: ['"Plus Jakarta Sans"', '"Noto Sans TC"', 'sans-serif'],
          mono: ['"Space Mono"', 'monospace']
        },
        letterSpacing: {
          architect: '0.2em',
          mono: '0.15em'
        }
      }
    }
  }
</script>

<style>
  /* 40px Architectural Blueprint Drafting Grid */
  .blueprint-grid {
    background-size: 40px 40px;
    background-image: 
      linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  }

  /* Frosted Glass Header Navigation */
  .glass-nav {
    background: rgba(10, 12, 16, 0.88);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid #272b38;
  }
</style>
```

---

## 2. Core Design Rules (Named Rules)

1. **The Blueprint Rule**
   All top-level canvas sections feature the 40px drafting grid (`rgba(255,255,255,0.03)`). Component containers snap to 24px/48px grid increments with 1px hairline borders (`border-[#272b38]`).

2. **The Cyan Rarity Rule**
   Blueprint Cyan (`#38bdf8`) is an intentional accent representing laser drafting lines and active selection. It must occupy **$\le 5\%$** of any visible screen area.

3. **The Concrete Monolith Rule**
   Visual elevation is created exclusively by stepped tonal brightness (`#0a0c10` $\rightarrow$ `#12151c` $\rightarrow$ `#181b24`), never through heavy fuzzy drop-shadows (`shadow-2xl`).

4. **The Dual-Type Tension Rule**
   - Narrative & Headings: Geometric Sans (`Plus Jakarta Sans` / `Noto Sans TC`), with section titles using `letter-spacing: 0.2em` (`.tracking-architect`).
   - Technical Metadata: Strictly Monospaced (`Space Mono`), uppercase with `0.15em` tracking for IDs, coordinates, years, and area measurements.

---

## 3. UI Component Patterns

### Primary CTA Button
```html
<a href="#contact" class="inline-flex items-center justify-center gap-2 px-6 py-3 rounded text-sm font-semibold tracking-wider bg-arch-accent text-arch-black hover:bg-arch-accentHover transition-all duration-200">
  <span>CONSULTATION / 預約諮詢</span>
  <i data-lucide="arrow-right" class="w-4 h-4"></i>
</a>
```

### Architectural Project Card
```html
<article class="group relative bg-arch-card border border-arch-border rounded-lg overflow-hidden transition-all duration-300 hover:border-arch-accent/50">
  <div class="aspect-[16/10] overflow-hidden bg-arch-black relative">
    <img src="project-cover.jpg" alt="Project Name" class="w-full h-full object-cover object-center transition-transform duration-500 group-hover:scale-105" loading="lazy">
    <span class="absolute top-3 left-3 px-2 py-1 rounded-[2px] bg-arch-charcoal/90 border border-arch-border text-[11px] font-mono tracking-mono text-arch-slate">
      2024 / RESIDENTIAL
    </span>
  </div>
  <div class="p-6">
    <div class="text-[12px] font-mono tracking-mono text-arch-accent mb-1">PROJ_042 ｜ 25.0493° N, 121.4870° E</div>
    <h3 class="text-xl font-bold text-white tracking-wide mb-2 group-hover:text-arch-accent transition-colors">建案名 / Project Title</h3>
    <p class="text-sm text-arch-slate line-clamp-2 leading-relaxed">基地座落於水岸交界，透過退縮露台與清水混凝土立面建立光影層次。</p>
  </div>
</article>
```

### Monospaced Filter Tag / Chip
```html
<!-- Inactive Chip -->
<button class="px-3 py-1.5 rounded-[2px] text-xs font-mono tracking-mono bg-arch-charcoal border border-arch-border text-arch-slate hover:text-white hover:border-arch-slate transition-all">
  ALL WORKS (113)
</button>

<!-- Active Chip -->
<button class="px-3 py-1.5 rounded-[2px] text-xs font-mono tracking-mono bg-arch-accent text-arch-black font-bold">
  APARTMENTS (24)
</button>
```

---

## 4. GSAP 3 Motion Integration

For smooth entrance and scroll triggers:

```javascript
// Header Reveal
gsap.fromTo('header', 
  { y: -30, opacity: 0 }, 
  { y: 0, opacity: 1, duration: 0.8, ease: 'power2.out', clearProps: 'transform,opacity' }
);

// Hero Image Scale & Parallax
gsap.fromTo('.hero-bg',
  { scale: 1.12, opacity: 0 },
  { scale: 1.0, opacity: 0.4, duration: 1.6, ease: 'power2.out', clearProps: 'transform' }
);

// Staggered Project Cards Reveal
gsap.fromTo('.project-card',
  { y: 35, opacity: 0 },
  {
    y: 0, opacity: 1, duration: 0.7, stagger: 0.1, ease: 'power2.out',
    clearProps: 'transform,opacity',
    scrollTrigger: { trigger: '.project-grid', start: 'top 88%', once: true }
  }
);
```
