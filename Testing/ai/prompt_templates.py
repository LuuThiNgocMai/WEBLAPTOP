# System prompt for the AI
SYSTEM_PROMPT = """
Bạn là AI hỗ trợ làm giàu testcase cho hệ thống kiểm thử tự động.

Nhiệm vụ của bạn:
Từ testcase được cung cấp, chỉ sinh thêm dữ liệu kiểm thử.

Ràng buộc bắt buộc:
- Chỉ được sinh dữ liệu kiểm thử
- Không được sinh bước kiểm thử chi tiết
- Không được sinh kết quả mong đợi
- Không được sinh kết quả thực tế
- Không được sinh trạng thái test
- Không được suy diễn ngoài thông tin testcase được cung cấp

Chỉ được dựa trên:
- Tên Test Case
- Mô tả
- Điều kiện tiên quyết
- Các bước thực hiện
- Dữ liệu test gốc
- Ghi chú tự động hóa

Dữ liệu sinh ra phải thực tế, phù hợp với ngữ cảnh Việt Nam.
Trả về đúng JSON với cấu trúc: {"du_lieu_test_ai": {}}
"""

# Template for the enrichment request
ENRICH_PROMPT_TEMPLATE = """
Hãy thực hiện nhiệm vụ làm giàu testcase sau:

Mã TC: {ma_tc}
Tên Test Case: {ten_test_case}
Mô tả: {mo_ta}
Điều kiện tiên quyết: {dieu_kien_tien_quyet}
Các bước thực hiện:
{cac_buoc_thuc_hien}
Dữ liệu test gốc: {du_lieu_test_goc}
Ghi chú tự động hóa: {ghi_chu_tu_dong_hoa}

Hãy trả về đúng JSON với cấu trúc sau:
{{
  "du_lieu_test_ai": {{}}
}}
"""

# FEW-SHOT EXAMPLES as requested
EXAMPLES = {
    "login": {
        "input": "Đăng nhập hệ thống với tài khoản admin",
        "output": {
            "du_lieu_test_ai": {
                "email": "admin@gmail.com",
                "mat_khau": "Admin@123",
                "loai_tai_khoan": "quản trị viên"
            }
        }
    },
    "search": {
        "input": "Tìm kiếm sản phẩm trên trang chủ",
        "output": {
            "du_lieu_test_ai": {
                "tu_khoa": "Laptop Gaming ASUS",
                "danh_muc": "Điện tử",
                "sap_xep": "Giá thấp đến cao"
            }
        }
    },
    "cart": {
        "input": "Thêm sản phẩm vào giỏ hàng",
        "output": {
            "du_lieu_test_ai": {
                "ma_san_pham": "SP001",
                "so_luong": 2,
                "mau_sac": "Đen",
                "kich_thuoc": "L"
            }
        }
    }
}
