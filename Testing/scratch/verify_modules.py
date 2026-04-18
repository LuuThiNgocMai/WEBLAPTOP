import sys
import os
from unittest.mock import MagicMock

# Add project root to sys.path to resolve relative imports
# d:\DATN - Mai\Testing\core\step_dispatcher.py uses ..modules
# So we need to be at d:\DATN - Mai and run with -m or add it to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from Testing.core.step_dispatcher import dispatch_step

def test_wiring():
    print("--- Starting Wiring Verification ---")
    
    # Mock driver
    mock_driver = MagicMock()
    
    # Test Data
    test_data = {
        "email": "test@example.com",
        "password": "password123",
        "keyword": "macbook",
        "full_name": "Mai Luu",
        "address": "TPHCM",
        "phone": "0909123456"
    }
    
    # Scenarios to test
    scenarios = [
        ("Login", "module=login", "mo_trang_dang_nhap"),
        ("Login Input", "module=login", "nhap_email"),
        ("Search", "module=search", "nhap_tu_khoa_tim_kiem"),
        ("Product", "module=product", "chon_san_pham_dau_tien"),
        ("Cart", "module=cart", "them_vao_gio_hang"),
        ("Checkout", "module=checkout", "nhan_thanh_toan"),
        ("Generic", "module=general", "wait 1s")
    ]
    
    for label, notes, content in scenarios:
        step_info = {"noi_dung": content}
        print(f"Testing {label}: [{notes}] {content}...")
        try:
            # We use a mock driver, so Selenium calls will fail if they try to interact with real browser
            # But the logic flow should reach the handlers.
            # In our handlers, we call self.page.XXX which calls self.click/enter_text
            # BasePage methods use WebDriverWait, which might fail with MagicMock if not properly setup.
            # However, for a simple wiring test, we just want to see if it imports and routes.
            
            success, message = dispatch_step(mock_driver, step_info, test_data, notes)
            print(f"  Result: {'PASS' if success else 'FAIL'} - {message}")
        except Exception as e:
            print(f"  ERROR: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_wiring()
