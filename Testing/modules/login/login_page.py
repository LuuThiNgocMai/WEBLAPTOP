from selenium.webdriver.common.by import By
from core.base_page import BasePage
from config import URL_CONFIG

class LoginPage(BasePage):
    """Page Object for Login Page of the laptop store."""
    
    # Locators (Updated for local MVC site)
    EMAIL_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_SUCCESS_INDICATOR = (By.CSS_SELECTOR, ".bi-person-circle")
    GOOGLE_LOGIN_BUTTON = (By.CLASS_NAME, "btn-google")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Quên mật khẩu")
    SIGNUP_LINK = (By.LINK_TEXT, "Đăng ký ngay")



    def navigate_to_login(self, env_config=None):
        url = URL_CONFIG.get("login", "https://localhost:44396/Login")
        
        if env_config and env_config.get('target_url'):
            url = env_config.get('target_url')

        final_url = self.get_formatted_url(url, env_config.get('auth') if env_config else None)
        self.driver.get(final_url)

    def enter_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def is_logged_in(self):
        return self.is_visible(self.LOGIN_SUCCESS_INDICATOR)

    def click_google_login(self):
        self.click(self.GOOGLE_LOGIN_BUTTON)

    def click_forgot_password(self):
        self.click(self.FORGOT_PASSWORD_LINK)

    def click_signup(self):
        self.click(self.SIGNUP_LINK)

