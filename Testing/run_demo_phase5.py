from core.test_runner import run_test_case

# Mock a "Reviewed" test case with AI data from Phase 3
mock_test_case = {
    "stt": 1,
    "ma_tc": "TC_LOGIN_001",
    "ten_test_case": "Đăng nhập thành công",
    "mo_ta": "Kiểm tra tính năng đăng nhập với user hợp lệ",
    "dieu_kien_tien_quyet": "Trình duyệt đang ở trang chủ",
    "cac_buoc_thuc_hien_goc": "1. Mở trang chủ\n2. Nhập email\n3. Nhập pass\n4. Nhấn Login",
    "danh_sach_buoc": [
        {"so_buoc": 1, "noi_dung": "Mở trang chủ"},
        {"so_buoc": 2, "noi_dung": "Nhập email"},
        {"so_buoc": 3, "noi_dung": "Nhập pass"},
        {"so_buoc": 4, "noi_dung": "Nhấn Login"}
    ],
    "du_lieu_test_goc": "user: admin@test.com",
    "ket_qua_mong_doi": "Vào được Dashboard",
    "ghi_chu_tu_dong_hoa": "module=login",
    "du_lieu_test_ai": {
        "email": "admin@test.com",
        "mat_khau": "123456",
        "url": "https://example.com/login"
    },
    "trang_thai_review": "REVIEWED"
}

if __name__ == "__main__":
    print("--- 🚀 Bắt đầu chạy thử nghiệm lõi Selenium (Phase 5) ---")
    
    # Run test (headless mode for speed/CI)
    summary, report_path = run_test_case(mock_test_case, headless=True)
    
    print("\n--- 📊 Kết quả kiểm thử ---")
    print(f"Mã TC: {summary['ma_tc']}")
    print(f"Trạng thái: {summary['trang_thai_cuoi']}")
    print(f"Tiến độ: Pass {summary['so_buoc_pass']}/{summary['tong_so_buoc']}")
    print(f"Thời gian: {summary['tong_thoi_gian_chay']}")
    print(f"Chi tiết report: {report_path}")
