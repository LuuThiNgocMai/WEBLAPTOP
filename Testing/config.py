# Testing/config.py
GEMINI_API_KEY = "AIzaSyAzmn_Sr99IRp6xigdlYOaoRV2k6gOKON8"

# Base configuration for the laptop store automation
BASE_URL = "https://localhost:44396"

# Module-specific paths
URL_CONFIG = {
    "login": f"{BASE_URL}/Login",
    "register": f"{BASE_URL}/SignUp",
    "cart": f"{BASE_URL}/Cart",
    "profile": f"{BASE_URL}/Profile/Khachhang",
    "product": f"{BASE_URL}/Product"
}

# Timeout settings
DEFAULT_TIMEOUT = 10
IMPLICIT_WAIT = 5
