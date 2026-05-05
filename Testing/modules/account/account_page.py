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
    EDIT_BUTTON = (By.XPATH, "//a[contains(., 'CHỈNH SỬA') or contains(., 'Chỉnh sửa') or contains(., 'chỉnh sửa') or contains(., 'CHINH SUA') or contains(., 'Chinh sua')] | //button[contains(., 'CHỈNH SỬA') or contains(., 'Chỉnh sửa') or contains(., 'chỉnh sửa') or contains(., 'CHINH SUA') or contains(., 'Chinh sua')]")
    BACK_HOME_BUTTON = (By.XPATH, "//a[contains(., 'trang chủ') or contains(., 'Trang chủ') or contains(., 'TRANG CHỦ') or contains(., 'TRANG CHU') or contains(., 'trang chu') or contains(., 'Trang chu')] | //button[contains(., 'trang chủ') or contains(., 'Trang chủ') or contains(., 'TRANG CHỦ') or contains(., 'TRANG CHU') or contains(., 'trang chu') or contains(., 'Trang chu')]")
    BACK_BUTTON = (By.XPATH, "//a[contains(., 'QUAY LẠI') or contains(., 'Quay lại') or contains(., 'Quay lai')] | //button[contains(., 'QUAY LẠI') or contains(., 'Quay lại') or contains(., 'Quay lai')]")
    CANCEL_BUTTON = (By.XPATH, "//a[contains(., 'HỦY') or contains(., 'Hủy') or contains(., 'Huy')] | //button[contains(., 'HỦY') or contains(., 'Hủy') or contains(., 'Huy')]")
    
    # SweetAlert2 Locators
    SWAL_CONFIRM_BUTTON = (By.CSS_SELECTOR, "button.swal2-confirm")
    SWAL_CANCEL_BUTTON = (By.CSS_SELECTOR, "button.swal2-cancel")
    SWAL_SUCCESS_OK = (By.CSS_SELECTOR, "button.swal2-confirm") # Usually the same
    LOGOUT_BUTTON = (By.LINK_TEXT, "ĐĂNG XUẤT")
    ACCOUNT_MENU = (By.CSS_SELECTOR, ".bi-person-circle")
    # Hỗ trợ tìm kiếm theo cả text và theo href link ẩn bên dưới
    PROFILE_LINK = (By.XPATH, "//a[contains(., 'Thông tin tài khoản') or contains(., 'Quản lý tài khoản') or contains(., 'Quan ly tai khoan') or contains(@href, 'Profile') or contains(@href, 'Account') or contains(@href, 'KhachHang')]")



    def update_profile(self, data):
        """Updates profile fields."""
        # Chuyển tất cả keys về chữ thường để dễ so sánh
        data_lower = {k.lower(): v for k, v in data.items()}
        
        fullname = next((v for k, v in data_lower.items() if 'tên' in k or 'ten' in k), None)
        if fullname is not None:
            self.enter_text(self.FULLNAME_INPUT, fullname)
            
        email = next((v for k, v in data_lower.items() if 'email' in k or 'mail' in k), None)
        if email is not None:
            self.enter_text(self.EMAIL_INPUT, email)
            
        address = next((v for k, v in data_lower.items() if 'địa chỉ' in k or 'dia chi' in k), None)
        if address is not None:
            self.enter_text(self.ADDRESS_INPUT, address)
            
        phone = next((v for k, v in data_lower.items() if 'điện thoại' in k or 'sdt' in k or 'sđt' in k or 'dien thoai' in k), None)
        if phone is not None:
            self.enter_text(self.PHONE_INPUT, phone)
            
        birthday = next((v for k, v in data_lower.items() if 'ngày sinh' in k or 'ngay sinh' in k or 'ngaysinh' in k), None)
        if birthday is not None:
            self.enter_text(self.BIRTHDAY_INPUT, birthday)
            
        gender = next((v for k, v in data_lower.items() if 'giới tính' in k or 'gioi tinh' in k or 'gioitinh' in k), None)
        if gender is not None:
            self.enter_text(self.GENDER_INPUT, gender)
            
        password = next((v for k, v in data_lower.items() if 'mật khẩu' in k or 'mk' in k or 'mat khau' in k), None)
        if password is not None:
             self.enter_text(self.PASSWORD_INPUT, password)

    def click_save(self):
        try:
            self.click(self.SAVE_BUTTON)
        except:
            try:
                elem = self.driver.find_element(*self.SAVE_BUTTON)
                self.driver.execute_script("arguments[0].click();", elem)
            except:
                print("Could not click SAVE_BUTTON via selenium or JS")
        
    def handle_swal_confirmation(self):
        """Handles the SweetAlert2 popup."""
        # Wait a bit for Swal to appear
        time.sleep(1)
        try:
            if self.is_visible(self.SWAL_CONFIRM_BUTTON):
                self.click(self.SWAL_CONFIRM_BUTTON)
                return True, "Đã xác nhận lưu thay đổi trên SweetAlert2"
        except:
            try:
                elem = self.driver.find_element(*self.SWAL_CONFIRM_BUTTON)
                self.driver.execute_script("arguments[0].click();", elem)
                return True, "Đã xác nhận lưu thay đổi trên SweetAlert2 bằng JS"
            except:
                pass
        return False, "Không tìm thấy hoặc không thể click nút xác nhận SweetAlert2"

    def handle_swal_cancel(self):
        """Handles the Cancel action on SweetAlert2 popup."""
        time.sleep(1)
        try:
            if self.is_visible(self.SWAL_CANCEL_BUTTON):
                self.click(self.SWAL_CANCEL_BUTTON)
                return True, "Đã nhấn nút Hủy trên SweetAlert2"
        except:
            try:
                elem = self.driver.find_element(*self.SWAL_CANCEL_BUTTON)
                self.driver.execute_script("arguments[0].click();", elem)
                return True, "Đã nhấn nút Hủy trên SweetAlert2 bằng JS"
            except:
                pass
        return False, "Không tìm thấy hoặc không thể click nút Hủy trên SweetAlert2"
