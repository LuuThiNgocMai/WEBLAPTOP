from .login_page import LoginPage
from selenium.webdriver.common.by import By

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
            
        elif "nhap" in action_name and ("ten_dang_nhap" in action_name or "email" in action_name) and ("mat_khau" in action_name or "password" in action_name):
            # Combined step: "Nhập tên đăng nhập và mật khẩu"
            email = ""
            password = ""
            
            # 1. Manual data check (if formatted as "user|pass" in Excel or similar, but usually we use AI)
            # For combined steps, it's safer to use AI data which has separate fields.
            
            # 2. Get data from AI
            keys_user = ['email', 'tên đăng nhập', 'username', 'login_id', 'user']
            for k in keys_user:
                if k in test_data_ai:
                    email = test_data_ai[k]
                    break
            
            keys_pass = ['password', 'mật khẩu', 'mat_khau', 'pass']
            for k in keys_pass:
                if k in test_data_ai:
                    password = test_data_ai[k]
                    break
            
            self.page.enter_email(email)
            self.page.enter_password(password)
            return True, f"Đã nhập cả tên đăng nhập và mật khẩu"

        elif action_name == "nhap_email" or "nhap_ten_dang_nhap" in action_name:
            # Flexible key lookup for username/email
            keys_to_try = ['email', 'tên đăng nhập', 'username', 'login_id', 'user']
            email = ""
            
            # 1. Prioritize manual data from Excel if available for this specific step
            manual_data = step_info.get("Dữ liệu test", "").strip()
            if manual_data:
                 email = manual_data
                 print(f"[LoginHandler] Sử dụng dữ liệu thủ công cho Email: {email}")
            
            # 2. Otherwise use AI generated data
            if not email:
                for k in keys_to_try:
                    if k in test_data_ai:
                        email = test_data_ai[k]
                        print(f"[LoginHandler] Sử dụng dữ liệu AI cho Email ({k}): {email}")
                        break
                    
                if not email and email != "": 
                     for k, v in test_data_ai.items():
                         if any(sub in k.lower() for sub in ['tên', 'email', 'user']):
                             email = v
                             print(f"[LoginHandler] Sử dụng dữ liệu AI (fuzzy match) cho Email: {email}")
                             break

            self.page.enter_email(email)
            return True, f"Đã nhập thông tin đăng nhập: {email if email else '(rỗng)'}"
            
        elif action_name == "nhap_mat_khau" or "mat_khau" in action_name:
            keys_to_try = ['password', 'mật khẩu', 'mat_khau', 'pass']
            password = ""
            
            # 1. Prioritize manual data from Excel
            manual_data = step_info.get("Dữ liệu test", "").strip()
            if manual_data:
                 password = manual_data
                 print(f"[LoginHandler] Sử dụng dữ liệu thủ công cho Password")
            
            # 2. Use AI data
            if not password:
                for k in keys_to_try:
                    if k in test_data_ai:
                        password = test_data_ai[k]
                        print(f"[LoginHandler] Sử dụng dữ liệu AI cho Password ({k})")
                        break
            
            self.page.enter_password(password)
            return True, "Đã nhập mật khẩu"
            
        elif action_name in ["nhan_nut_dang_nhap", "click_nut_dang_nhap", "bam_nut_dang_nhap", "dang_nhap_he_thong"]:
            self.page.click_login()
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
            
        elif "avatar" in action_name or "bieu_tuong" in action_name:
            print(f"[LoginHandler] Đang ở URL: {self.page.driver.current_url}")
            # 1. Nếu đã ở trang Đăng nhập rồi thì bỏ qua để tránh lỗi
            if "/Login" in self.page.driver.current_url:
                return True, "Đã ở trang đăng nhập, bỏ qua bước click avatar"

            import time
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            
            avatar_locator = (By.CSS_SELECTOR, ".bi-person-circle")
            try:
                # Tìm icon và thử click vào thẻ cha của nó (thường là thẻ <a> hoặc <button>)
                icon = self.page.driver.find_element(*avatar_locator)
                self.page.driver.execute_script("arguments[0].click();", icon)
                time.sleep(0.5)
            except:
                # Fallback: click theo tọa độ hoặc nút text
                try:
                    btn = self.page.driver.find_element(By.LINK_TEXT, "Đăng nhập")
                    btn.click()
                except:
                    # Nếu vẫn không được, điều hướng thẳng
                    self.page.navigate_to_login(env_config)
            
            # Chờ trang Login xuất hiện (chờ id=username xuất hiện là chắc nhất)
            try:
                WebDriverWait(self.page.driver, 5).until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
                print(f"[LoginHandler] Đã chuyển sang trang đăng nhập thành công")
            except:
                print(f"[LoginHandler] Cảnh báo: Chưa thấy ô 'username' sau khi click avatar")

            return True, "Đã nhấn vào biểu tượng avatar tài khoản"
            
        elif "dang_xuat" in action_name or "logout" in action_name:
            # Try finding logout link by text or common selectors
            logout_selectors = [
                (By.LINK_TEXT, "Đăng xuất"),
                (By.LINK_TEXT, "Dang xuat"),
                (By.XPATH, "//a[contains(text(), 'Đăng xuất') or contains(text(), 'Dang xuat')]"),
                (By.CSS_SELECTOR, "a[href*='Logout']")
            ]
            
            for selector in logout_selectors:
                try:
                    self.page.click(selector)
                    return True, "Đã nhấn nút Đăng xuất"
                except:
                    continue
            return False, "Không tìm thấy nút Đăng xuất"

        else:
            return False, f"Hành động '{action_name}' chưa được hỗ trợ trong module Login"
