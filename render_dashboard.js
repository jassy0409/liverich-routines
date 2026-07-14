#!/usr/bin/env node
// LRM dashboard renderer: HTML -> full-page JPG (quality 92).
// Usage: NODE_PATH=/opt/node22/lib/node_modules node render_dashboard.js <in.html> <out.jpg>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

function findChromium() {
  const base = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  try {
    const dir = fs.readdirSync(base).find(d => /^chromium-\d+$/.test(d));
    if (dir) {
      const exe = path.join(base, dir, 'chrome-linux', 'chrome');
      if (fs.existsSync(exe)) return exe;
    }
  } catch {}
  return undefined; // fall back to playwright's own resolution
}

(async () => {
  const [inFile, outFile] = process.argv.slice(2);
  if (!inFile || !outFile) {
    console.error('usage: render_dashboard.js <in.html> <out.jpg>');
    process.exit(1);
  }
  const browser = await chromium.launch({ executablePath: findChromium() });
  const page = await browser.newPage({ viewport: { width: 960, height: 800 } });
  await page.goto('file://' + path.resolve(inFile));
  await page.waitForTimeout(150);
  await page.screenshot({ path: outFile, fullPage: true, quality: 92, type: 'jpeg' });
  await browser.close();
  console.log('wrote', outFile);
})();
