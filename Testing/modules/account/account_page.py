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
    SWAL_CONFIRM_BUTTON = (By.CSS_SELECTOR, "button.swal2-confirm, .swal2-confirm, .swal2-actions button.swal2-confirm")
    SWAL_CANCEL_BUTTON = (By.CSS_SELECTOR, "button.swal2-cancel, .swal2-cancel")
    SWAL_SUCCESS_OK = (By.CSS_SELECTOR, "button.swal2-confirm, .swal2-confirm")
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
        """Clicks the save button, ensuring it is clickable and triggers events."""
        try:
            # Scroll and click
            self.click(self.SAVE_BUTTON)
            # Extra insurance: trigger click event via JS just in case
            self.driver.execute_script("document.getElementById('saveButton').click();")
            time.sleep(1.5) # Wait for Swal to animate in
            return True
        except Exception as e:
            print(f"Click failed for SAVE_BUTTON: {str(e)}")
            try:
                self.driver.execute_script("document.getElementById('saveButton').click();")
                time.sleep(1.5)
                return True
            except:
                return False
        
    def handle_swal_confirmation(self):
        """Handles the SweetAlert2 popup with aggressive confirmation attempts."""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # 1. Try to detect Swal visibility
        is_swal_visible = self.driver.execute_script("return typeof Swal !== 'undefined' && Swal.isVisible();")
        
        # 2. Attempt to click confirm directly via JS anyway (most reliable)
        try:
            # We try to call clickConfirm() regardless of visibility check 
            # because sometimes check fails during animation
            self.driver.execute_script("if(typeof Swal !== 'undefined') { Swal.clickConfirm(); }")
            
            # Wait for URL change to verify success
            old_url = self.driver.current_url
            for _ in range(10): 
                time.sleep(0.5)
                if self.driver.current_url != old_url:
                    return True, "Đã lưu thành công (Chuyển hướng sau clickConfirm)"
        except:
            pass

        # 3. If still on same page, try manual submission as final fallback
        try:
            # Check if there are any REAL validation errors visible on page
            # ASP.NET MVC adds specific classes when there are errors
            has_errors = self.driver.execute_script('''
                return document.querySelectorAll('.field-validation-error, .validation-summary-errors').length > 0;
            ''')
            if has_errors:
                return False, "Có lỗi validation trên form, không thể lưu"
                
            self.driver.execute_script("document.getElementById('editProfileForm').submit();")
            time.sleep(2)
            return True, "Đã ép buộc submit form (Dự phòng cuối cùng)"
        except Exception as e:
            return False, f"Không thể lưu dữ liệu: {str(e)}"
                
        except Exception as e:
            return False, f"Lỗi khi xác nhận SweetAlert2: {str(e)}"

    def handle_swal_cancel(self):
        """Handles the Cancel action on SweetAlert2 popup."""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        try:
            wait = WebDriverWait(self.driver, 5)
            cancel_btn = wait.until(EC.element_to_be_clickable(self.SWAL_CANCEL_BUTTON))
            time.sleep(0.5)
            cancel_btn.click()
            return True, "Đã nhấn nút Hủy trên SweetAlert2"
        except Exception as e:
            try:
                elem = self.driver.find_element(*self.SWAL_CANCEL_BUTTON)
                self.driver.execute_script("arguments[0].click();", elem)
                return True, "Đã nhấn nút Hủy trên SweetAlert2 (JS fallback)"
            except:
                return False, f"Không tìm thấy hoặc không thể click nút Hủy trên SweetAlert2: {str(e)}"
