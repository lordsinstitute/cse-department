import asyncio
import base64
import threading
from playwright.async_api import async_playwright


class BrowserManager:
    """Manages Playwright browser lifecycle with async-sync bridge."""

    def __init__(self):
        self._loop = None
        self._thread = None
        self._playwright = None
        self._browser = None
        self._page = None

    def start(self):
        """Start browser on a background asyncio thread."""
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        self.run_async(self._launch_browser())

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    async def _launch_browser(self):
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )

    def stop(self):
        """Close browser and stop the event loop."""
        if self._browser:
            self.run_async(self._close())
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread:
            self._thread.join(timeout=5)

    async def _close(self):
        if self._page:
            await self._page.close()
            self._page = None
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

    def run_async(self, coro):
        """Bridge sync Flask to async Playwright."""
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result(timeout=60)

    def new_page(self, url=None):
        """Create a new page and optionally navigate to a URL."""
        return self.run_async(self._new_page(url))

    async def _new_page(self, url):
        if self._page:
            await self._page.close()
        context = await self._browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        self._page = await context.new_page()
        if url:
            await self._page.goto(url, timeout=30000, wait_until="domcontentloaded")
        return self._page

    def navigate(self, url):
        """Navigate the current page to a URL."""
        return self.run_async(self._navigate(url))

    async def _navigate(self, url):
        if not self._page:
            return await self._new_page(url)
        await self._page.goto(url, timeout=30000, wait_until="domcontentloaded")
        return self._page

    def screenshot(self, quality=50):
        """Take a JPEG screenshot, return base64-encoded string."""
        return self.run_async(self._screenshot(quality))

    async def _screenshot(self, quality):
        if not self._page:
            return None
        img_bytes = await self._page.screenshot(type="jpeg", quality=quality)
        return base64.b64encode(img_bytes).decode("utf-8")

    @property
    def page(self):
        return self._page
