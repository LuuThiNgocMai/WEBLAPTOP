from .checkout_page import CheckoutPage

class CheckoutHandler:
    """Handles logic for the Checkout module."""
    
    def __init__(self, driver):
        self.page = CheckoutPage(driver)

    def execute_action(self, action_name, step_info, test_data_ai, env_config=None):
        action_name = action_name.lower()
        
        if action_name == "nhan_thanh_toan":
            self.page.click_checkout()
            return True, "Đã nhấn nút tiến hành thanh toán"
            
        elif action_name == "nhập_thông_tin_giao_hàng" or action_name == "nhap_thong_tin_giao_hang":
            name = test_data_ai.get('full_name', 'Khách')
            address = test_data_ai.get('address', 'Địa chỉ mặc định')
            phone = test_data_ai.get('phone', '0123456789')
            self.page.enter_shipping_info(name, address, phone)
            return True, "Đã nhập thông tin giao hàng"
            
        elif action_name == "xác_nhận_đặt_hàng" or action_name == "xac_nhan_dat_hang":
            self.page.click_confirm()
            return True, "Đã nhấn nút xác nhận đặt hàng"
            
        else:
            return False, f"Hành động '{action_name}' chưa được hỗ trợ trong module Checkout"
