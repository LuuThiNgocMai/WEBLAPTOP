import sys
import os
import json
from pathlib import Path

# Add the parent directory of 'Testing' (which is the project root) to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# We need to be careful with imports inside Testing
# Since app.py uses 'from core.test_runner import ...'
# it expects 'Testing' to be the package or for 'Testing' to be in path.

from Testing.core.test_runner import run_test_case

def verify_phase7():
    print("--- Verifying Phase 7 Reporting ---")
    
    # Use one of the sample test cases from Testing/data/testcase_review.json
    review_path = Path("Testing/data/testcase_review.json")
    if not review_path.exists():
        print("Error: testcase_review.json not found")
        return

    with open(review_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        tc_data = data[0]

    print(f"Running test for: {tc_data['ma_tc']}")
    
    # Run in headless mode to avoid popping up browser during silent verification
    # Note: This will still attempt to open a browser. 
    # If the environment doesn't have chrome, this might fail.
    # But we want to test the *reporting* logic inside run_test_case.
    try:
        summary = run_test_case(tc_data, headless=True)
        print("Execution finished.")
        print(f"Summary: {summary['trang_thai_cuoi']} - {summary['tong_so_buoc']} steps")
        
        # Check files
        report_csv = Path("Testing/reports/ket_qua_chay_test.csv")
        if report_csv.exists():
            print(f"SUCCESS: Global CSV report found at {report_csv}")
        else:
            print(f"FAILED: Global CSV report not found")
            
    except Exception as e:
        print(f"Execution failed (expected if Chrome is missing, but checking code flow): {e}")

if __name__ == "__main__":
    verify_phase7()
