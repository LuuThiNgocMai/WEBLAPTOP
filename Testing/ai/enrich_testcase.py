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
        "mật khẩu": "MockPass123"
    }

    # 1. Module Detection
    ma_tc = testcase_data.get('ma_tc', '').upper()
    
    # Priority 1: Prefix in Mã TC
    is_reg = ma_tc.startswith('REG')
    is_login = ma_tc.startswith('LOG')
    is_cart = ma_tc.startswith('CART')
    
    # Priority 2: Keywords in Name (Strong indicators)
    if not is_reg and not is_login and not is_cart:
        if 'đăng ký' in name or 'register' in name:
            is_reg = True
        elif 'đăng nhập' in name or 'login' in name:
            is_login = True
        elif 'giỏ hàng' in name or 'cart' in name:
            is_cart = True
            
    # Priority 3: Keywords in Full Text (Fallback)
    if not is_reg and not is_login and not is_cart:
        if any(k in full_text for k in ['họ và tên', 'địa chỉ', 'ngày sinh', 'số điện thoại']):
            is_reg = True
        elif any(k in full_text for k in ['tên đăng nhập', 'mật khẩu', 'username', 'password']):
            is_login = True
        elif 'giỏ hàng' in name or 'cart' in name:
            is_cart = True

    if is_reg:
        # Check if this is a UI/Button check case (no data needed)
        is_ui_check = any(k in full_text for k in ["nút", "button", "hiển thị", "giao diện", "interface", "layout"])
        # Avoid "đăng nhập" triggering the "nhập" input keyword
        has_input_action = any(k in full_text for k in ["nhập ", " điền", " chọn", "nhập liệu"])
        
        if is_ui_check and not has_input_action:
            return {"du_lieu_test_ai": {}}

        # Check if this is the "Golden" (Valid Full Info) case or an "Already Exists" case
        is_golden = "đầy đủ thông tin hợp lệ" in full_text
        is_exists = any(k in full_text for k in ["đã tồn tại", "da ton tai", "already exists"])

        # Start with RANDOM values for everyone to avoid unintended clashes
        data_fields = {
            "tên đăng nhập": "MockUser54265",
            "mật khẩu": "MockPass123"
        }

        if is_golden:
            # GOLDEN case uses full baseline
            data_fields = BASELINE_REG.copy()
        elif is_exists:
            # ONLY override the specific field mentioned as existing
            if any(k in full_text for k in ["tên đăng nhập", "username", "tk"]):
                data_fields["tên đăng nhập"] = BASELINE_REG["tên đăng nhập"]
            if "email" in full_text:
                data_fields["email"] = BASELINE_REG["email"]
            if any(k in full_text for k in ["sđt", "số điện thoại", "điện thoại"]):
                data_fields["số điện thoại"] = BASELINE_REG["số điện thoại"]


        # 1a. Logic for empty/blank fields
        if any(k in full_text for k in ["rỗng", "trống", "empty", "blank", "không nhập", "bỏ trống"]):
            if any(k in full_text for k in ["tên đăng nhập", "username"]): data_fields["tên đăng nhập"] = ""
            if any(k in full_text for k in ["mật khẩu", "password", "mat_khau"]): data_fields["mật khẩu"] = ""

        # 1c. Logic for invalid format
        if "sai định dạng" in full_text or "không hợp lệ" in full_text or "sai" in full_text:
            if any(k in full_text for k in ["mật khẩu", "password"]): data_fields["mật khẩu"] = "123"
            if any(k in full_text for k in ["tên đăng nhập", "username"]): data_fields["tên đăng nhập"] = "!"

        return {"du_lieu_test_ai": data_fields}




    # 2. Login Module
    if is_login:
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
    if 'tìm kiếm' in name or 'search' in name:
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
        }
        # Theo yêu cầu: chỉ cần mã sản phẩm, không cần thêm gì khác
        return {"du_lieu_test_ai": cart_data}
    elif 'chi tiết' in name or 'sản phẩm' in name or 'product' in name:
        return {
            "du_lieu_test_ai": {
                "số lượng": 2
            }
        }
    elif any(k in name for k in ['tài khoản', 'chỉnh sửa', 'account', 'họ tên', 'email', 'sđt', 'số điện thoại', 'ngày sinh', 'giới tính', 'mật khẩu']):
        return {
            "du_lieu_test_ai": {
                "họ tên": "Mock Account Tên",
                "email": "mock_account@example.com",
                "địa chỉ": "Mock Địa Chỉ Account",
                "số điện thoại": "0987654321",
                "ngày sinh": "01/01/1990",
                "giới tính": "Nam",
                "mật khẩu mới": "MockNewPass123"
            }
        }
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
