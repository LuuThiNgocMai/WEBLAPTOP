from selenium.webdriver.common.by import By
from core.base_page import BasePage

class CheckoutPage(BasePage):
    """Page Object for Checkout functions."""
    
    # Locators
    CHECKOUT_BUTTON = (By.ID, "checkout-btn")
    NAME_INPUT = (By.ID, "full-name")
    ADDRESS_INPUT = (By.ID, "address")
    PHONE_INPUT = (By.ID, "phone")
    CONFIRM_ORDER_BUTTON = (By.ID, "place-order")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "order-success")

    def click_checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def enter_shipping_info(self, name, address, phone):
        self.enter_text(self.NAME_INPUT, name)
        self.enter_text(self.ADDRESS_INPUT, address)
        self.enter_text(self.PHONE_INPUT, phone)

    def click_confirm(self):
        self.click(self.CONFIRM_ORDER_BUTTON)

    def is_order_successful(self):
        return self.is_visible(self.SUCCESS_MESSAGE)
