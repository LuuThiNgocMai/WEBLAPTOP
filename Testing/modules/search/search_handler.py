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
            
        # 1. Check for explicit click/submit action
        elif any(k in action_name for k in ["click", "nhan", "bam", "nut_tim_kiem"]):
            self.page.click_search()
            return True, "Đã nhấn nút tìm kiếm"
            
        # 2. Check for explicit input action
        elif any(k in action_name for k in ["nhap", "dien", "go_tu_khoa", "o_tim_kiem", "tu_khoa", "keyword"]):
            # Check for keyword in all possible fields
            keyword = ""
            # Expanded keys to try (including Vietnamese and common technical terms)
            keys_to_try = [
                'tu_khoa', 'keyword', 'product_name', 'tên sản phẩm', 'ten_san_pham', 
                'search_query', 'name', 'tên danh mục', 'ten_danh_muc', 'danh_muc'
            ]
            
            # Check step_info for manual data from Excel first
            if "Dữ liệu test" in step_info and step_info["Dữ liệu test"]:
                 keyword = step_info["Dữ liệu test"]
            
            # If still empty, check AI generated data
            if not keyword:
                for k in keys_to_try:
                    if k in test_data_ai:
                        keyword = test_data_ai[k]
                        break
            
            self.page.enter_search_keyword(keyword)
            return True, f"Đã nhập từ khóa tìm kiếm: {keyword if keyword else '(rỗng)'}"
            
        # 3. Fallback for generic "Tìm kiếm" or steps containing "tim_kiem" but not specific to input/click
        elif "tim_kiem" in action_name:
            # Check if there's a keyword to enter as a precaution
            keyword = ""
            keys_to_try = [
                'tu_khoa', 'keyword', 'product_name', 'tên sản phẩm', 'ten_san_pham', 
                'search_query', 'name', 'tên danh mục', 'ten_danh_muc', 'danh_muc'
            ]
            
            # Manual data from Excel
            if "Dữ liệu test" in step_info and step_info["Dữ liệu test"]:
                 keyword = step_info["Dữ liệu test"]
            
            # AI data
            if not keyword:
                for k in keys_to_try:
                    if k in test_data_ai:
                        keyword = test_data_ai[k]
                        break
            
            # If we found a keyword and the action name doesn't explicitly say "click", 
            # we can try to input it. If it was already input in a previous step, this is just a redundant but safe action.
            if keyword and not any(k in action_name for k in ["click", "nhan", "bam"]):
                self.page.enter_search_keyword(keyword)
                
            self.page.click_search()
            return True, "Đã thực hiện tìm kiếm"
            
        else:
            return False, f"Hành động '{action_name}' chưa được hỗ trợ trong module Search"
