from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from playwright.async_api import async_playwright
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust this to lock down access if needed
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scrape")
async def scrape(domain: str):
    try:
        url = f"https://{domain}"
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url, timeout=100000)
            cookies = await context.cookies()
            await browser.close()
            return {"domain": domain, "cookies": cookies}
    except Exception as e:
        return {"domain": domain, "error": str(e)}
