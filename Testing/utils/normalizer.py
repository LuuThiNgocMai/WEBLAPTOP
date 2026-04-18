import re
from typing import List, Dict, Any

def parse_steps(steps_str: str) -> List[Dict[str, Any]]:
    """
    Parse a string of steps into a list of dictionaries.
    Supports formats like:
    1. Step one
    2. Step two
    Or just newlines.
    """
    if not steps_str:
        return []

    # Split by newline
    lines = [line.strip() for line in str(steps_str).split('\n') if line.strip()]
    
    parsed_steps = []
    step_num = 1
    
    for line in lines:
        # Check for numeric prefix like "1. ", "2) ", etc.
        # Regex matches digital prefix followed by period, parenthesis or space
        match = re.match(r'^(\d+)[\.\s\)-]+(.*)', line)
        if match:
            # Optionally use the number from the string, but here we re-number
            # as per user's request "đánh lại số bước nếu cần"
            content = match.group(2).strip()
        else:
            content = line
            
        if content:
            parsed_steps.append({
                "so_buoc": step_num,
                "noi_dung": content
            })
            step_num += 1
            
    return parsed_steps

def normalize_testcase(raw_record: Dict[str, Any], index: int = None) -> Dict[str, Any]:
    """
    Normalize a raw test case record into the standardized JSON schema.
    """
    # Mapping logic with fallbacks for different possible column names (support both English and Vietnamese)
    def get_val(keys: List[str], default: Any = ""):
        for key in keys:
            if key in raw_record and raw_record[key] is not None and str(raw_record[key]).strip() != "nan":
                return str(raw_record[key]).strip()
        return default

    # Input columns mapping
    stt_val = get_val(['STT', 'stt', 'No.', 'index'])
    try:
        stt = int(float(stt_val)) if stt_val else (index + 1 if index is not None else 1)
    except:
        stt = index + 1 if index is not None else 1

    ma_tc = get_val(['Mã TC', 'ma_tc', 'test_case_id', 'ID', 'TC ID'])
    ten_tc = get_val(['Tên Test Case', 'ten_test_case', 'scenario', 'Test Case Name', 'Name'])
    mo_ta = get_val(['Mô tả', 'mo_ta', 'Description', 'description'])
    dk_tien_quyet = get_val(['Điều kiện tiên quyết', 'dieu_kien_tien_quyet', 'precondition', 'Pre-condition'])
    buoc_goc = get_val(['Các bước thực hiện', 'steps', 'Steps', 'cac_buoc_thuc_hien'])
    du_lieu_test = get_val(['Dữ liệu test', 'du_lieu_test_goc', 'test_data', 'Data'])
    kq_mong_doi = get_val(['Kết quả mong đợi', 'ket_qua_mong_doi', 'expected_result', 'Expected Result'])
    ghi_chu = get_val(['Ghi chú / Automation Note', 'Ghi chú tự động hóa', 'ghi_chu_tu_dong_hoa', 'notes', 'Note'])

    return {
        "stt": stt,
        "ma_tc": ma_tc,
        "ten_test_case": ten_tc,
        "mo_ta": mo_ta,
        "dieu_kien_tien_quyet": dk_tien_quyet,
        "cac_buoc_thuc_hien_goc": buoc_goc,
        "danh_sach_buoc": parse_steps(buoc_goc),
        "du_lieu_test_goc": du_lieu_test or "",
        "ket_qua_mong_doi": kq_mong_doi,
        "ghi_chu_tu_dong_hoa": ghi_chu or "",
        "buoc_chi_tiet_ai": [],
        "du_lieu_test_ai": {},
        "trang_thai_review": "NEW"
    }
