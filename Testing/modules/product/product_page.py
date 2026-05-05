from selenium.webdriver.common.by import By
from core.base_page import BasePage

class ProductPage(BasePage):
    """Page Object for Product Detail and List views."""
    
    # Locators (Local MVC Site)
    FIRST_PRODUCT_LINK = (By.CSS_SELECTOR, ".card")
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".fs-4.fw-semibold")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".fs-3.fw-bold.text-warning")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".col-md-3 button[onclick*='AddToCart'], .col-md-3 .bi-cart, .product-details .btn-add-to-cart, .purchase-box .bi-cart")
    # Dự phòng bằng XPATH cực kỳ linh hoạt để tìm bất kỳ phần tử nào có liên quan đến giỏ hàng HOẶC nằm cạnh nút MUA NGAY (Ưu tiên nút trong col-md-3)
    ADD_TO_CART_XPATH = (By.XPATH, "//div[contains(@class, 'col-md-3')]//button[contains(@onclick, 'AddToCart')] | //div[contains(@class, 'col-md-3')]//i[contains(@class, 'bi-cart')] | //div[contains(translate(text(), 'MUA NGAY', 'mua ngay'), 'mua ngay')]/following-sibling::button | //div[contains(translate(text(), 'MUA NGAY', 'mua ngay'), 'mua ngay')]/parent::div/following-sibling::div//i[contains(@class, 'cart')]")
    PRODUCT_MENU_LINK = (By.XPATH, "//a[contains(text(), 'Sản phẩm')]")

    def click_product_menu(self):
        self.click(self.PRODUCT_MENU_LINK)

    def click_add_to_cart(self):
        try:
            self.click(self.ADD_TO_CART_BUTTON)
        except:
            self.click(self.ADD_TO_CART_XPATH)

    def click_first_product(self):
        self.click(self.FIRST_PRODUCT_LINK)

    def get_product_title(self):
        return self.get_text(self.PRODUCT_TITLE)

    def wait_for_detail_page(self):
        return self.is_visible(self.PRODUCT_TITLE)

    def click_product_by_name(self, product_name):
        if not product_name:
            return self.click_first_product()
        # Tìm card chứa tên sản phẩm
        locator = (By.XPATH, f"//div[contains(@class, 'card')]//h5[contains(text(), '{product_name}')]/ancestor::div[contains(@class, 'card')]")
        if self.is_visible(locator):
            self.click(locator)
        else:
            # Fallback nếu không tìm thấy chính xác card qua text trong h5
            locator_simple = (By.XPATH, f"//*[contains(text(), '{product_name}')]")
            self.click(locator_simple)
            
    def navigate_to_product(self, product_id):
        from config import BASE_URL
        url = f"{BASE_URL}/Product/Details/{product_id}"
        self.driver.get(url)
