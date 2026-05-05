from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logging.getLogger(self.__class__.__name__)

    def find_element(self, locator):
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            self.logger.error(f"Element not found within timeout: {locator}")
            return None

    def click(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            # Scroll to element to ensure it's not blocked by fixed headers/chatbots
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.1)
            element.click()
        except Exception as e:
            self.logger.warning(f"Standard click failed for {locator}, trying JS click. Error: {str(e)}")
            self.click_js(locator)

    def click_js(self, locator):
        element = self.find_element(locator)
        if element:
            self.driver.execute_script("arguments[0].click();", element)
        else:
            raise NoSuchElementException(f"Cannot JS click, element not found: {locator}")

    def enter_text(self, locator, text):
        element = self.find_element(locator)
        if element:
            element.clear()
            # Ensure text is not None to avoid 'NoneType object is not iterable' error
            element.send_keys(str(text) if text is not None else "")
        else:
            raise NoSuchElementException(f"Cannot enter text, element not found: {locator}")

    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text if element else ""

    def is_visible(self, locator, timeout=None):
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_seconds(self, seconds):
        import time
        time.sleep(seconds)

    def get_formatted_url(self, base_url, auth_config=None):
        """
        Formats the URL with Basic Auth credentials if provided.
        """
        if not auth_config or not auth_config.get('use_auth'):
            return base_url

        user = auth_config.get('username', '')
        password = auth_config.get('password', '')
        
        if not user or not password:
            return base_url

        # Inject user:pass into the URL
        if "://" in base_url:
            protocol, rest = base_url.split("://", 1)
            return f"{protocol}://{user}:{password}@{rest}"
        
        return base_url
