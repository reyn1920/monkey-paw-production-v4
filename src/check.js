/**
 * Headful sanity check for the local app.
 * Opens http://127.0.0.1:8000 and confirms basic interactivity.
 * No removals; only prints status lines.
 */
const puppeteer = require("puppeteer");

(async () => {
  const url = "http://127.0.0.1:8000";
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  page.setDefaultTimeout(15000);
  console.log("[PUP] opening", url);
  await page.goto(url, { waitUntil: "domcontentloaded" });
  await page.evaluate(() => { document.body.focus(); });
  const title = await page.title().catch(() => "");
  console.log("[PUP] title:", title || "(none)");
  console.log("[PUP] ok");
  await browser.close();
})().catch(err => {
  console.error("[PUP] error:", err && err.message ? err.message : err);
  process.exit(1);
});
