import json
import os
import random
import time
import logging
import copy
from typing import Dict, Any
from pathlib import Path
import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME
from .prompt_templates import SYSTEM_PROMPT, ENRICH_PROMPT_TEMPLATE, EXAMPLES

# --- Setup Logging ---
LOG_DIR = Path("Testing/reports")
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "ai_generation.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# --- Configure Gemini ---
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def _real_ai_call(testcase_data: Dict[str, Any], retries: int = 3) -> Dict[str, Any]:
    """
    Calls Google Gemini API to generate realistic test data based on steps and name.
    Includes retry logic for network or quota issues.
    """
    prompt = get_full_prompt(testcase_data)
    
    for attempt in range(retries):
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            # Set response_mime_type to application/json if supported, 
            # or just instruct in prompt (already done in SYSTEM_PROMPT)
            response = model.generate_content(
                contents=[{"role": "user", "parts": [{"text": SYSTEM_PROMPT + "\n\n" + prompt}]}]
            )
            
            # Extract JSON from response
            text = response.text
            # Basic cleaning if AI includes markdown code blocks
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
                
            result = json.loads(text)
            
            # --- Post-processing: Ensure single values per field ---
            if "du_lieu_test_ai" in result and isinstance(result["du_lieu_test_ai"], dict):
                for key, value in result["du_lieu_test_ai"].items():
                    if isinstance(value, list):
                        # If AI returns a list despite the prompt, just take the first item
                        result["du_lieu_test_ai"][key] = value[0] if value else ""
            
            logging.info(f"Successfully generated data for {testcase_data.get('ma_tc')}")
            return result
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed for {testcase_data.get('ma_tc')}: {str(e)}")
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1)) # Exponential backoff
            else:
                raise Exception(f"Gemini API Error (404/429/500/etc): {str(e)}")

def _mock_ai_call(testcase_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates an AI API call for testing.
    Standardizes output for common scenarios and handles empty field cases.
    """
    name = str(testcase_data.get('ten_test_case') or '').lower()
    steps = testcase_data.get('danh_sach_buoc') or []
    steps_content = " ".join([
        str(s.get('noi_dung', '')).lower()
        for s in steps
        if isinstance(s, dict)
    ])
    full_text = f"{name} {steps_content}"
    
    # User's Baseline Valid Data (used for 'already exists' scenarios)
    BASELINE_REG = {
        "tên đăng nhập": "MockUser54265",
        "mật khẩu": "MockPass123",
        "họ và tên": "Nguyen Van A",
        "địa chỉ": "123 Đường Example, Hà Nội",
        "số điện thoại": "0369852147",
        "ngày sinh": "1990-01-01",
        "email": "mock.user@example.com",
        "giới tính": "Nam"
    }

    # 1. Module Detection (Mutually Exclusive)
    ma_tc = testcase_data.get('ma_tc', '').upper()
    is_reg = is_login = is_cart = is_product = is_account = False

    # Priority 1: Prefix in Mã TC (Strongest)
    if ma_tc.startswith('REG'):
        is_reg = True
    elif ma_tc.startswith('LOG') or ma_tc.startswith('TC_'):
        is_login = True
    elif ma_tc.startswith('CART'):
        is_cart = True
    elif ma_tc.startswith('VIEWP'):
        is_product = True
    elif ma_tc.startswith('ACC'):
        is_account = True
    
    # Priority 2: Keywords in Name (If no prefix matched)
    if not (is_reg or is_login or is_cart or is_product or is_account):
        if 'đăng ký' in name or 'register' in name:
            is_reg = True
        elif 'đăng nhập' in name or 'login' in name:
            is_login = True
        elif 'giỏ hàng' in name or 'cart' in name:
            is_cart = True
        elif ('chi tiết' in name and 'khách hàng' not in name) or 'sản phẩm' in name or 'product' in name:
            is_product = True
        elif 'tài khoản' in name or 'account' in name or 'hồ sơ' in name:
            is_account = True
            
    # Priority 3: Fallback Keywords (If still no match)
    if not (is_reg or is_login or is_cart or is_product or is_account):
        if any(k in full_text for k in ['họ và tên', 'địa chỉ', 'ngày sinh', 'số điện thoại']):
            # For account management cases, prioritize account over registration if 'tài khoản' is mentioned
            if 'tài khoản' in full_text or 'account' in full_text:
                is_account = True
            else:
                is_reg = True
        elif any(k in full_text for k in ['tên đăng nhập', 'mật khẩu', 'username', 'password']):
            is_login = True
        elif 'giỏ hàng' in name or 'cart' in name:
            is_cart = True

    if is_reg:
        # --- REG_12: UI check (nút "Đăng nhập ngay") → không cần data ---
        is_ui_check = any(k in full_text for k in ["nút", "button", "đăng nhập ngay"])
        has_input_action = any(k in full_text for k in ["nhập ", " điền", " chọn", "nhập liệu"])
        if is_ui_check and not has_input_action:
            return {"du_lieu_test_ai": {}}

        # Mọi case đăng ký đều bắt đầu từ BASELINE đầy đủ 8 trường
        data_fields = BASELINE_REG.copy()

        # --- REG_04: Để trống Tên đăng nhập ---
        if "để trống tên đăng nhập" in full_text:
            data_fields["tên đăng nhập"] = ""

        # --- REG_05: Để trống Mật khẩu ---
        if "để trống mật khẩu" in full_text:
            data_fields["mật khẩu"] = ""

        # --- REG_06: Để trống Họ và tên ---
        if "để trống họ và tên" in full_text:
            data_fields["họ và tên"] = ""

        # --- REG_07: Để trống Email ---
        if "để trống email" in full_text:
            data_fields["email"] = ""

        # --- REG_08: Email sai định dạng ---
        if "email sai định dạng" in full_text:
            data_fields["email"] = "invalid-email@@"

        # --- REG_09: SĐT sai định dạng ---
        if "sđt sai định dạng" in full_text:
            data_fields["số điện thoại"] = "abc123"

        # --- REG_10: Ngày sinh không hợp lệ ---
        if "ngày sinh không hợp lệ" in full_text:
            data_fields["ngày sinh"] = "2099-12-31"

        # --- REG_11: Không chọn Giới tính ---
        if "không chọn giới tính" in full_text:
            data_fields["giới tính"] = ""

        # --- REG_13: Ký tự đặc biệt trong Họ tên, Địa chỉ ---
        if "ký tự đặc biệt" in full_text:
            data_fields["họ và tên"] = "Nguyễn @#$% Văn"
            data_fields["địa chỉ"] = "123 !@#$ Đường Test"

        # --- REG_14: Độ dài tối thiểu ---
        if "độ dài tối thiểu" in full_text:
            data_fields["tên đăng nhập"] = "A"
            data_fields["mật khẩu"] = "1"
            data_fields["họ và tên"] = "A"

        # --- REG_15: Độ dài tối đa ---
        if "độ dài tối đa" in full_text:
            data_fields["tên đăng nhập"] = "A" * 255
            data_fields["mật khẩu"] = "P" * 128
            data_fields["họ và tên"] = "Nguyễn " + "A" * 200

        # REG_01 (đầy đủ hợp lệ), REG_02 (TĐN đã tồn tại), REG_03 (Email đã tồn tại)
        # → giữ nguyên BASELINE_REG, không cần sửa gì thêm

        return {"du_lieu_test_ai": data_fields}




    # 2. Login Module
    elif is_login:
        login_data = {
            "tên đăng nhập": "thanhtung",
            "mật khẩu": "abc123"
        }
        
        # 2b. Logic for non-existent user
        if "không tồn tại" in full_text or "not exist" in full_text:
            login_data["tên đăng nhập"] = "user_khong_ton_tai"

        # 2c. Logic for wrong password
        if "sai mật khẩu" in full_text or "mật khẩu không đúng" in full_text:
            login_data["mật khẩu"] = "SaiMatKhau123"

        # 2a. Logic for empty/blank fields
        if any(k in full_text for k in ["rỗng", "trống", "empty", "blank", "không nhập", "bỏ trống"]):
            # Ưu tiên tìm ý định để trống trong Tên Test Case vì các bước (steps) có thể nhắc đến cả 2 trường
            name_lower = name.lower()
            is_both = any(k in name_lower for k in ["cả hai", "all", "các trường"])
            
            if is_both:
                login_data["tên đăng nhập"] = ""
                login_data["mật khẩu"] = ""
            elif "tên đăng nhập" in name_lower or "username" in name_lower:
                login_data["tên đăng nhập"] = ""
                login_data["mật khẩu"] = "abc123"
            elif "mật khẩu" in name_lower or "password" in name_lower:
                login_data["tên đăng nhập"] = "thanhtung"
                login_data["mật khẩu"] = ""
            else:
                # Nếu tên không rõ, mới dùng full_text nhưng lỏng hơn
                if any(k in full_text for k in ["tên đăng nhập", "email", "username"]): 
                    login_data["tên đăng nhập"] = ""
                if any(k in full_text for k in ["mật khẩu", "password", "mat_khau"]): 
                    login_data["mật khẩu"] = ""
        
        # 2b. Logic for invalid/wrong credentials
        if any(k in full_text for k in ["sai", "không đúng", "không hợp lệ", "invalid", "chưa đăng ký"]):
            if any(k in full_text for k in ["mật khẩu", "password", "mat_khau"]):
                login_data["mật khẩu"] = "WrongPass123"
            if any(k in full_text for k in ["tên đăng nhập", "email", "username"]):
                login_data["tên đăng nhập"] = "wrong_user"

        # 2c. Logic for special characters
        if "ký tự đặc biệt" in full_text:
            login_data["tên đăng nhập"] = "Admin@#!123"

        # 2d. Logic for length limits
        if "độ dài" in full_text or "giới hạn" in full_text:
            if "tên đăng nhập" in full_text:
                login_data["tên đăng nhập"] = "A" * 255
            if "mật khẩu" in full_text:
                login_data["mật khẩu"] = "P" * 128

        # 2e. Logic for case sensitivity
        if "chữ hoa" in full_text or "viết hoa" in full_text:
            if "tên đăng nhập" in full_text:
                login_data["tên đăng nhập"] = str(login_data["tên đăng nhập"]).upper()
            if "mật khẩu" in full_text:
                login_data["mật khẩu"] = str(login_data["mật khẩu"]).upper()

        return {"du_lieu_test_ai": login_data}

    # 3. Other modules
    elif 'tìm kiếm' in name or 'search' in name:
        if any(k in full_text for k in ['danh mục', 'danh muc', 'category']):
            return {
                "du_lieu_test_ai": {
                    "danh_muc": "Laptop", # Chỉ cần trường danh mục
                    "loai_tim_kiem": "theo danh mục"
                }
            }
        elif any(k in full_text for k in ['không có kết quả', 'không tồn tại', 'no result', 'khong co ket qua', 'không tìm thấy']):
            return {
                "du_lieu_test_ai": {
                    "tu_khoa": "!@##$$",
                    "loai_tim_kiem": "không có kết quả"
                }
            }
        elif any(k in full_text for k in ['rỗng', 'trống', 'empty', 'blank', 'không nhập']):
            return {
                "du_lieu_test_ai": {
                    "tu_khoa": "",
                    "danh_muc": "",
                    "loai_tim_kiem": "từ khóa rỗng"
                }
            }
        return copy.deepcopy(EXAMPLES['search']['output'])
    elif is_cart:
        cart_data = {
            "ma_san_pham": "Gigabyte AORUS 17H",
            "tên sản phẩm": "Gigabyte AORUS 17H"
        }
        
        # Cart_006: Thêm nhiều lần
        if "nhiều lần" in full_text or "nhiều sản phẩm" in full_text:
            cart_data["số lượng"] = 3
            
        # Cart_005: Giảm số lượng xuống 1
        if "xuống 1" in full_text:
            cart_data["số lượng mục tiêu"] = 1

        return {"du_lieu_test_ai": cart_data}
    # 4. Product Detail module (ViewP)
    elif is_product:
        # ViewP_002: Không kết nối CSDL → không cần data sản phẩm
        if 'không kết nối' in full_text or 'mất kết nối' in full_text or 'csdl' in full_text or 'database' in full_text:
            return {"du_lieu_test_ai": {}}

        # ViewP_004: Sản phẩm không tồn tại → tên sai
        if 'không tồn tại' in full_text:
            return {
                "du_lieu_test_ai": {
                    "tên sản phẩm": "abc"
                }
            }

        # ViewP_001, ViewP_003: Xem chi tiết thành công → tên đúng
        return {
            "du_lieu_test_ai": {
                "tên sản phẩm": "Gigabyte AORUS 17H"
            }
        }
    # 5. Account Management module (ACC)
    elif is_account:
        # ACC_01, ACC_02, ACC_03, ACC_04: UI check / Navigation / Display Check → no data needed
        # Theo yêu cầu: "xem chi tiết", "Kiểm tra dữ liệu hiển thị đúng", "Click nút Chỉnh sửa" không cần sinh data
        is_no_data_case = any(k in full_text for k in [
            "nút chỉnh sửa", 
            "quay lại trang chủ", 
            "điều hướng",
            "xem chi tiết",
            "màn hình chi tiết",
            "hiển thị đúng",
            "kiểm tra dữ liệu"
        ])
        has_input_action = any(k in full_text for k in ["nhập", "điền", "cập nhật", "thay đổi", "chỉnh sửa họ tên", "chỉnh sửa email", "chỉnh sửa số điện thoại"])
        
        if is_no_data_case and not has_input_action:
            return {"du_lieu_test_ai": {}}

        # Mọi case tài khoản (nếu cần data)
        # Theo yêu cầu mới: Chỉnh sửa trường nào thì CHỈ sinh data trường đó
        data_fields = {}

        # 1. Xử lý Họ tên
        if "họ tên" in full_text:
            data_fields["họ và tên"] = "Nguyễn Văn Mới"
            
        # 2. Xử lý Email
        if "email" in full_text:
            if "sai định dạng" in full_text:
                data_fields["email"] = "invalid-email@@"
            else:
                data_fields["email"] = "new.email@example.com"
                
        # 3. Xử lý Số điện thoại
        if "số điện thoại" in full_text or "sđt" in full_text:
            if "không hợp lệ" in full_text or "sai" in full_text:
                data_fields["số điện thoại"] = "abc123456"
            else:
                data_fields["số điện thoại"] = "0999888777"

        # Nếu không bắt được trường cụ thể nào thì mới dùng baseline (fallback)
        if not data_fields:
            data_fields = BASELINE_REG.copy()
            data_fields.pop("tên đăng nhập", None)
            data_fields.pop("mật khẩu", None)

        return {"du_lieu_test_ai": data_fields}
    else:
        return {
            "du_lieu_test_ai": {
                "gia_tri_mac_dinh": "Dữ liệu mẫu từ Mock AI",
                "so_luong": random.randint(1, 10),
                "ngay_tao": "2024-01-01"
            }
        }

def enrich_test_data(testcase_data: Dict[str, Any], engine: str = "Mock AI") -> Dict[str, Any]:
    """
    Main entry point for AI enrichment. Supports 'Mock AI' or 'Gemini AI'.
    """
    if engine == "Mock AI":
        return _mock_ai_call(testcase_data)
    else:
        return _real_ai_call(testcase_data)

def get_full_prompt(testcase_data: Dict[str, Any]) -> str:
    """Constructs the prompt for the AI."""
    # Build a string representing all steps clearly
    steps_list = testcase_data.get('danh_sach_buoc') or []

    steps_formatted = "\n".join([
        f"Bước {s.get('so_buoc', '')}: {s.get('noi_dung', '')}"
        for s in steps_list
        if isinstance(s, dict)
    ])
    return ENRICH_PROMPT_TEMPLATE.format(
        ma_tc=testcase_data.get('ma_tc', ''),
        ten_test_case=testcase_data.get('ten_test_case', ''),
        mo_ta=testcase_data.get('mo_ta', ''),
        dieu_kien_tien_quyet=testcase_data.get('dieu_kien_tien_quyet', ''),
        cac_buoc_thuc_hien=steps_formatted,
        du_lieu_test_goc=testcase_data.get('du_lieu_test_goc', ''),
        ghi_chu_tu_dong_hoa=testcase_data.get('ghi_chu_tu_dong_hoa', '')
    )
