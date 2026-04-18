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
            
        elif "nhan_dang_ky" in action_name or "click_dang_ky" in action_name or "bam_dang_ky" in action_name:
            self.page.click_submit()
            return True, "Đã nhấn nút Đăng ký"
            
        elif "nhap" in action_name:
            # Generic single field entry if needed
            self.page.register(test_data_ai)
            return True, f"Thực hiện nhập dữ liệu: {action_name}"

        else:
            return False, f"Hành động '{action_name}' chưa được hỗ trợ trong module Register"
