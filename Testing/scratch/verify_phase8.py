import os
import pandas as pd
from pathlib import Path

def verify_phase8_exports():
    print("--- Verifying Phase 8 Exports ---")
    
    EXPORT_DIR = Path("Testing/exports")
    REPORT_CSV = Path("Testing/reports/ket_qua_chay_test.csv")
    
    if not REPORT_CSV.exists():
        print(f"Error: {REPORT_CSV} not found. Cannot test export.")
        return

    # Simulate the export button logic for Excel and CSV
    df = pd.read_csv(REPORT_CSV)
    
    csv_path = EXPORT_DIR / "report_summary.csv"
    xlsx_path = EXPORT_DIR / "report_summary.xlsx"
    
    try:
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        df.to_excel(xlsx_path, index=False)
        
        if csv_path.exists() and xlsx_path.exists():
            print(f"SUCCESS: Exported CSV found at {csv_path}")
            print(f"SUCCESS: Exported Excel found at {xlsx_path}")
            print(f"CSV Size: {csv_path.stat().st_size} bytes")
            print(f"Excel Size: {xlsx_path.stat().st_size} bytes")
        else:
            print("FAILED: One or more export files missing.")
            
    except Exception as e:
        print(f"Export FAILED: {e}")

if __name__ == "__main__":
    verify_phase8_exports()
