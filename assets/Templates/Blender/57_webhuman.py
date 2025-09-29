from fastapi import APIRouter
from pydantic import BaseModel, Field
import random

router = APIRouter()

try:
    from playwright.async_api import async_playwright

    PLAYWRIGHT_OK = True
except Exception:
    PLAYWRIGHT_OK = False


class BrowseTask(BaseModel):
    url: str = Field(..., description="Public URL to browse")
    max_seconds: int = Field(40, ge=5, le=180)
    min_scrolls: int = Field(2, ge=0, le=50)
    max_scrolls: int = Field(10, ge=0, le=200)
    typing: bool = Field(True, description="Type into search boxes if found")
    headless: bool = Field(False, description="Visible by default for live runs")


def _jitter(a, b):
    import random as _r

    return _r.uniform(a, b)


async def _humanize_page(page, task: BrowseTask):
    await page.wait_for_timeout(int(_jitter(500, 1600)))
    scrolls = random.randint(task.min_scrolls, task.max_scrolls)
    for _ in range(scrolls):
        await page.mouse.wheel(0, random.randint(200, 1000))
        await page.wait_for_timeout(int(_jitter(400, 1500)))
    if task.typing:
        boxes = page.locator("input[type='search'], input[type='text'], textarea")
        count = await boxes.count()
        if count > 0:
            box = boxes.nth(0)
            await box.click()
            sample = "ideas " + str(random.randint(10, 99))
            for ch in sample:
                await page.keyboard.type(ch, delay=int(_jitter(40, 110)))
            await page.wait_for_timeout(int(_jitter(600, 1400)))


@router.post("/enqueue")
async def enqueue(task: BrowseTask):
    if not PLAYWRIGHT_OK:
        return {
            "ok": False,
            "message": "Playwright not available; run: pip3 install --user playwright && python3 -m playwright install chromium",
        }
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=task.headless,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context(
            locale="en-US", timezone_id="America/Denver"
        )
        page = await context.new_page()
        await page.goto(task.url, wait_until="domcontentloaded", timeout=45000)
        await _humanize_page(page, task)
        await browser.close()
    return {"ok": True}
