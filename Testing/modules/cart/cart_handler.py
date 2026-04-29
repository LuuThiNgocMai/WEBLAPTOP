from .cart_page import CartPage

class CartHandler:
    """Handles logic for the Cart module."""
    
    def __init__(self, driver):
        self.page = CartPage(driver)

    def execute_action(self, action_name, step_info, test_data_ai, env_config=None):
        action_name = action_name.lower()
        
        if "them_vao_gio_hang" in action_name or "click_bieu_tuong_gio_hang" in action_name:
            self.page.click_add_to_cart_first_item()
            return True, "Đã thêm sản phẩm vào giỏ hàng"
            
        elif "mo_gio_hang" in action_name or "vao_trang_gio_hang" in action_name:
            self.page.open_cart()
            success = self.page.wait_for_cart_page()
            return success, "Đã mở giỏ hàng"
            
        elif "tang_so_luong" in action_name or "click_nut_plus" in action_name:
            self.page.increment_quantity()
            return True, "Đã tăng số lượng sản phẩm"
            
        elif "giam_so_luong" in action_name or "click_nut_minus" in action_name:
            self.page.decrement_quantity()
            return True, "Đã giảm số lượng sản phẩm"
            
        elif "xoa_san_pham" in action_name or "click_nut_x" in action_name:
            self.page.remove_first_product()
            return True, "Đã xóa sản phẩm khỏi giỏ hàng"
            
        elif "xoa_tat_ca" in action_name or "xoa_toan_bo" in action_name:
            self.page.clear_all()
            return True, "Đã xóa toàn bộ giỏ hàng"
            
        else:
            return False, f"Hành động '{action_name}' chưa được hỗ trợ trong module Cart"
