from .account_page import AccountPage

class AccountHandler:
    """Handles logic for the Account Management module."""
    
    def __init__(self, driver):
        self.page = AccountPage(driver)

    def execute_action(self, action_name, step_info, test_data_ai, env_config=None):
        action_name = action_name.lower()
        
        if "cap_nhat" in action_name or "sua_thong_tin" in action_name or "nhap_thong_tin" in action_name:
            self.page.update_profile(test_data_ai)
            return True, "Đã cập nhật thông tin tài khoản"
            
        elif "bam_luu" in action_name or "click_luu" in action_name or "xac_nhan" in action_name:
            self.page.click_save()
            # Handle the SweetAlert2 confirmation that follows
            success, msg = self.page.handle_swal_confirmation()
            return success, msg
            
        elif "doi_mat_khau" in action_name:
            if 'mật khẩu mới' in test_data_ai:
                self.page.update_profile({'mật khẩu mới': test_data_ai['mật khẩu mới']})
                self.page.click_save()
                return self.page.handle_swal_confirmation()
            return False, "Thiếu dữ liệu mật khẩu mới"

        elif "dang_xuat" in action_name or "click_dang_xuat" in action_name:
            # Need to find the logout button, might need to open menu first
            try:
                self.page.click((By.LINK_TEXT, "ĐĂNG XUẤT"))
            except:
                # Fallback if it's hidden in a menu
                self.page.click(self.page.ACCOUNT_MENU)
                self.page.click(self.page.LOGOUT_BUTTON)
            return True, "Đã nhấn đăng xuất"

        else:
            return False, f"Hành động '{action_name}' chưa được hỗ trợ trong module Account"
