import json

def mock_logic(name, full_text):
    login_data = {
        "tên đăng nhập": "thanhtung",
        "mật khẩu": "abc123"
    }
    
    if any(k in full_text.lower() for k in ["rỗng", "trống", "empty", "blank", "không nhập", "bỏ trống"]):
        name_lower = name.lower()
        is_both = any(k in name_lower for k in ["cả hai", "all", "các trường"])
        
        if is_both:
            login_data["tên đăng nhập"] = ""
            login_data["mật khẩu"] = ""
        elif "tên đăng nhập" in name_lower or "username" in name_lower:
            login_data["tên đăng nhập"] = ""
            login_data["mật khẩu"] = "abc123"
        elif "mật khẩu" in name_lower or "password" in name_lower:
            login_data["tên đăng nhập"] = "thanhtung"
            login_data["mật khẩu"] = ""
            
    return login_data

# Test case 4
name4 = "Dang nhap that bai - De trong Ten dang nhap"
steps4 = "1. Click avatar\n2. Nhap mat khau\n3. Click dang nhap"
print(f"TC_04: {json.dumps(mock_logic(name4, name4 + ' ' + steps4), ensure_ascii=False)}")

# Test case 5
name5 = "Dang nhap that bai - De trong Mat khau"
steps5 = "1. Click avatar\n2. Nhap ten dang nhap\n3. Click dang nhap"
print(f"TC_05: {json.dumps(mock_logic(name5, name5 + ' ' + steps5), ensure_ascii=False)}")
