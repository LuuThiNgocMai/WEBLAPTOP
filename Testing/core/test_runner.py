import os
import time
from datetime import datetime
from pathlib import Path
from core.driver_factory import create_driver
from core.step_dispatcher import dispatch_step
from core.result_logger import ResultLogger, StepResult

# --- Hằng số tài khoản dùng cho điều kiện tiên quyết ---
_PREREQUISITE_USERNAME = "thanhtung"
_PREREQUISITE_PASSWORD = "abc123"

def _check_prerequisite_login(dieu_kien: str) -> bool:
    """
    Kiểm tra chuỗi điều kiện tiên quyết có yêu cầu trạng thái đã đăng nhập không.
    Trả về True nếu TC yêu cầu user đã đăng nhập trước.
    """
    if not dieu_kien:
        return False
    kw = dieu_kien.lower()
    return any(k in kw for k in [
        "đã đăng nhập", "da dang nhap", "user logged in",
        "logged in", "đăng nhập trước", "dang nhap truoc",
        "yêu cầu đăng nhập", "nguoi dung da dang nhap",
        "người dùng đã đăng nhập"
    ])

def perform_prerequisite_login(driver, env_config: dict) -> tuple[bool, str]:
    """
    Thực hiện đăng nhập vào hệ thống với tài khoản mặc định.
    Trả về (success: bool, message: str).
    """
    from config import URL_CONFIG
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    import logging

    logger = logging.getLogger("PrerequisiteLogin")

    try:
        # 1. Điều hướng đến trang đăng nhập
        login_url = URL_CONFIG.get("login", "https://localhost:44396/Login")
        logger.info(f"[Tiền điều kiện] Đang mở trang đăng nhập: {login_url}")
        print(f"[Tiền điều kiện] Đang mở trang đăng nhập: {login_url}")
        driver.get(login_url)

        wait = WebDriverWait(driver, 10)

        # 2. Nhập username
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.clear()
        username_field.send_keys(_PREREQUISITE_USERNAME)
        logger.info(f"[Tiền điều kiện] Đã nhập username: {_PREREQUISITE_USERNAME}")
        print(f"[Tiền điều kiện] Đã nhập username: {_PREREQUISITE_USERNAME}")

        # 3. Nhập password
        password_field = wait.until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.clear()
        password_field.send_keys(_PREREQUISITE_PASSWORD)
        logger.info("[Tiền điều kiện] Đã nhập mật khẩu")
        print("[Tiền điều kiện] Đã nhập mật khẩu")

        # 4. Nhấn nút đăng nhập
        login_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_btn.click()
        logger.info("[Tiền điều kiện] Đã nhấn nút Đăng nhập")
        print("[Tiền điều kiện] Đã nhấn nút Đăng nhập")

        # 5. Xác nhận đăng nhập thành công (chờ icon person xuất hiện)
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".bi-person-circle"))
        )
        msg = f"[Tiền điều kiện] Đăng nhập thành công với tài khoản '{_PREREQUISITE_USERNAME}'"
        logger.info(msg)
        print(msg)
        return True, msg

    except TimeoutException as e:
        msg = f"[Tiền điều kiện] Timeout khi đăng nhập: {str(e)}"
        logger.error(msg)
        print(msg)
        return False, msg
    except Exception as e:
        msg = f"[Tiền điều kiện] Lỗi đăng nhập: {str(e)}"
        logger.error(msg)
        print(msg)
        return False, msg

def perform_post_test_logout(driver):
    """
    Thực hiện đăng xuất sau khi hoàn thành test case thành công.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    print("[Hậu điều kiện] Đang thực hiện đăng xuất tự động...")
    try:
        wait = WebDriverWait(driver, 5) # Giảm xuống 5s
        # 1. Click Avatar
        avatar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".bi-person-circle")))
        avatar.click()
        time.sleep(0.3) # Giảm sleep

        # 2. Click Logout
        logout_selectors = [
            (By.LINK_TEXT, "Dang xuat"),
            (By.LINK_TEXT, "Đăng xuất"),
            (By.PARTIAL_LINK_TEXT, "xuat"),
            (By.XPATH, "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'xuat')]"),
            (By.CSS_SELECTOR, "a[href*='Logout']")
        ]
        
        logout_clicked = False
        for selector in logout_selectors:
            try:
                # Thử tìm và click trực tiếp bằng JS để nhanh nhất
                btn = driver.find_element(*selector)
                driver.execute_script("arguments[0].click();", btn)
                logout_clicked = True
                break
            except:
                continue
        
        if logout_clicked:
            print("[Hậu điều kiện] Đã đăng xuất thành công.")
        else:
            print("[Hậu điều kiện] Không tìm thấy nút Đăng xuất.")
            
    except Exception as e:
        print(f"[Hậu điều kiện] Lỗi khi đăng xuất tự động: {str(e)}")

def run_test_case(test_case_data, headless=False, env_config=None, keep_open=False, existing_driver=None, should_navigate=False, clear_cookies=False, already_logged_in=False):
    """
    Main execution engine for a single test case.
    """
    if env_config is None:
        env_config = {}
        
    ma_tc = test_case_data.get('ma_tc', 'TC_UNK')
    ten_tc = test_case_data.get('ten_test_case', 'Không xác định')
    dieu_kien = test_case_data.get('dieu_kien_tien_quyet', '')
    logger = ResultLogger(ma_tc)
    
    driver = existing_driver
    current_logged_in = already_logged_in
    try:
        # 1. Initialize Driver if not provided
        if driver is None:
            driver = create_driver(headless=headless)
        
        # 2. Initial Navigation & Session Management
        target_url = env_config.get('target_url')
        if should_navigate and target_url:
            print(f"Đang điều hướng tới {target_url}...")
            driver.get(target_url)
            
        if clear_cookies:
            if already_logged_in and _check_prerequisite_login(dieu_kien):
                print("Bỏ qua việc xóa cookie để giữ phiên đăng nhập cho Test Case này...")
            else:
                print("Đang xóa cookies...")
                driver.delete_all_cookies()
                driver.refresh() # Khuyến nghị sau khi xóa cookies
                current_logged_in = False # Xóa cookie thì mất session đăng nhập
        
        # 2b. Thực hiện đăng nhập nếu điều kiện tiên quyết yêu cầu
        if _check_prerequisite_login(dieu_kien):
            if current_logged_in:
                print(f"[{ma_tc}] Điều kiện tiên quyết: đã đăng nhập từ trước → Bỏ qua bước login.")
            else:
                print(f"[{ma_tc}] Phát hiện điều kiện tiên quyết: '{dieu_kien}' → Tự động đăng nhập...")
                login_ok, login_msg = perform_prerequisite_login(driver, env_config)
                if not login_ok:
                    # Ghi nhận lỗi tiền điều kiện và dừng TC
                    err_step = StepResult(
                        ma_tc=ma_tc,
                        ten_test_case=ten_tc,
                        so_buoc=0,
                        noi_dung_buoc="[Tiền điều kiện] Đăng nhập hệ thống",
                        module="prerequisite",
                        action="prerequisite_login",
                        trang_thai="LỖI",
                        thong_bao_loi=login_msg,
                        thoi_gian_bat_dau=datetime.now().isoformat(),
                        thoi_gian_ket_thuc=datetime.now().isoformat()
                    )
                    logger.log_step(err_step)
                    return logger.get_summary(), current_logged_in
                current_logged_in = True
                time.sleep(1)  # Chờ trang ổn định sau đăng nhập
        
        # 3. Iterate Steps
        steps = test_case_data.get('danh_sach_buoc', [])
        test_data_ai = test_case_data.get('du_lieu_test_ai', {})
        automation_notes = test_case_data.get('ghi_chu_tu_dong_hoa', '')
        
        for step in steps:
            start_time = datetime.now().isoformat()
            
            # Record base info
            res = StepResult(
                ma_tc=ma_tc,
                ten_test_case=ten_tc,
                so_buoc=step['so_buoc'],
                noi_dung_buoc=step['noi_dung'],
                module=automation_notes,
                action=step['noi_dung'], # Tạm thời dùng nội dung làm action
                trang_thai="CHỜ",
                thoi_gian_bat_dau=start_time
            )
            
            # 3. Dispatch & Execute
            try:
                success, message = dispatch_step(driver, step, test_data_ai, automation_notes, env_config, ma_tc)
            except Exception as e:
                success, message = False, f"Lỗi Điều phối (Dispatch Error): {str(e)}"
            
            res.trang_thai = "ĐẠT" if success else "LỖI"
            res.thong_bao_loi = message if not success else ""
            res.thoi_gian_ket_thuc = datetime.now().isoformat()
            
            # 4. Handle Failure (Screenshot)
            if not success:
                screenshot_filename = f"fail_{ma_tc}_step{step['so_buoc']}.png"
                screenshot_path = os.path.join("Testing", "screenshots", screenshot_filename)
                os.makedirs("Testing/screenshots", exist_ok=True)
                try:
                    driver.save_screenshot(screenshot_path)
                    res.duong_dan_anh_chup = screenshot_path
                except:
                    res.thong_bao_loi += " (Không thể chụp ảnh màn hình)"
                
            logger.log_step(res)
            
            # Add a small delay for observability if not headless
            if not headless and success:
                time.sleep(0.3)
            
            if not success:
                break # Stop on first failure
                
        # --- Hậu điều kiện: Tự động đăng xuất nếu là case Đăng nhập thành công ---
        if success and ("đăng nhập thành công" in ten_tc.lower() or "login thành công" in ten_tc.lower()):
            perform_post_test_logout(driver)
            current_logged_in = False
            
        # Quay lại trang chủ sau mỗi case đăng nhập (thành công hoặc thất bại) để đảm bảo trạng thái sạch
        if "đăng nhập" in ten_tc.lower() or "login" in ten_tc.lower():
            target_url = env_config.get('target_url')
            if target_url:
                print(f"[Hậu điều kiện] Đang quay lại trang chủ: {target_url}")
                driver.get(target_url)
                time.sleep(0.3)
            
    except Exception as e:
        print(f"Lỗi trong quá trình chạy {ma_tc}: {e}")
    finally:
        # 5. Cleanup - Only quit if not an existing driver and not requested to keep open
        if driver and existing_driver is None and not keep_open:
            driver.quit()
        
        # 6. Save results to individual and global reports
        logger.save_json() # Individual timestamped report
        logger.save_csv("ket_qua_chay_test.csv") # Global CSV
        
        return logger.get_summary(), current_logged_in
