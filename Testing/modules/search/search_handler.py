from .search_page import SearchPage

class SearchHandler:
    """Handles logic for the Search module."""
    
    def __init__(self, driver):
        self.page = SearchPage(driver)

    def execute_action(self, action_name, step_info, test_data_ai, env_config=None):
        action_name = action_name.lower()
        if env_config is None: env_config = {}
        
        if action_name == "mo_trang_chu":
            self.page.navigate_to_home(env_config)
            return True, "Đã mở trang chủ"
            
        elif any(k in action_name for k in ["nhap_tu_khoa_tim_kiem", "nhap_ten_san_pham", "o_tim_kiem"]):
            keyword = test_data_ai.get('tu_khoa') or test_data_ai.get('keyword') or test_data_ai.get('product_name') or test_data_ai.get('tên sản phẩm') or 'laptop'
            self.page.enter_search_keyword(keyword)
            return True, f"Đã nhập từ khóa tìm kiếm: {keyword}"
            
        elif action_name == "nhan_nut_tim_kiem" or "tim_kiem" in action_name:
            self.page.click_search()
            return True, "Đã nhấn nút tìm kiếm"
            
        else:
            return False, f"Hành động '{action_name}' chưa được hỗ trợ trong module Search"
