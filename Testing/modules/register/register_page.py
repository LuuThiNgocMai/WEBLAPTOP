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
    
    def register(self, data):
        """Fills out the registration form."""
        if 'tên đăng nhập' in data or 'tk' in data:
            self.enter_text(self.USERNAME_INPUT, data.get('tên đăng nhập') or data.get('tk'))
        
        if 'mật khẩu' in data or 'mk' in data:
            self.enter_text(self.PASSWORD_INPUT, data.get('mật khẩu') or data.get('mk'))
            
        if 'họ và tên' in data or 'tenkh' in data:
            self.enter_text(self.FULLNAME_INPUT, data.get('họ và tên') or data.get('tenkh'))
            
        if 'địa chỉ' in data:
            self.enter_text(self.ADDRESS_INPUT, data.get('địa chỉ'))
            
        if 'số điện thoại' in data or 'sdt' in data:
            self.enter_text(self.PHONE_INPUT, data.get('số điện thoại') or data.get('sdt'))
            
        if 'ngày sinh' in data:
            # Note: HTML5 date input usually expects YYYY-MM-DD
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
