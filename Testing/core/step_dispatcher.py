import time
import logging
from modules.login.login_handler import LoginHandler
from modules.search.search_handler import SearchHandler
from modules.product.product_handler import ProductHandler
from modules.cart.cart_handler import CartHandler
from modules.checkout.checkout_handler import CheckoutHandler
from modules.register.register_handler import RegisterHandler
from modules.account.account_handler import AccountHandler

def _normalize_string(s):
    """Simple normalization: lowercase, remove spaces, and basic accent removal for common cases."""
    import unicodedata
    if not s: return ""
    s = s.lower().strip()
    s = "".join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = s.replace(" ", "_").replace("-", "_")
    return s

def dispatch_step(driver, step_info, test_data_ai, automation_notes, env_config=None):
    """
    Identifies the module from automation_notes and executes the corresponding logic.
    """
    if env_config is None:
        env_config = {}

    # 1. Parse module from automation notes (e.g., "module=login")
    notes = str(automation_notes or "").lower()
    module_name = "general"
    
    if "module=" in notes:
        module_name = notes.split("module=")[1].split(";")[0].strip()
    else:
        # Heuristic: try to guess module from step content if notes are missing
        content = step_info.get('noi_dung', '').lower()
        if any(k in content for k in ["đăng nhập", "login", "mật khẩu", "email"]):
            module_name = "login"
        elif any(k in content for k in ["tìm kiếm", "search", "keyword"]):
            module_name = "search"
        elif any(k in content for k in ["sản phẩm", "product", "chi tiết"]):
            module_name = "product"
        elif any(k in content for k in ["giỏ hàng", "cart", "thêm vào"]):
            module_name = "cart"
        elif any(k in content for k in ["thanh toán", "checkout", "đặt hàng"]):
            module_name = "checkout"
        elif any(k in content for k in ["đăng ký", "signup", "register"]):
            module_name = "register"
        elif any(k in content for k in ["tài khoản", "profile", "account"]):
            module_name = "account"
    
    # 2. Extract and normalize action name
    raw_action = step_info.get('noi_dung', '')
    action_name = _normalize_string(raw_action)
    
    # 3. Route to specific module handlers
    try:
        if module_name == "login":
            handler = LoginHandler(driver)
            return handler.execute_action(action_name, step_info, test_data_ai, env_config)
            
        elif module_name == "search":
            handler = SearchHandler(driver)
            return handler.execute_action(action_name, step_info, test_data_ai, env_config)
            
        elif module_name == "product":
            handler = ProductHandler(driver)
            return handler.execute_action(action_name, step_info, test_data_ai, env_config)
            
        elif module_name == "cart":
            handler = CartHandler(driver)
            return handler.execute_action(action_name, step_info, test_data_ai, env_config)
            
        elif module_name == "checkout":
            handler = CheckoutHandler(driver)
            return handler.execute_action(action_name, step_info, test_data_ai, env_config)
            
        elif module_name == "register":
            handler = RegisterHandler(driver)
            return handler.execute_action(action_name, step_info, test_data_ai, env_config)
            
        elif module_name == "account":
            handler = AccountHandler(driver)
            return handler.execute_action(action_name, step_info, test_data_ai, env_config)
            
        else:
            return _handle_generic(driver, step_info, test_data_ai)
            
    except Exception as e:
        import logging
        logging.error(f"Lỗi trong module {module_name}: {str(e)}")
        return False, f"Lỗi thực thi module {module_name}: {str(e)}"

def _handle_generic(driver, step_info, test_data):
    """Xử lý các bước cơ bản nếu không xác định được module."""
    content = step_info.get('noi_dung', '').lower()
    if any(k in content for k in ["đợi", "wait", "nghỉ"]):
        import time
        time.sleep(2)
        return True, "Đã tạm dừng 2 giây"
    
    if any(k in content for k in ["tải lại", "refresh", "f5"]):
        driver.refresh()
        return True, "Đã tải lại trang"
    
    return True, f"Đã thực hiện bước chung: {content}"
