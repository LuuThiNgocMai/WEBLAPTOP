from selenium.webdriver.common.by import By
from core.base_page import BasePage

class CartPage(BasePage):
    """Page Object for Shopping Cart functions."""
    
    # Locators (Local MVC Site)
    CART_ICON = (By.CSS_SELECTOR, "i.bi-cart")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item")
    REMOVE_PRODUCT_BUTTON = (By.CSS_SELECTOR, ".remove-btn") # Match method name
    INCREMENT_BUTTON = (By.CSS_SELECTOR, ".btn-plus")
    DECREMENT_BUTTON = (By.CSS_SELECTOR, ".btn-minus")
    CLEAR_ALL_BUTTON = (By.CSS_SELECTOR, ".btn-clear-cart")
    TOTAL_PRICE = (By.CSS_SELECTOR, ".final-price")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".btn-dat-hang")
    CART_EMPTY_MESSAGE = (By.CSS_SELECTOR, ".empty-cart-message")
    ADD_TO_CART_BUTTON_LIST = (By.CSS_SELECTOR, ".btn-add-to-cart")

    def click_add_to_cart_first_item(self):
        # Adds the first item found on the page (usually home or search results)
        self.click(self.ADD_TO_CART_BUTTON_LIST)

    def open_cart(self):
        self.click(self.CART_ICON)

    def increment_quantity(self):
        self.click(self.INCREMENT_BUTTON)

    def decrement_quantity(self):
        self.click(self.DECREMENT_BUTTON)

    def remove_first_product(self):
        self.click(self.REMOVE_PRODUCT_BUTTON)
        
    def clear_all(self):
        self.click(self.CLEAR_ALL_BUTTON)

    def wait_for_cart_page(self):
        return self.is_visible(self.REMOVE_PRODUCT_BUTTON) or self.is_visible(self.CART_EMPTY_MESSAGE)
