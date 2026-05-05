from selenium.webdriver.common.by import By
from core.base_page import BasePage

class RegisterPage(BasePage):
    """Page Object for the Registration page in the ASP.NET MVC app."""
    
    # Locators (Names/IDs from SignUp/Index.cshtml)
    USERNAME_INPUT = (By.NAME, "TK")
    PASSWORD_INPUT = (By.NAME, "MK")
    FULLNAME_INPUT = (By.NAME, "TenKH")
    ADDRESS_INPUT = (By.NAME, "DiaChi")
    PHONE_INPUT = (By.NAME, "SDT")
    BIRTHDAY_INPUT = (By.NAME, "NgaySinh")
    EMAIL_INPUT = (By.NAME, "Email")
    GENDER_MALE = (By.ID, "male")
    GENDER_FEMALE = (By.ID, "female")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # Navigation Locators
    ACCOUNT_MENU = (By.CSS_SELECTOR, ".bi-person-circle")
    REGISTER_LINK = (By.XPATH, "//a[contains(., 'Đăng ký') or contains(., 'Đăng kí') or contains(@href, 'SignUp')]")
    REGISTER_NOW_LINK = (By.XPATH, "//a[contains(text(), 'Đăng ký ngay')] | //a[contains(@href, 'SignUp')]")
    LOGOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'ĐĂNG XUẤT') or contains(text(), 'Đăng xuất') or contains(., 'Đăng xuất')]")
    
    def register(self, data):
        """Fills out the registration form."""
        if data is None:
            return
            
        if 'tên đăng nhập' in data or 'tk' in data:
            val = data.get('tên đăng nhập') if 'tên đăng nhập' in data else data.get('tk')
            self.enter_text(self.USERNAME_INPUT, val)
        
        if 'mật khẩu' in data or 'mk' in data:
            val = data.get('mật khẩu') if 'mật khẩu' in data else data.get('mk')
            self.enter_text(self.PASSWORD_INPUT, val)
            
        if 'họ và tên' in data or 'tenkh' in data:
            val = data.get('họ và tên') if 'họ và tên' in data else data.get('tenkh')
            self.enter_text(self.FULLNAME_INPUT, val)
            
        if 'địa chỉ' in data:
            self.enter_text(self.ADDRESS_INPUT, data.get('địa chỉ'))
            
        if 'số điện thoại' in data or 'sdt' in data:
            val = data.get('số điện thoại') if 'số điện thoại' in data else data.get('sdt')
            self.enter_text(self.PHONE_INPUT, val)
            
        if 'ngày sinh' in data:
            self.enter_text(self.BIRTHDAY_INPUT, data.get('ngày sinh'))
            
        if 'email' in data:
            self.enter_text(self.EMAIL_INPUT, data.get('email'))

            
        if 'giới tính' in data:
            gender = str(data.get('giới tính')).lower()
            if 'nam' in gender:
                self.click(self.GENDER_MALE)
            else:
                self.click(self.GENDER_FEMALE)
                
    def click_submit(self):
        self.click(self.SUBMIT_BUTTON)
