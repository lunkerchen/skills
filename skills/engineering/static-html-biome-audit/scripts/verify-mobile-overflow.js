// Mobile RWD verification probe — horizontal overflow + grid/touch metrics at a viewport.
//
// Usage:
//   node verify-mobile-overflow.js <url> [width] [height]
//   node verify-mobile-overflow.js https://example.com/ 390 844
//
// One-time setup (in the dir you run from):
//   npm i playwright-core            # require('playwright') fails without a local install
//   npx --yes playwright install chromium
//
// Exit code 1 + FAIL line when horizontal overflow exists at the given viewport.
// Selectors below match the common RWD class set; adjust per page.

const { chromium } = require('playwright-core');

const url = process.argv[2] || 'http://localhost:3000/';
const width = parseInt(process.argv[3] || '390', 10);
const height = parseInt(process.argv[4] || '844', 10);

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height } });
  await page.goto(url, { waitUntil: 'networkidle' });

  const m = await page.evaluate(() => {
    const cols = (sel) => {
      const el = document.querySelector(sel);
      return el ? getComputedStyle(el).gridTemplateColumns : 'N/A';
    };
    const btn = document.querySelector('.cta-button');
    const rect = btn ? btn.getBoundingClientRect() : null;
    return {
      scrollWidth: document.documentElement.scrollWidth,
      innerWidth: window.innerWidth,
      horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth,
      kpiRow: cols('.kpi-row'),
      fieldGrid: cols('.field-grid'),
      tabs: cols('.tabs'),
      outlineGrid: cols('#outline div[style*="repeat(4"]'),
      teacherGrid: cols('#teacher div[style*="auto 1fr"]'),
      ctaButton: rect ? `${Math.round(rect.width)}x${Math.round(rect.height)}` : 'N/A',
    };
  });

  console.log(JSON.stringify(m, null, 2));
  if (m.horizontalOverflow) {
    console.error('FAIL: horizontal overflow at ' + width + 'px');
    process.exitCode = 1;
  } else {
    console.log('PASS: no horizontal overflow at ' + width + 'px');
  }
  await browser.close();
})();
