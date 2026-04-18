from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def create_driver(headless=False, implicit_wait=10, page_load_timeout=30):
    """
    Initializes a Chrome WebDriver with specific configurations.
    """
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("detach", True)

    # Initialize Driver (Assumes chromedriver is in PATH or handled by system)
    # For a more robust approach, use webdriver-manager
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(implicit_wait)
        driver.set_page_load_timeout(page_load_timeout)
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        raise e
