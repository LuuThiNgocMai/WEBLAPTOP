import time
from .cart_page import CartPage

class CartHandler:
    """Handles logic for the Cart module."""
    
    def __init__(self, driver):
        self.page = CartPage(driver)

    def execute_action(self, action_name, step_info, test_data_ai, env_config=None):
        action_name = action_name.lower()
        
        if "them_vao_gio_hang" in action_name or "click_bieu_tuong_gio_hang" in action_name:
            so_luong = test_data_ai.get('số lượng', test_data_ai.get('so_luong'))
            if so_luong:
                try:
                    times = int(so_luong)
                except ValueError:
                    times = 3 if "nhieu_lan" in action_name else 1
            else:
                times = 3 if "nhieu_lan" in action_name else 1
                
            p_name = test_data_ai.get('ma_san_pham', test_data_ai.get('tên sản phẩm', ''))
            original_url = self.page.driver.current_url
            
            for i in range(times):
                if p_name:
                    if i > 0 or (i == 0 and not "/Details" in self.page.driver.current_url and not "/Product" in self.page.driver.current_url):
                        from config import BASE_URL
                        if i > 0:
                            self.page.driver.get(BASE_URL)
                            time.sleep(0.5)
                            
                        from modules.search.search_page import SearchPage
                        s_page = SearchPage(self.page.driver)
                        s_page.enter_search_keyword(p_name)
                        s_page.click_search()
                        time.sleep(0.8)
                        
                        from modules.product.product_page import ProductPage
                        p_page = ProductPage(self.page.driver)
                        try:
                            p_page.click_product_by_name(p_name)
                            time.sleep(0.8)
                        except Exception as e:
                            self.page.logger.warning(f"Failed to click product '{p_name}' in search results: {e}")
                
                try:
                    # Thử selector của trang danh sách trước
                    self.page.click_add_to_cart_first_item()
                except:
                    # Nếu lỗi, thử selector của trang chi tiết
                    from modules.product.product_page import ProductPage
                    p_page = ProductPage(self.page.driver)
                    p_page.click_add_to_cart()
                
                # Sau mỗi lần nhấn, nếu bị redirect sang trang giỏ hàng thì quay lại trang sản phẩm để nhấn tiếp
                if times > 1 and i < times - 1:
                    time.sleep(0.8) # Chờ hiệu ứng/redirect
                    if not p_name and "/Cart" in self.page.driver.current_url:
                        self.page.driver.get(original_url)
                        time.sleep(0.5)
            
            # --- Verification Step ---
            # Chờ trang xử lý AddToCart (redirect có thể mất 1-3s)
            for _ in range(10):
                if "/Cart" in self.page.driver.current_url:
                    break
                time.sleep(0.5)
            
            # Nếu vẫn chưa ở trang giỏ hàng sau 5s, hãy thử mở nó
            if "/Cart" not in self.page.driver.current_url:
                self.page.open_cart()
                time.sleep(1.0)
            
            # Kiểm tra xem có sản phẩm nào trong giỏ hàng không
            if self.page.is_visible(self.page.CART_EMPTY_MESSAGE, timeout=3):
                return False, "LỖI: Đã nhấn thêm vào giỏ hàng nhưng giỏ hàng vẫn trống!"
            
            if not self.page.is_visible(self.page.REMOVE_PRODUCT_BUTTON, timeout=3):
                return False, "LỖI: Không tìm thấy sản phẩm trong giỏ hàng sau khi nhấn thêm."
                
            return True, f"Đã thực hiện nhấn thêm vào giỏ hàng ({times} lần) và xác nhận thành công"
            
        elif "xem_chi_tiet" in action_name:
            from modules.product.product_page import ProductPage
            from selenium.webdriver.common.by import By
            p_name = test_data_ai.get('ma_san_pham', '')
            p_page = ProductPage(self.page.driver)
            
            # Kiểm tra nhanh (2s) nếu sản phẩm có trên trang hiện tại
            locator = (By.XPATH, f"//*[contains(text(), '{p_name}')]")
            if not p_page.is_visible(locator, timeout=2):
                # Nếu không thấy sau 2s, thực hiện tìm kiếm ngay
                from modules.search.search_page import SearchPage
                s_page = SearchPage(self.page.driver)
                s_page.enter_search_keyword(p_name)
                s_page.click_search()
            
            p_page.click_product_by_name(p_name)
            return True, f"Đã nhấn xem chi tiết sản phẩm: {p_name}"
            
        elif "mo_gio_hang" in action_name or "vao_trang_gio_hang" in action_name or "vao_gio_hang" in action_name:
            self.page.open_cart()
            # Đợi ngắn xem có chuyển trang không
            success = self.page.wait_for_cart_page()
            
            if not success:
                # Fallback: Điều hướng trực tiếp bằng URL nếu click không tác dụng
                from config import BASE_URL
                self.page.driver.get(f"{BASE_URL}/Cart")
                success = self.page.wait_for_cart_page()
                
            if success:
                return True, "Đã mở giỏ hàng"
            else:
                current_url = self.page.driver.current_url
                if "Login" in current_url:
                    return False, "LỖI: Không thể vào giỏ hàng vì bị redirect sang trang Đăng nhập. Vui lòng đăng nhập trước."
                return False, f"LỖI: Không thể mở trang giỏ hàng (URL hiện tại: {current_url})"
            
        elif "tang_so_luong" in action_name or "click_nut_plus" in action_name or "+" in action_name or "“+”" in action_name:
            self.page.increment_quantity()
            time.sleep(0.8) # Chờ trang tải lại sau khi submit form tự động
            return True, "Đã tăng số lượng sản phẩm"
            
        elif any(k in action_name for k in ["giam_so_luong", "click_nut_minus", "-", "–", "—", "“_”"]):
            # Trích xuất số mục tiêu nếu có (ví dụ: "đến khi số lượng = 1")
            import re
            target_match = re.search(r"=\s*(\d+)", action_name) or re.search(r"xuong\s*(\d+)", action_name)
            target_qty = int(target_match.group(1)) if target_match else 0
            
            if "lien_tuc" in action_name or "den_khi" in action_name:
                count = 0
                while count < 15: # Safety limit
                    # Thử lấy số lượng hiện tại
                    try:
                        current_qty_str = self.page.driver.find_element(By.NAME, "so_luong").get_attribute("value")
                        if current_qty_str and int(current_qty_str) <= target_qty:
                            return True, f"Đã đạt số lượng mục tiêu ({target_qty}) sau {count} lần nhấn."
                    except:
                        if target_qty == 0 and not self.page.is_visible(self.page.DECREMENT_BUTTON, timeout=1):
                            return True, f"Sản phẩm đã được xóa sau {count} lần nhấn."
                    
                    if not self.page.is_visible(self.page.DECREMENT_BUTTON, timeout=1):
                        break
                        
                    self.page.decrement_quantity()
                    count += 1
                    time.sleep(1.0) # Chờ load trang
                
                # Kiểm tra kết quả cuối cùng
                try:
                    current_qty = int(self.page.driver.find_element(By.NAME, "so_luong").get_attribute("value"))
                    if current_qty <= target_qty:
                        return True, f"Đã giảm số lượng thành công về {current_qty}."
                    else:
                        return False, f"LỖI: Đã nhấn {count} lần nhưng số lượng vẫn là {current_qty}, không giảm xuống {target_qty} được (có thể do UI chặn)."
                except:
                    if target_qty == 0:
                        return True, "Đã xóa sản phẩm thành công."
                    return False, "LỖI: Không tìm thấy ô nhập số lượng để xác nhận."
            else:
                self.page.decrement_quantity()
                time.sleep(0.8) # Chờ trang tải lại sau khi submit form tự động
                return True, "Đã giảm số lượng sản phẩm"
            
        elif any(k in action_name for k in ["xoa_san_pham", "click_nut_x", "xoa", "“x”"]):
            # Kiểm tra nếu chưa ở trang giỏ hàng thì tự động mở
            if not self.page.is_visible(self.page.REMOVE_PRODUCT_BUTTON, timeout=2) and \
               not self.page.is_visible(self.page.CART_EMPTY_MESSAGE, timeout=2):
                self.page.open_cart()
                self.page.wait_for_cart_page()

            if "tat_ca" in action_name or "cac_dong" in action_name:
                count = self.page.remove_all_products()
                return True, f"Đã xóa tất cả sản phẩm ({count}) khỏi giỏ hàng"
            else:
                try:
                    self.page.remove_first_product()
                except Exception as e:
                    # Fallback sang XPath nếu CSS selector thất bại
                    self.page.click(self.page.REMOVE_PRODUCT_XPATH)
                return True, "Đã xóa sản phẩm khỏi giỏ hàng"
            
        elif "xoa_tat_ca" in action_name or "xoa_toan_bo" in action_name:
            self.page.clear_all()
            return True, "Đã xóa toàn bộ giỏ hàng"
            
        elif "thay_doi_so_luong" in action_name:
            # Mặc định là tăng số lượng để thể hiện việc thay đổi
            self.page.increment_quantity()
            return True, "Đã thay đổi số lượng sản phẩm (Tăng)"
            
        else:
            return False, f"Hành động '{action_name}' chưa được hỗ trợ trong module Cart"
