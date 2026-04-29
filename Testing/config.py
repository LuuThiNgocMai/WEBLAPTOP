# Testing/config.py
GEMINI_API_KEY = "abccc"
MODEL_NAME = "gemini-2.5-flash" # Bạn có thể đổi thành "gemini-1.5-flash" hoặc "gemini-1.5-pro"

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
