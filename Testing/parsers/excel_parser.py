import pandas as pd
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Lowercase and strip whitespace from column names.
    Original names are preserved as well.
    """
    # Simply keep names as is for the normalizer to handle, 
    # but we can provide lowercased versions as well if needed.
    return df

def parse_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse the first sheet of an Excel file and return a list of dictionaries.
    """
    try:
        logger.info(f"Parsing Excel file: {file_path}")
        # Read the first sheet
        df = pd.read_excel(file_path, sheet_name=0)
        
        # Fill NaN values with empty string
        df = df.fillna("")
        
        # Loại bỏ dòng trống (dòng mà Mã TC hoặc Tên Test Case đều rỗng)
        key_cols = [c for c in df.columns if any(k in c.lower() for k in ['mã', 'ma', 'tên test', 'ten test'])]
        if key_cols:
            # Giữ lại dòng có ít nhất 1 cột quan trọng không rỗng
            mask = df[key_cols].apply(lambda row: any(str(v).strip() != '' for v in row), axis=1)
            df = df[mask].reset_index(drop=True)
        else:
            # Fallback: bỏ dòng mà tất cả cột đều rỗng
            df = df[df.apply(lambda row: any(str(v).strip() != '' for v in row), axis=1)].reset_index(drop=True)
        
        # Convert all columns to list of dicts
        # The normalize_testcase function handles the header mapping.
        data = df.to_dict('records')
        
        return data
    except Exception as e:
        logger.error(f"Error parsing Excel file {file_path}: {e}")
        raise e
