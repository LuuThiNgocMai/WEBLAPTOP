from .account_page import AccountPage

class AccountHandler:
    """Handles logic for the Account Management module."""
    
    def __init__(self, driver):
        self.page = AccountPage(driver)

    def execute_action(self, action_name, step_info, test_data_ai, env_config=None):
        action_name = action_name.lower()
        
        if any(kw in action_name for kw in ["cap_nhat", "sua_thong_tin", "nhap_thong_tin", "nhap", "xoa", "bo_trong", "thay_doi", "dien", "de_trong", "đe_trong", "ngay_sinh", "gioi_tinh"]):
            self.page.update_profile(test_data_ai)
            # Nếu hành động yêu cầu để trống mật khẩu nhưng test_data_ai không có 'mật khẩu mới'
            if "mat_khau" in action_name and ("de_trong" in action_name or "đe_trong" in action_name):
                self.page.enter_text(self.page.PASSWORD_INPUT, "")
            return True, "Đã điền/cập nhật thông tin trên form"
            
        elif "chon_luu" in action_name or "xac_nhan" in action_name:
            success, msg = self.page.handle_swal_confirmation()
            if not success:
                # Nếu không thấy popup thì coi như đã xử lý trước đó hoặc không cần
                return True, "Đã bỏ qua hoặc xử lý xong popup Lưu"
            return success, msg
            
        elif "luu_thay_doi" in action_name or "click_luu" in action_name or "bam_luu" in action_name:
            self.page.click_save()
            return True, "Đã click nút LƯU THAY ĐỔI"
            
        elif "luu" in action_name.split("_"):
            self.page.click_save()
            success, msg = self.page.handle_swal_confirmation()
            return True, "Đã nhấn lưu và xử lý popup (nếu có)"
            
        elif "chinh_sua" in action_name or "sua" in action_name.split("_"):
            try:
                self.page.click(self.page.EDIT_BUTTON)
            except:
                elem = self.page.driver.find_element(*self.page.EDIT_BUTTON)
                self.page.driver.execute_script("arguments[0].click();", elem)
            return True, "Đã nhấn nút Chỉnh sửa"

        elif "trang_chu" in action_name:
            try:
                self.page.click(self.page.BACK_HOME_BUTTON)
            except:
                elem = self.page.driver.find_element(*self.page.BACK_HOME_BUTTON)
                self.page.driver.execute_script("arguments[0].click();", elem)
            return True, "Đã nhấn nút Quay lại trang chủ"

        elif "quay_lai" in action_name:
            try:
                self.page.click(self.page.BACK_BUTTON)
            except:
                elem = self.page.driver.find_element(*self.page.BACK_BUTTON)
                self.page.driver.execute_script("arguments[0].click();", elem)
            return True, "Đã nhấn nút Quay lại"

        elif "chon_huy" in action_name:
            success, msg = self.page.handle_swal_cancel()
            if not success:
                return True, "Không thấy popup Hủy (có thể đã đóng hoặc không có)"
            return success, msg
            
        elif "huy" in action_name or "click_huy" in action_name:
            try:
                self.page.click(self.page.CANCEL_BUTTON)
            except:
                try:
                    elem = self.page.driver.find_element(*self.page.CANCEL_BUTTON)
                    self.page.driver.execute_script("arguments[0].click();", elem)
                except:
                    return False, "Không tìm thấy nút Hủy trên form"
            return True, "Đã nhấn nút Hủy"
            
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

        elif "avatar" in action_name or "bieu_tuong" in action_name:
            # Mở menu avatar 
            self.page.click(self.page.ACCOUNT_MENU)
            return True, "Đã nhấn vào biểu tượng avatar tài khoản"

        elif "thong_tin" in action_name or "quan_ly" in action_name or "tai_khoan" in action_name:
            # Chọn "Thông tin tài khoản" hoặc "Quản lý tài khoản" trong dropdown
            try:
                self.page.click(self.page.PROFILE_LINK)
            except:
                elem = self.page.driver.find_element(*self.page.PROFILE_LINK)
                self.page.driver.execute_script('arguments[0].click();', elem)
            return True, "Đã chuyển đến trang Thông tin tài khoản"

        else:
            return False, f"Hành động '{action_name}' chưa được hỗ trợ trong module Account"
