from .cart_page import CartPage

class CartHandler:
    """Handles logic for the Cart module."""
    
    def __init__(self, driver):
        self.page = CartPage(driver)

    def execute_action(self, action_name, step_info, test_data_ai, env_config=None):
        action_name = action_name.lower()
        
        if action_name == "them_vao_gio_hang":
            self.page.click_add_to_cart()
            return True, "Đã thêm sản phẩm vào giỏ hàng"
            
        elif action_name == "mo_gio_hang":
            self.page.open_cart()
            success = self.page.wait_for_cart_page()
            return success, "Đã mở giỏ hàng"
            
        elif action_name == "xoa_san_pham_khoi_gio":
            self.page.remove_first_product()
            return True, "Đã xóa sản phẩm khỏi giỏ hàng"
            
        else:
            return False, f"Hành động '{action_name}' chưa được hỗ trợ trong module Cart"
