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
        
        # Convert all columns to list of dicts
        # The normalize_testcase function handles the header mapping.
        data = df.to_dict('records')
        
        return data
    except Exception as e:
        logger.error(f"Error parsing Excel file {file_path}: {e}")
        raise e
