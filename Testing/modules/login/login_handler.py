from .login_page import LoginPage

class LoginHandler:
    """Handles logic for the Login module."""
    
    def __init__(self, driver):
        self.page = LoginPage(driver)

    def execute_action(self, action_name, step_info, test_data_ai, env_config=None):
        """
        Maps a high-level action name to a sequence of Page Object calls.
        """
        action_name = action_name.lower()
        if env_config is None: env_config = {}
        
        if action_name == "mo_trang_dang_nhap":
            self.page.navigate_to_login(env_config)
            return True, "Đã mở trang đăng nhập"
            
        elif action_name == "nhap_email":
            email = test_data_ai.get('email', '')
            if not email:
                return False, "Thiếu dữ liệu email trong test data"
            self.page.enter_email(email)
            return True, f"Đã nhập email: {email}"
            
        elif action_name == "nhap_mat_khau":
            password = test_data_ai.get('password', '')
            if not password:
                return False, "Thiếu dữ liệu mật khẩu trong test data"
            self.page.enter_password(password)
            return True, "Đã nhập mật khẩu"
            
        elif action_name == "nhan_nut_dang_nhap":
            self.page.click_login()
            # Optional: verify success if needed immediately
            return True, "Đã nhấn nút đăng nhập"
            
        elif "google" in action_name:
            self.page.click_google_login()
            return True, "Đã nhấn nút đăng nhập bằng Google"
            
        elif "quen_mat_khau" in action_name or "forgot" in action_name:
            self.page.click_forgot_password()
            return True, "Đã nhấn link Quên mật khẩu"
            
        elif "dang_ky_ngay" in action_name or "signup" in action_name:
            self.page.click_signup()
            return True, "Đã nhấn link Đăng ký ngay"
            
        else:
            return False, f"Hành động '{action_name}' chưa được hỗ trợ trong module Login"
