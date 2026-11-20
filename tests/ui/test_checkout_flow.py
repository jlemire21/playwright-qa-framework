from playwright.sync_api import Page
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_valid_login_loads_inventory(page: Page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.assert_loaded()


def test_locked_out_user_shows_error_banner(page: Page):
    login_page = LoginPage(page)

    login_page.navigate()
    login_page.login("locked_out_user", "secret_sauce")
    login_page.assert_error_contains("Sorry, this user has been locked out.")


def test_invalid_credentials_show_error(page: Page):
    login_page = LoginPage(page)

    login_page.navigate()
    login_page.login("standard_user", "wrong_password")
    login_page.assert_error_contains("Username and password do not match")


def test_full_end_to_end_checkout_calculates_correct_subtotal(page: Page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    # 1. Log in
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    # 2. Add two items ($29.99 backpack + $9.99 bike light = $39.98 subtotal)
    inventory_page.add_item_to_cart("sauce-labs-backpack")
    inventory_page.add_item_to_cart("sauce-labs-bike-light")
    assert inventory_page.get_cart_count() == 2

    # 3. Verify cart & complete checkout
    inventory_page.go_to_cart()
    cart_page.assert_item_count(2)
    cart_page.complete_checkout(first_name="Justin", last_name="Lemire", postal_code="B3A1A1")
    cart_page.assert_subtotal_equals("$39.98")
    cart_page.finish_order()
