from selenium.webdriver.common.by import By
from core.base_page import BasePage
from config import URL_CONFIG

class SearchPage(BasePage):
    """Page Object for Product Search functions."""
    
    # Locators (Local MVC Site)
    SEARCH_INPUT = (By.NAME, "name")
    SEARCH_BUTTON = (By.NAME, "submitSearch")
    SEARCH_RESULTS_CONTAINER = (By.CLASS_NAME, "product-home") # Dựa trên cấu trúc container hiển thị danh sách

    def navigate_to_home(self, env_config=None):
        url = "https://laptop-store.example.com"
        if env_config and env_config.get('target_url'):
            url = env_config.get('target_url')
        else:
            url = URL_CONFIG.get("home", url)
            
        final_url = self.get_formatted_url(url, env_config.get('auth') if env_config else None)
        self.driver.get(final_url)

    def enter_search_keyword(self, keyword):
        self.enter_text(self.SEARCH_INPUT, keyword)

    def click_search(self):
        self.click(self.SEARCH_BUTTON)

    def results_are_displayed(self):
        return self.is_visible(self.SEARCH_RESULTS_CONTAINER)
