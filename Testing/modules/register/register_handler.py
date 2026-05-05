from .register_page import RegisterPage

class RegisterHandler:
    """Handles logic for the Registration module."""
    
    def __init__(self, driver):
        self.page = RegisterPage(driver)

    def execute_action(self, action_name, step_info, test_data_ai, env_config=None):
        action_name = action_name.lower()
        
        if "nhap_thong_tin" in action_name or "dien_form" in action_name:
            # Map test_data_ai to form fields
            self.page.register(test_data_ai)
            return True, "Đã nhập thông tin đăng ký"
            
        elif "dang_ky_ngay" in action_name or "đang_ky_ngay" in action_name:
            try:
                self.page.click(self.page.REGISTER_NOW_LINK)
            except:
                try:
                    elem = self.page.driver.find_element(*self.page.REGISTER_NOW_LINK)
                    self.page.driver.execute_script("arguments[0].click();", elem)
                except:
                    return False, "Không tìm thấy nút Đăng ký ngay trên trang"
            return True, "Đã chọn Đăng ký ngay từ màn hình Đăng nhập"
            
        elif "nhan_dang_ky" in action_name or "click_dang_ky" in action_name or "bam_dang_ky" in action_name or "click_đang_ky" in action_name:
            self.page.click_submit()
            return True, "Đã nhấn nút Đăng ký"
            
        elif any(k in action_name for k in ["nhap", "dien", "de_trong", "bo_trong", "trong", "khong_chon"]):
            # Generic field entry or clearing
            self.page.register(test_data_ai)
            return True, f"Thực hiện hành động dữ liệu: {action_name}"


        elif "avatar" in action_name or "bieu_tuong" in action_name:
            try:
                self.page.click(self.page.ACCOUNT_MENU)
            except:
                try:
                    elem = self.page.driver.find_element(*self.page.ACCOUNT_MENU)
                    self.page.driver.execute_script("arguments[0].click();", elem)
                except:
                    # Nếu đang ở trang không có avatar (ví dụ màn đăng nhập/đăng ký riêng biệt), báo Failed an toàn
                    return False, "Không tìm thấy biểu tượng avatar trên giao diện hiện tại"
            return True, "Đã nhấn vào biểu tượng avatar tài khoản"
            
        elif "chon_dang_ky" in action_name or ("chon" in action_name and "dang_ky" in action_name):
            try:
                self.page.click(self.page.REGISTER_LINK)
            except:
                try:
                    elem = self.page.driver.find_element(*self.page.REGISTER_LINK)
                    self.page.driver.execute_script("arguments[0].click();", elem)
                except:
                    return False, "Không tìm thấy menu Đăng ký trên giao diện"
            return True, "Đã chọn Đăng ký từ menu"

        elif "dang_xuat" in action_name or "click_dang_xuat" in action_name:
            try:
                self.page.click(self.page.LOGOUT_BUTTON)
            except:
                try:
                    elem = self.page.driver.find_element(*self.page.LOGOUT_BUTTON)
                    self.page.driver.execute_script("arguments[0].click();", elem)
                except:
                    return False, "Không tìm thấy nút Đăng xuất trên giao diện"
            return True, "Đã nhấn nút Đăng xuất để xóa session"

        else:
            return False, f"Hành động '{action_name}' chưa được hỗ trợ trong module Register"
