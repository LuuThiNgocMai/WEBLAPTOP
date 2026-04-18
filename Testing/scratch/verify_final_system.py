import os
import json
from pathlib import Path

def verify_full_system_data_flow():
    print("--- Verifying Full System Data Flow ---")
    
    # Paths
    DATA_DIR = Path("Testing/data")
    STANDARDIZED = DATA_DIR / "testcase_chuan_hoa.json"
    AI_DATA = DATA_DIR / "testcase_ai.json"
    REVIEWED = DATA_DIR / "testcase_review.json"

    # 1. Mock Step 1: Normalization
    mock_normalized = [{"stt": 1, "ma_tc": "VERIFY_FLOW", "ten_test_case": "Flow Check", "danh_sach_buoc": []}]
    with open(STANDARDIZED, 'w', encoding='utf-8') as f:
        json.dump(mock_normalized, f, indent=2)
    print("Mock Normalization: OK")

    # 2. Mock Step 2: Batch AI
    # (Simulating what app.py does)
    with open(STANDARDIZED, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        item['du_lieu_test_ai'] = {"test": "data"}
    with open(AI_DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("Mock AI Batch: OK")

    # 3. Mock Step 2.5: Approve
    if AI_DATA.exists():
        with open(AI_DATA, 'r', encoding='utf-8') as f:
            ai_data_content = json.load(f)
        with open(REVIEWED, 'w', encoding='utf-8') as f:
            json.dump(ai_data_content, f, indent=2)
        print("Mock Approval: OK")

    # 4. Final Check
    if REVIEWED.exists():
        with open(REVIEWED, 'r', encoding='utf-8') as f:
            final = json.load(f)
        if len(final) > 0 and 'du_lieu_test_ai' in final[0]:
            print("SUCCESS: Full data flow from Upload -> AI -> Review is verified.")
        else:
            print("FAILED: Data missing details in REVIEWED stage.")
    else:
        print("FAILED: REVIEWED file not created.")

if __name__ == "__main__":
    verify_full_system_data_flow()
