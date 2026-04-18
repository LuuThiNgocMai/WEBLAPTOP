from selenium.webdriver.common.by import By
from core.base_page import BasePage
import time

class AccountPage(BasePage):
    """Page Object for the Account Management (Profile) page."""
    
    # Locators (from Profile/Edit.cshtml)
    FULLNAME_INPUT = (By.ID, "TenKH")
    EMAIL_INPUT = (By.ID, "Email")
    ADDRESS_INPUT = (By.ID, "DiaChi")
    PHONE_INPUT = (By.ID, "SDT")
    GENDER_INPUT = (By.ID, "GioTinh")
    BIRTHDAY_INPUT = (By.ID, "NgaySinh")
    PASSWORD_INPUT = (By.ID, "MK")
    SAVE_BUTTON = (By.ID, "saveButton")
    
    # SweetAlert2 Locators
    SWAL_CONFIRM_BUTTON = (By.CSS_SELECTOR, "button.swal2-confirm")
    SWAL_SUCCESS_OK = (By.CSS_SELECTOR, "button.swal2-confirm") # Usually the same

    def update_profile(self, data):
        """Updates profile fields."""
        if 'họ tên' in data or 'tenkh' in data:
            self.enter_text(self.FULLNAME_INPUT, data.get('họ tên') or data.get('tenkh'))
            
        if 'email' in data:
            self.enter_text(self.EMAIL_INPUT, data.get('email'))
            
        if 'địa chỉ' in data:
            self.enter_text(self.ADDRESS_INPUT, data.get('địa chỉ'))
            
        if 'số điện thoại' in data or 'sdt' in data:
            self.enter_text(self.PHONE_INPUT, data.get('số điện thoại') or data.get('sdt'))
            
        if 'mật khẩu mới' in data or 'mk' in data:
             self.enter_text(self.PASSWORD_INPUT, data.get('mật khẩu mới') or data.get('mk'))

    def click_save(self):
        self.click(self.SAVE_BUTTON)
        
    def handle_swal_confirmation(self):
        """Handles the SweetAlert2 popup."""
        # Wait a bit for Swal to appear
        time.sleep(1)
        if self.is_visible(self.SWAL_CONFIRM_BUTTON):
            self.click(self.SWAL_CONFIRM_BUTTON)
            return True, "Đã xác nhận lưu thay đổi trên SweetAlert2"
        return False, "Không tìm thấy nút xác nhận SweetAlert2"
