import os
import time
from datetime import datetime
from pathlib import Path
from core.driver_factory import create_driver
from core.step_dispatcher import dispatch_step
from core.result_logger import ResultLogger, StepResult

def run_test_case(test_case_data, headless=False, env_config=None, keep_open=False, existing_driver=None, should_navigate=False, clear_cookies=False):
    """
    Main execution engine for a single test case.
    """
    if env_config is None:
        env_config = {}
        
    ma_tc = test_case_data.get('ma_tc', 'TC_UNK')
    ten_tc = test_case_data.get('ten_test_case', 'Không xác định')
    logger = ResultLogger(ma_tc)
    
    driver = existing_driver
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
            print("Đang xóa cookies...")
            driver.delete_all_cookies()
            driver.refresh() # Khuyến nghị sau khi xóa cookies
        
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
                success, message = dispatch_step(driver, step, test_data_ai, automation_notes, env_config)
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
                time.sleep(1)
            
            if not success:
                break # Stop on first failure
                
    except Exception as e:
        print(f"Lỗi trong quá trình chạy {ma_tc}: {e}")
    finally:
        # 5. Cleanup - Only quit if not an existing driver and not requested to keep open
        if driver and existing_driver is None and not keep_open:
            driver.quit()
        
        # 6. Save results to individual and global reports
        logger.save_json() # Individual timestamped report
        logger.save_csv("ket_qua_chay_test.csv") # Global CSV
        
        return logger.get_summary()
