from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator("[data-test='inventory-item']")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.subtotal_label = page.locator("[data-test='subtotal-label']")
        self.finish_button = page.locator("[data-test='finish']")
        self.complete_header = page.locator("[data-test='complete-header']")

    def assert_item_count(self, expected_count: int) -> None:
        expect(self.cart_items).to_have_count(expected_count)

    def complete_checkout(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.checkout_button.click()
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    def assert_subtotal_equals(self, expected_subtotal: str) -> None:
        expect(self.subtotal_label).to_contain_text(expected_subtotal)

    def finish_order(self) -> None:
        self.finish_button.click()
        expect(self.complete_header).to_have_text("Thank you for your order!")
