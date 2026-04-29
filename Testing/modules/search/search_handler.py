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
            
        elif any(k in action_name for k in ["nhap_tu_khoa", "tim_kiem", "nhap_ten", "o_tim_kiem"]):
            # Check for keyword in all possible fields
            keyword = ""
            keys_to_try = ['tu_khoa', 'keyword', 'product_name', 'tên sản phẩm', 'search_query', 'name']
            for k in keys_to_try:
                if k in test_data_ai:
                    keyword = test_data_ai[k]
                    break
            
            # If still empty, check step_info for clues (manual data)
            if not keyword and "Dữ liệu test" in step_info:
                 keyword = step_info["Dữ liệu test"]

            self.page.enter_search_keyword(keyword)
            return True, f"Đã nhập từ khóa tìm kiếm: {keyword if keyword else '(rỗng)'}"
            
        elif action_name == "nhan_nut_tim_kiem" or "tim_kiem" in action_name:
            self.page.click_search()
            return True, "Đã nhấn nút tìm kiếm"
            
        else:
            return False, f"Hành động '{action_name}' chưa được hỗ trợ trong module Search"
