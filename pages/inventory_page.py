from playwright.sync_api import Page, expect


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator("[data-test='title']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")

    def assert_loaded(self) -> None:
        expect(self.title).to_have_text("Products")

    def add_item_to_cart(self, item_slug: str) -> None:
        """Clicks 'Add to cart' using SauceDemo's kebab-case item slug (e.g., 'sauce-labs-backpack')."""
        self.page.locator(f"[data-test='add-to-cart-{item_slug}']").click()

    def get_cart_count(self) -> int:
        if not self.cart_badge.is_visible():
            return 0
        return int(self.cart_badge.inner_text())

    def go_to_cart(self) -> None:
        self.cart_link.click()
