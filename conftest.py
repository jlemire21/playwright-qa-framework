from pathlib import Path
import pytest
from playwright.sync_api import Page

BASE_URL = "https://saucedemo.com"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configures a consistent desktop viewport for headless browser tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Automatically captures a screenshot if a Playwright UI test fails."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page: Page | None = item.funcargs.get("page")
        if page:
            screenshots_dir = Path("reports/screenshots")
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshots_dir / f"{item.name}.png"
            page.screenshot(path=str(screenshot_path))
