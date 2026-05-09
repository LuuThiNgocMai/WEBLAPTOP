from selenium.webdriver.common.by import By
from core.base_page import BasePage

class ProductPage(BasePage):
    """Page Object for Product Detail and List views."""
    
    # Locators (Local MVC Site)
    FIRST_PRODUCT_LINK = (By.CSS_SELECTOR, ".card")
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".fs-4.fw-semibold")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".fs-3.fw-bold.text-warning")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, 
        "button[onclick*='AddToCart'], "
        "a[onclick*='AddToCart'], "
        "input[onclick*='AddToCart'], "
        ".btn-add-to-cart, "
        "form[action*='AddToCart'] button, "
        "form[action*='AddToCart'] input[type='submit'], "
        "a[href*='AddToCart'], "
        ".bi-cart-plus, "
        "button .bi-cart"
    )
    ADD_TO_CART_XPATH = (By.XPATH, 
        "//button[contains(@onclick, 'AddToCart')] "
        "| //a[contains(@onclick, 'AddToCart')] "
        "| //input[contains(@onclick, 'AddToCart')] "
        "| //form[contains(@action, 'AddToCart')]//button "
        "| //form[contains(@action, 'AddToCart')]//input[@type='submit'] "
        "| //a[contains(@href, 'AddToCart')] "
        "| //button[contains(text(), 'Thêm vào giỏ')] "
        "| //a[contains(text(), 'Thêm vào giỏ')] "
        "| //i[contains(@class, 'bi-cart-plus')]/parent::* "
        "| //i[contains(@class, 'bi-cart')]/parent::button "
        "| //i[contains(@class, 'bi-cart')]/parent::a"
    )
    PRODUCT_MENU_LINK = (By.XPATH, "//a[contains(text(), 'Sản phẩm')]")

    def click_product_menu(self):
        self.click(self.PRODUCT_MENU_LINK)

    def click_add_to_cart(self):
        try:
            self.click(self.ADD_TO_CART_BUTTON)
        except:
            try:
                self.click(self.ADD_TO_CART_XPATH)
            except:
                # Fallback cuối: tìm bất kỳ element nào có chứa 'cart' trong class và click
                fallback = (By.XPATH, "//*[contains(@class, 'cart') and (self::button or self::a or self::i)][1]")
                self.click(fallback)

    def click_first_product(self):
        self.click(self.FIRST_PRODUCT_LINK)

    def get_product_title(self):
        return self.get_text(self.PRODUCT_TITLE)

    def wait_for_detail_page(self):
        return self.is_visible(self.PRODUCT_TITLE)

    def click_product_by_name(self, product_name):
        if not product_name:
            return self.click_first_product()
        # Tìm card chứa tên sản phẩm (có thể nằm trong h5 hoặc h6)
        locator = (By.XPATH, f"//div[contains(@class, 'card')]//*[self::h5 or self::h6][contains(text(), '{product_name}')]/ancestor::div[contains(@class, 'card')]")
        if self.is_visible(locator):
            self.click(locator)
        else:
            # Fallback nếu không tìm thấy chính xác card
            locator_simple = (By.XPATH, f"//*[contains(text(), '{product_name}')]")
            self.click(locator_simple)
            
    def navigate_to_product(self, product_id):
        from config import BASE_URL
        url = f"{BASE_URL}/Product/Details/{product_id}"
        self.driver.get(url)
