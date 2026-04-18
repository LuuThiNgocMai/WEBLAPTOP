from selenium.webdriver.common.by import By
from core.base_page import BasePage

class CartPage(BasePage):
    """Page Object for Shopping Cart functions."""
    
    # Locators (Local MVC Site)
    CART_ICON = (By.CSS_SELECTOR, "i.bi-cart")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item")
    REMOVE_ITEM_BUTTON = (By.CSS_SELECTOR, ".remove-btn")
    TOTAL_PRICE = (By.CSS_SELECTOR, ".final-price")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".btn-dat-hang")
    CART_EMPTY_MESSAGE = (By.CSS_SELECTOR, ".empty-cart-message")

    def click_add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def open_cart(self):
        self.click(self.CART_ICON)

    def remove_first_product(self):
        self.click(self.REMOVE_PRODUCT_BUTTON)

    def wait_for_cart_page(self):
        return self.is_visible(self.REMOVE_PRODUCT_BUTTON) or self.is_visible(self.CART_EMPTY_MESSAGE)
