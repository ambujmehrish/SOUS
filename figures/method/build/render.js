const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [svgPath, pngPath, pdfPath, scale] = process.argv.slice(2);
  const svg = fs.readFileSync(svgPath, 'utf8');
  const html = `<!doctype html><html><head><style>html,body{margin:0;padding:0;background:#fff}svg{display:block;width:6.875in;height:auto}</style></head><body>${svg}</body></html>`;
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: Number(scale || 4), viewport: { width: 660, height: 300 } });
  await page.setContent(html, { waitUntil: 'load' });
  const el = await page.$('svg');
  await el.screenshot({ path: pngPath });
  const box = await el.boundingBox();
  await page.pdf({ path: pdfPath, width: '6.875in', height: `${box.height / 96}in`, printBackground: true, pageRanges: '1' });
  await browser.close();
})();
