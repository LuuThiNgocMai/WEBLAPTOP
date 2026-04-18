import pandas as pd
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names to match the system's expected names.
    Same logic as in excel_parser.
    """
    mapping = {
        'id': 'test_case_id',
        'test case id': 'test_case_id',
        'tc_id': 'test_case_id',
        'name': 'scenario',
        'test scenario': 'scenario',
        'test steps': 'steps',
        'step': 'steps',
        'precondition': 'precondition',
        'pre-condition': 'precondition',
        'module': 'module',
        'feature': 'module'
    }
    
    new_columns = {}
    for col in df.columns:
        norm_col = str(col).strip().lower()
        if norm_col in mapping:
            new_columns[col] = mapping[norm_col]
        elif norm_col.replace(' ', '_') in mapping.values():
            new_columns[col] = norm_col.replace(' ', '_')
            
    return df.rename(columns=new_columns)

def parse_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse a CSV file and return a list of dictionaries.
    """
    try:
        logger.info(f"Parsing CSV file: {file_path}")
        # Read CSV
        df = pd.read_csv(file_path)
        
        # Normalize columns
        df = normalize_columns(df)
        
        # Priority columns
        priority_cols = ['test_case_id', 'scenario', 'steps', 'precondition', 'module']
        
        # Ensure priority columns exist
        for col in priority_cols:
            if col not in df.columns:
                df[col] = ""
                
        # Fill NaN values
        df = df.fillna("")
        
        # Convert to list of dicts
        data = df[priority_cols].to_dict('records')
        
        return data
    except Exception as e:
        logger.error(f"Error parsing CSV file {file_path}: {e}")
        raise e
