from .product_page import ProductPage

class ProductHandler:
    """Handles logic for the Product module."""
    
    def __init__(self, driver):
        self.page = ProductPage(driver)

    def execute_action(self, action_name, step_info, test_data_ai, env_config=None):
        action_name = action_name.lower()
        
        if action_name == "chon_san_pham_dau_tien" or "chon_mot_san_pham_bat_ky" in action_name or "san_pham_tren_trang_chu" in action_name:
            self.page.click_first_product()
            return True, "Đã nhấn chọn một sản phẩm trong danh sách"
            
        elif "click_vao_menu" in action_name and "san_pham" in action_name:
            self.page.click_product_menu()
            return True, "Đã nhấn vào menu Sản phẩm"
            
        elif "them_vao_gio_hang" in action_name or "add_to_cart" in action_name:
            self.page.click_add_to_cart()
            return True, "Đã thêm sản phẩm vào giỏ hàng"
            
        elif action_name == "mo_trang_chi_tiet_san_pham":
            # Đây có thể chỉ là một bước kiểm tra hoặc điều hướng trực tiếp
            success = self.page.wait_for_detail_page()
            title = self.page.get_product_title()
            return success, f"Trang chi tiết sản phẩm đã tải: {title}"
            
        elif "san_pham_khong_ton_tai" in action_name or "nhap_url_san_pham_sai" in action_name:
            self.page.navigate_to_product("999999")
            return True, "Đã điều hướng tới link sản phẩm không tồn tại (ID: 999999)"
            
        else:
            return False, f"Hành động '{action_name}' chưa được hỗ trợ trong module Product"
