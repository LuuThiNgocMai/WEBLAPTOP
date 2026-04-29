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
    name = testcase_data.get('ten_test_case', '').lower()
    data = {"du_lieu_test_ai": {}}
    
    # 1. Base data generation
    if 'đăng nhập' in name or 'login' in name:
        data = copy.deepcopy(EXAMPLES['login']['output'])
    elif 'tìm kiếm' in name or 'search' in name:
        data = copy.deepcopy(EXAMPLES['search']['output'])
    elif 'giỏ hàng' in name or 'cart' in name:
        data = copy.deepcopy(EXAMPLES['cart']['output'])
    else:
        data = {
            "du_lieu_test_ai": {
                "gia_tri_mac_dinh": "Dữ liệu mẫu từ Mock AI",
                "so_luong": random.randint(1, 10),
                "ngay_tao": "2024-01-01"
            }
        }

    # 2. Logic for empty/blank fields (Negative Testing)
    # Scan both Title and Steps for "rỗng" or "trống" keywords
    steps_content = " ".join([s['noi_dung'].lower() for s in testcase_data.get('danh_sach_buoc', [])])
    full_text = f"{name} {steps_content}"
    
    if any(k in full_text for k in ["rỗng", "trống", "empty", "blank"]):
        ai_fields = data["du_lieu_test_ai"]
        # Check specific field mentions followed by empty keywords in the combined text
        if "email" in full_text:
            ai_fields["email"] = ""
        if any(k in full_text for k in ["mật khẩu", "password", "mat_khau"]):
            ai_fields["mat_khau"] = ""
        if any(k in full_text for k in ["tên", "từ khóa", "keyword", "tu_khoa", "search"]):
            if "tu_khoa" in ai_fields: ai_fields["tu_khoa"] = ""
            if "product_name" in ai_fields: ai_fields["product_name"] = ""
            if "keyword" in ai_fields: ai_fields["keyword"] = ""
            
    return data

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
    steps_list = testcase_data.get('danh_sach_buoc', [])
    steps_formatted = "\n".join([f"Bước {s['so_buoc']}: {s['noi_dung']}" for s in steps_list])
    
    return ENRICH_PROMPT_TEMPLATE.format(
        ma_tc=testcase_data.get('ma_tc', ''),
        ten_test_case=testcase_data.get('ten_test_case', ''),
        mo_ta=testcase_data.get('mo_ta', ''),
        dieu_kien_tien_quyet=testcase_data.get('dieu_kien_tien_quyet', ''),
        cac_buoc_thuc_hien=steps_formatted,
        du_lieu_test_goc=testcase_data.get('du_lieu_test_goc', ''),
        ghi_chu_tu_dong_hoa=testcase_data.get('ghi_chu_tu_dong_hoa', '')
    )
