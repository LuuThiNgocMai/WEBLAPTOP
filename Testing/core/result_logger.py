import json
import csv
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class StepResult:
    ma_tc: str
    ten_test_case: str
    so_buoc: int
    noi_dung_buoc: str
    module: str
    action: str
    trang_thai: str # ĐẠT, LỖI, ERROR
    thong_bao_loi: str = ""
    duong_dan_anh_chup: str = ""
    thoi_gian_bat_dau: str = ""
    thoi_gian_ket_thuc: str = ""

class ResultLogger:
    def __init__(self, ma_tc: str, output_dir: str = "Testing/reports"):
        self.ma_tc = ma_tc
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.steps: List[StepResult] = []
        self.start_time = datetime.now()

    def log_step(self, step_result: StepResult):
        """Logs an individual step result."""
        self.steps.append(step_result)
        print(f"Step {step_result.so_buoc}: {step_result.trang_thai} - {step_result.noi_dung_buoc}")

    def get_summary(self) -> Dict[str, Any]:
        """Calculates final summary for the test case."""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        total = len(self.steps)
        passed = sum(1 for s in self.steps if s.trang_thai == "ĐẠT")
        failed = sum(1 for s in self.steps if s.trang_thai in ["LỖI", "ERROR"])
        
        status = "THÀNH CÔNG" if failed == 0 and total > 0 else "THẤT BẠI"
        
        last_error = ""
        last_screenshot = ""
        if failed > 0:
            fail_step = next((s for s in self.steps if s.trang_thai in ["LỖI", "ERROR"]), None)
            if fail_step:
                last_error = fail_step.thong_bao_loi
                last_screenshot = fail_step.duong_dan_anh_chup

        return {
            "ma_tc": self.ma_tc,
            "ten_test_case": self.steps[0].ten_test_case if self.steps else "Không xác định",
            "tong_so_buoc": total,
            "so_buoc_pass": passed,
            "so_buoc_fail": failed,
            "trang_thai_cuoi": status,
            "thoi_gian_bat_dau": self.start_time.isoformat(),
            "thoi_gian_ket_thuc": end_time.isoformat(),
            "tong_thoi_gian_chay": f"{duration:.2f}s",
            "thong_bao_loi_cuoi_cung": last_error,
            "screenshot_loi_cuoi_cung": last_screenshot,
            "chi_tiet_buoc": [asdict(s) for s in self.steps]
        }

    def save_json(self, filename=None):
        """Saves the result to a JSON file."""
        summary = self.get_summary()
        if not filename:
            filename = f"result_{self.ma_tc}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        return str(file_path)

    def save_csv(self, filename="ket_qua_chay_test.csv"):
        """Saves current steps to a global CSV report (appends if exists)."""
        file_path = self.output_dir / filename
        file_exists = file_path.exists()
        
        summary = self.get_summary()
        
        with open(file_path, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            if not file_exists:
                # Headers for summary per test case (simplified for CSV report)
                writer.writerow([
                    "Mã TC", "Tên Test Case", "Tổng Bước", "Pass", "Fail", 
                    "Trạng thái", "Thời gian chạy", "Lỗi cuối", "Screenshot"
                ])
            
            writer.writerow([
                summary['ma_tc'],
                summary['ten_test_case'],
                summary['tong_so_buoc'],
                summary['so_buoc_pass'],
                summary['so_buoc_fail'],
                summary['trang_thai_cuoi'],
                summary['tong_thoi_gian_chay'],
                summary['thong_bao_loi_cuoi_cung'],
                summary['screenshot_loi_cuoi_cung']
            ])
            
        return str(file_path)
