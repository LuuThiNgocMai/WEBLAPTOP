from selenium.webdriver.common.by import By
from core.base_page import BasePage

class ProductPage(BasePage):
    """Page Object for Product Detail and List views."""
    
    # Locators (Local MVC Site)
    FIRST_PRODUCT_LINK = (By.CSS_SELECTOR, ".card")
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".fs-4.fw-semibold")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".fs-3.fw-bold.text-warning")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[onclick*='AddToCart']")
    PRODUCT_MENU_LINK = (By.XPATH, "//a[contains(text(), 'Sản phẩm')]")

    def click_product_menu(self):
        self.click(self.PRODUCT_MENU_LINK)

    def click_add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def click_first_product(self):
        self.click(self.FIRST_PRODUCT_LINK)

    def get_product_title(self):
        return self.get_text(self.PRODUCT_TITLE)

    def wait_for_detail_page(self):
        return self.is_visible(self.PRODUCT_TITLE)

    def navigate_to_product(self, product_id):
        from config import BASE_URL
        url = f"{BASE_URL}/Product/Details/{product_id}"
        self.driver.get(url)
