import json
import os
import re

# Raw data from browser subagent
raw_data = {
    "Đăng ký": [
        {"STT": 1, "Mã TC": "REG_01", "Tên Test Case": "Đăng ký thành công với đầy đủ thông tin hợp lệ", "Mô tả": "Kiểm tra đăng ký tài khoản mới thành công", "Điều kiện tiên quyết": "Chưa tồn tại email & tên đăng nhập", "Các bước thực hiện": "1. Mở màn Trang chủ\n2. Click ĐĂNG NHẬP\n3. Click Đăng ký ngay\n4. Nhập đầy đủ thông tin hợp lệ\n5. Click ĐĂNG KÝ", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị thông báo đăng ký thành công -> chuyển hướng về trang Đăng nhập hoặc Dashboard"},
        {"STT": 2, "Mã TC": "REG_02", "Tên Test Case": "Đăng ký thất bại - Tên đăng nhập đã tồn tại", "Mô tả": "Kiểm tra trường hợp tên đăng nhập bị trùng", "Điều kiện tiên quyết": "Tên đăng nhập đã tồn tại", "Các bước thực hiện": "1. Mở màn Trang chủ\n2. Click ĐĂNG NHẬP\n3. Click Đăng ký ngay\n4. Nhập tên đăng nhập đã tồn tại\n5. Click ĐĂNG KÝ", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị lỗi: \"Tên đăng nhập đã tồn tại\""},
        {"STT": 3, "Mã TC": "REG_03", "Tên Test Case": "Đăng ký thất bại - Email đã tồn tại", "Mô tả": "Kiểm tra trường hợp email bị trùng", "Điều kiện tiên quyết": "Email đã tồn tại", "Các bước thực hiện": "1. Mở màn Trang chủ\n2. Click ĐĂNG NHẬP\n3. Click Đăng ký ngay\n4. Nhập email đã tồn tại\n5. Click ĐĂNG KÝ", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị lỗi: \"Email đã được sử dụng\""},
        {"STT": 4, "Mã TC": "REG_04", "Tên Test Case": "Đăng ký thất bại - Để trống Tên đăng nhập", "Mô tả": "Kiểm tra validation required field", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Mở màn Trang chủ\n2. Click ĐĂNG NHẬP\n3. Click Đăng ký ngay\n4. Để trống tên đăng nhập\n5. Click ĐĂNG KÝ", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị lỗi: \"Vui lòng nhập tên đăng nhập\""},
        {"STT": 5, "Mã TC": "REG_05", "Tên Test Case": "Đăng ký thất bại - Để trống Mật khẩu", "Mô tả": "Kiểm tra validation required field", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Mở màn Trang chủ\n2. Click ĐĂNG NHẬP\n3. Click Đăng ký ngay\n4. Để trống mật khẩu\n5. Click ĐĂNG KÝ", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị lỗi: \"Vui lòng nhập mật khẩu\""},
        {"STT": 6, "Mã TC": "REG_06", "Tên Test Case": "Đăng ký thất bại - Để trống Họ và tên", "Mô tả": "Kiểm tra validation required field", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Mở màn Trang chủ\n2. Click ĐĂNG NHẬP\n3. Click Đăng ký ngay\n4. Để trống Họ và tên\n5. Click ĐĂNG KÝ", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị lỗi: \"Vui lòng nhập họ và tên\""},
        {"STT": 7, "Mã TC": "REG_07", "Tên Test Case": "Đăng ký thất bại - Để trống Email", "Mô tả": "Kiểm tra validation required field", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Mở màn Trang chủ\n2. Click ĐĂNG NHẬP\n3. Click Đăng ký ngay\n4. Để trống email\n5. Click ĐĂNG KÝ", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị lỗi: \"Vui lòng nhập email\""},
        {"STT": 8, "Mã TC": "REG_08", "Tên Test Case": "Đăng ký thất bại - Email không đúng định dạng", "Mô tả": "Kiểm tra validation định dạng email", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Mở màn Trang chủ\n2. Click ĐĂNG NHẬP\n3. Click Đăng ký ngay\n4. Nhập email sai định dạng (thiếu @, .com...)\n5. Click ĐĂNG KÝ", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị lỗi: \"Email không hợp lệ\""},
        {"STT": 9, "Mã TC": "REG_09", "Tên Test Case": "Đăng ký thất bại - Số điện thoại không đúng định dạng", "Mô tả": "Kiểm tra validation số điện thoại", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Mở màn Trang chủ\n2. Click ĐĂNG NHẬP\n3. Click Đăng ký ngay\n4. Nhập số điện thoại sai định dạng (chứa chữ, quá dài/ngắn)\n5. Click ĐĂNG KÝ", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị lỗi: \"Số điện thoại không hợp lệ\""},
        {"STT": 10, "Mã TC": "REG_10", "Tên Test Case": "Đăng ký thất bại - Ngày sinh không hợp lệ", "Mô tả": "Kiểm tra validation ngày sinh (trong tương lai)", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Mở màn Trang chủ\n2. Click ĐĂNG NHẬP\n3. Click Đăng ký ngay\n4. Chọn ngày sinh trong tương lai\n5. Click ĐĂNG KÝ", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị lỗi: \"Ngày sinh không hợp lệ\""},
        {"STT": 11, "Mã TC": "REG_11", "Tên Test Case": "Đăng ký thất bại - Không chọn Giới tính", "Mô tả": "Kiểm tra validation giới tính", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Mở màn Trang chủ\n2. Click ĐĂNG NHẬP\n3. Click Đăng ký ngay\n4. Không chọn giới tính\n5. Click ĐĂNG KÝ", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị lỗi: \"Vui lòng chọn giới tính\""},
        {"STT": 12, "Mã TC": "REG_12", "Tên Test Case": "Kiểm tra độ dài tối thiểu & tối đa các trường", "Mô tả": "Kiểm tra boundary value (ví dụ tên đăng nhập 1-255 ký tự)", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập dữ liệu ở biên dưới và biên trên cho các trường\n2. Click ĐĂNG KÝ", "Dữ liệu test": "", "Kết quả mong đợi": "Thành công nếu trong biên, báo lỗi nếu vượt biên"},
        {"STT": 13, "Mã TC": "REG_13", "Tên Test Case": "Đăng ký thành công với ký tự đặc biệt trong họ tên", "Mô tả": "Kiểm tra xử lý ký tự đặc biệt", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập họ tên có dấu hoặc ký tự đặc biệt hợp lệ\n2. Click ĐĂNG KÝ", "Dữ liệu test": "", "Kết quả mong đợi": "Đăng ký thành công"},
        {"STT": 14, "Mã TC": "REG_14", "Tên Test Case": "Kiểm tra tính bảo mật của mật khẩu", "Mô tả": "Kiểm tra hiển thị mật khẩu dạng mã hóa", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập mật khẩu tại trường Mật khẩu", "Dữ liệu test": "", "Kết quả mong đợi": "Mật khẩu hiển thị dưới dạng dấu chấm hoặc dấu sao"},
        {"STT": 15, "Mã TC": "REG_15", "Tên Test Case": "Placeholder của các trường", "Mô tả": "Kiểm tra text gợi ý mặc định", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Mở trang đăng ký và quan sát các trường", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị đúng placeholder gợi ý cho từng trường"},
        {"STT": 16, "Mã TC": "REG_16", "Tên Test Case": "Kiểm tra mật khẩu bị che (ẩn)", "Mô tả": "Kiểm tra input type password", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập mật khẩu\n2. Quan sát hiển thị", "Dữ liệu test": "", "Kết quả mong đợi": "Ký tự ẩn (******)"},
        {"STT": 17, "Mã TC": "REG_17", "Tên Test Case": "Kiểm tra chọn ngày sinh từ Date Picker", "Mô tả": "Kiểm tra component Date Picker", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Click vào trường Ngày sinh\n2. Chọn một ngày từ bảng lịch hiện ra", "Dữ liệu test": "", "Kết quả mong đợi": "Ngày được điền đúng định dạng dd/MM/yyyy"},
        {"STT": 18, "Mã TC": "REG_18", "Tên Test Case": "Đăng ký với dữ liệu chứa ký tự đặc biệt (!@#...)", "Mô tả": "Kiểm tra xử lý ký tự đặc biệt chung", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập dữ liệu chứa ký tự lạ\n2. Click ĐĂNG KÝ", "Dữ liệu test": "", "Kết quả mong đợi": "Đăng ký thành công hoặc báo lỗi phù hợp quy tắc"}
    ],
    "Đăng nhập": [
        {"STT": 1, "Mã TC": "L_01", "Tên Test Case": "Đăng nhập thành công với tài khoản hợp lệ", "Mô tả": "Kiểm tra đăng nhập khi đúng Tên ĐN + MK", "Điều kiện tiên quyết": "Đã có tài khoản", "Các bước thực hiện": "1. Mở màn Đăng nhập\n2. Nhập đúng Tên ĐN & MK\n3. Click ĐĂNG NHẬP", "Dữ liệu test": "", "Kết quả mong đợi": "Chuyển hướng về Trang chủ / Dashboard"},
        {"STT": 2, "Mã TC": "L_02", "Tên Test Case": "Đăng nhập thành công bằng Google", "Mô tả": "Kiểm tra chức năng đăng nhập Google", "Điều kiện tiên quyết": "Có tài khoản Google", "Các bước thực hiện": "1. Click nút \"Đăng nhập bằng Google\"\n2. Xác thực tài khoản Google", "Dữ liệu test": "", "Kết quả mong đợi": "Đăng nhập thành công"},
        {"STT": 3, "Mã TC": "L_03", "Tên Test Case": "Đăng nhập thất bại - Tên đăng nhập không tồn tại", "Mô tả": "Kiểm tra lỗi khi sai tên ĐN", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập tên ĐN chưa đăng ký\n2. Click ĐĂNG NHẬP", "Dữ liệu test": "", "Kết quả mong đợi": "Thông báo: \"Tên đăng nhập hoặc mật khẩu không chính xác\""},
        {"STT": 4, "Mã TC": "L_04", "Tên Test Case": "Đăng nhập thất bại - Mật khẩu không đúng", "Mô tả": "Kiểm tra lỗi khi sai MK", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập đúng tên ĐN, sai MK\n2. Click ĐĂNG NHẬP", "Dữ liệu test": "", "Kết quả mong đợi": "Thông báo: \"Tên đăng nhập hoặc mật khẩu không chính xác\""},
        {"STT": 5, "Mã TC": "L_05", "Tên Test Case": "Đăng nhập thất bại - Để trống Tên đăng nhập", "Mô tả": "Validation trường bắt buộc", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Để trống Tên ĐN\n2. Click ĐĂNG NHẬP", "Dữ liệu test": "", "Kết quả mong đợi": "Lỗi: \"Vui lòng nhập tên đăng nhập\""},
        {"STT": 6, "Mã TC": "L_06", "Tên Test Case": "Đăng nhập thất bại - Để trống Mật khẩu", "Mô tả": "Validation trường bắt buộc", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Để trống MK\n2. Click ĐĂNG NHẬP", "Dữ liệu test": "", "Kết quả mong đợi": "Lỗi: \"Vui lòng nhập mật khẩu\""},
        {"STT": 7, "Mã TC": "L_07", "Tên Test Case": "Đăng nhập thất bại - Để trống cả hai trường", "Mô tả": "Validation cả hai", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Click ĐĂNG NHẬP khi chưa nhập gì", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị lỗi cho cả 2 trường"},
        {"STT": 8, "Mã TC": "L_08", "Tên Test Case": "Kiểm tra Placeholder của các trường", "Mô tả": "Check placeholder", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Quan sát màn đăng nhập", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị đúng text gợi ý"},
        {"STT": 9, "Mã TC": "L_09", "Tên Test Case": "Kiểm tra liên kết \"Đăng ký ngay\"", "Mô tả": "Check link chuyển hướng", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Click link \"Đăng ký ngay\"", "Dữ liệu test": "", "Kết quả mong đợi": "Chuyển hướng đến trang Đăng ký"},
        {"STT": 10, "Mã TC": "L_10", "Tên Test Case": "Kiểm tra liên kết \"Trở về trang chủ\"", "Mô tả": "Check link quay lại", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Click link \"Trở về trang chủ\"", "Dữ liệu test": "", "Kết quả mong đợi": "Chuyển về trang Home"},
        {"STT": 11, "Mã TC": "L_11", "Tên Test Case": "Kiểm tra hiển thị nút ĐĂNG NHẬP", "Mô tả": "Check trạng thái button", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Quan sát nút Đăng nhập", "Dữ liệu test": "", "Kết quả mong đợi": "Nút hiển thị rõ ràng, active"},
        {"STT": 12, "Mã TC": "L_12", "Tên Test Case": "Kiểm tra đăng nhập với ký tự đặc biệt", "Mô tả": "Check SQL Injection/Ký tự lạ", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập ký tự đặc biệt vào ô ĐN\n2. Click ĐĂNG NHẬP", "Dữ liệu test": "", "Kết quả mong đợi": "Hệ thống xử lý an toàn"},
        {"STT": 13, "Mã TC": "L_13", "Tên Test Case": "Kiểm tra giới hạn 255 ký tự Tên đăng nhập", "Mô tả": "Boundary length check", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập chuỗi 255 ký tự vào ô ĐN", "Dữ liệu test": "", "Kết quả mong đợi": "Xử lý đúng quy định (cho phép/báo lỗi)"},
        {"STT": 14, "Mã TC": "L_14", "Tên Test Case": "Kiểm tra giới hạn 128 ký tự Mật khẩu", "Mô tả": "Boundary length check", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập chuỗi 128 ký tự vào ô MK", "Dữ liệu test": "", "Kết quả mong đợi": "Xử lý đúng quy định"},
        {"STT": 15, "Mã TC": "L_15", "Tên Test Case": "Kiểm tra tính nhạy cảm chữ hoa/thường", "Mô tả": "Case-sensitive check", "Điều kiện tiên quyết": "Có tài khoản \"testuser\"", "Các bước thực hiện": "1. Nhập \"TESTUSER\" vào ô ĐN\n2. Nhập MK\n3. Click ĐĂNG NHẬP", "Dữ liệu test": "", "Kết quả mong đợi": "Thất bại nếu hệ thống phân biệt hoa thường"}
    ],
    "Xem chi tiết": [
        {"STT": 1, "Mã TC": "ViewP_001", "Tên Test Case": "Xem chi tiết sản phẩm thành công", "Mô tả": "Luồng cơ bản", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Chọn một sản phẩm bất kỳ từ danh sách", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị đầy đủ thông tin sản phẩm"},
        {"STT": 2, "Mã TC": "ViewP_002", "Tên Test Case": "Xem chi tiết sản phẩm khi lỗi CSDL", "Mô tả": "Xử lý ngoại lệ", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Click vào sản phẩm khi DB down", "Dữ liệu test": "", "Kết quả mong đợi": "Thông báo lỗi kết nối CSDL"},
        {"STT": 3, "Mã TC": "ViewP_003", "Tên Test Case": "Kiểm tra hiển thị đầy đủ thông tin", "Mô tả": "Giao diện và dữ liệu", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Xem chi tiết sản phẩm", "Dữ liệu test": "", "Kết quả mong đợi": "Load nhanh, đầy đủ ảnh, giá, mô tả"},
        {"STT": 4, "Mã TC": "ViewP_004", "Tên Test Case": "Kiểm tra sản phẩm không tồn tại", "Mô tả": "URL không hợp lệ", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập URL sản phẩm sai id (vd: /999999)", "Dữ liệu test": "", "Kết quả mong đợi": "Lỗi 404 hoặc thông báo không tồn tại"}
    ],
    "Tìm kiếm": [
        {"STT": 1, "Mã TC": "S_01", "Tên Test Case": "Tìm kiếm bằng tên chính xác", "Mô tả": "Exact match", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập đúng tên sản phẩm\n2. Nhấn Tìm kiếm", "Dữ liệu test": "Laptop Dell XPS", "Kết quả mong đợi": "Hiển thị đúng sản phẩm đó"},
        {"STT": 2, "Mã TC": "S_02", "Tên Test Case": "Tìm kiếm bằng từ khóa một phần", "Mô tả": "Partial match", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập một phần tên\n2. Nhấn Tìm kiếm", "Dữ liệu test": "Dell", "Kết quả mong đợi": "Hiển thị tất cả sản phẩm chứa chữ \"Dell\""},
        {"STT": 3, "Mã TC": "S_03", "Tên Test Case": "Tìm kiếm không có kết quả", "Mô tả": "No result", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập chuỗi ngẫu nhiên\n2. Nhấn Tìm kiếm", "Dữ liệu test": "xyzabc123", "Kết quả mong đợi": "Thông báo: \"Không tìm thấy sản phẩm phù hợp\""},
        {"STT": 4, "Mã TC": "S_04", "Tên Test Case": "Tìm kiếm khi để trống", "Mô tả": "Empty input", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Để trống ô tìm kiếm\n2. Nhấn Enter", "Dữ liệu test": "", "Kết quả mong đợi": "Hiển thị tất cả sản phẩm hoặc không làm gì"},
        {"STT": 5, "Mã TC": "S_05", "Tên Test Case": "Tìm kiếm với ký tự đặc biệt", "Mô tả": "Special chars", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập !@#$%\n2. Nhấn Tìm kiếm", "Dữ liệu test": "", "Kết quả mong đợi": "Xử lý an toàn, báo không tìm thấy"}
    ],
    "Giỏ hàng": [
        {"STT": 1, "Mã TC": "Cart_001", "Tên Test Case": "Thêm sản phẩm thành công", "Mô tả": "Add to cart", "Điều kiện tiên quyết": "Đã đăng nhập", "Các bước thực hiện": "1. Click biểu tượng giỏ hàng tại sản phẩm", "Dữ liệu test": "", "Kết quả mong đợi": "Thông báo thành công, số lượng giỏ tăng"},
        {"STT": 2, "Mã TC": "Cart_002", "Tên Test Case": "Tăng số lượng sản phẩm", "Mô tả": "Click (+)", "Điều kiện tiên quyết": "Giỏ có hàng", "Các bước thực hiện": "1. Click nút \"+\" tại sản phẩm", "Dữ liệu test": "", "Kết quả mong đợi": "Số lượng tăng, tổng tiền cập nhật đúng"},
        {"STT": 3, "Mã TC": "Cart_003", "Tên Test Case": "Giảm số lượng sản phẩm", "Mô tả": "Click (-)", "Điều kiện tiên quyết": "Giỏ có hàng (>1)", "Các bước thực hiện": "1. Click nút \"-\" tại sản phẩm", "Dữ liệu test": "", "Kết quả mong đợi": "Số lượng giảm, tổng tiền cập nhật đúng"},
        {"STT": 4, "Mã TC": "Cart_004", "Tên Test Case": "Xóa một sản phẩm", "Mô tả": "Remove item", "Điều kiện tiên quyết": "Giỏ có hàng", "Các bước thực hiện": "1. Click nút \"X\" xóa sản phẩm", "Dữ liệu test": "", "Kết quả mong đợi": "Sản phẩm mất khỏi giỏ hàng"},
        {"STT": 5, "Mã TC": "Cart_005", "Tên Test Case": "Xóa toàn bộ giỏ hàng", "Mô tả": "Clear all", "Điều kiện tiên quyết": "Giỏ có nhiều hàng", "Các bước thực hiện": "1. Click Xóa tất cả", "Dữ liệu test": "", "Kết quả mong đợi": "Giỏ hàng rỗng"},
        {"STT": 6, "Mã TC": "Cart_006", "Tên Test Case": "Giảm số lượng xuống 0", "Mô tả": "Decrement to zero", "Điều kiện tiên quyết": "Giỏ có hàng", "Các bước thực hiện": "1. Click nút \"-\" cho đến khi về 0", "Dữ liệu test": "", "Kết quả mong đợi": "Sản phẩm tự động bị xóa"},
        {"STT": 7, "Mã TC": "Cart_007", "Tên Test Case": "Thêm cùng một sản phẩm nhiều lần", "Mô tả": "Duplicate add", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Click thêm liên tiếp 1 sản phẩm", "Dữ liệu test": "", "Kết quả mong đợi": "Cộng dồn số lượng, không tạo dòng mới"},
        {"STT": 8, "Mã TC": "Cart_008", "Tên Test Case": "Lỗi CSDL khi thao tác giỏ hàng", "Mô tả": "DB error handling", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Thao tác giỏ hàng khi lỗi server", "Dữ liệu test": "", "Kết quả mong đợi": "Thông báo lỗi lịch sự, không crash"},
        {"STT": 9, "Mã TC": "Cart_009", "Tên Test Case": "Hiển thị giỏ hàng trống", "Mô tả": "Empty cart view", "Điều kiện tiên quyết": "Giỏ chưa có hàng", "Các bước thực hiện": "1. Vào trang Giỏ hàng", "Dữ liệu test": "", "Kết quả mong đợi": "Thông báo: \"Giỏ hàng của bạn đang trống\""},
        {"STT": 10, "Mã TC": "Cart_010", "Tên Test Case": "Cập nhật tổng tiền chính xác", "Mô tả": "Calculation check", "Điều kiện tiên quyết": "Giỏ có hàng", "Các bước thực hiện": "1. Thay đổi số lượng nhiều sản phẩm", "Dữ liệu test": "", "Kết quả mong đợi": "Tổng tiền = Sum(Đơn giá * Số lượng)"}
    ],
    "Quản lý tài khoản": [
        {"STT": 1, "Mã TC": "User_001", "Tên Test Case": "Đăng ký thành công", "Mô tả": "User registration", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Thực hiện các bước đăng ký hợp lệ", "Dữ liệu test": "", "Kết quả mong đợi": "Tạo tài khoản thành công"},
        {"STT": 2, "Mã TC": "User_002", "Tên Test Case": "Đăng nhập thành công", "Mô tả": "User login", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Đăng nhập với tài khoản mới", "Dữ liệu test": "", "Kết quả mong đợi": "Vào được hệ thống, hiện tên user"},
        {"STT": 3, "Mã TC": "User_003", "Tên Test Case": "Đăng xuất tài khoản", "Mô tả": "Logout", "Điều kiện tiên quyết": "Đang đăng nhập", "Các bước thực hiện": "1. Click ĐĂNG XUẤT", "Dữ liệu test": "", "Kết quả mong đợi": "Hết session, quay về Home/Login"},
        {"STT": 4, "Mã TC": "User_004", "Tên Test Case": "Cập nhật thông tin tài khoản", "Mô tả": "Update profile", "Điều kiện tiên quyết": "Đang đăng nhập", "Các bước thực hiện": "1. Vào Quản lý tài khoản\n2. Chỉnh sửa Họ tên, SĐT\n3. Click LƯU", "Dữ liệu test": "", "Kết quả mong đợi": "Thông tin được cập nhật thành công"},
        {"STT": 5, "Mã TC": "User_005", "Tên Test Case": "Thay đổi mật khẩu", "Mô tả": "Change password", "Điều kiện tiên quyết": "Đang đăng nhập", "Các bước thực hiện": "1. Nhập MK cũ, MK mới\n2. Click LƯU", "Dữ liệu test": "", "Kết quả mong đợi": "Đổi mật khẩu thành công"},
        {"STT": 6, "Mã TC": "User_006", "Tên Test Case": "Cập nhật thất bại - Để trống trường", "Mô tả": "Validation update", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Xóa họ tên và Lưu", "Dữ liệu test": "", "Kết quả mong đợi": "Lỗi: \"Vui lòng nhập họ và tên\""},
        {"STT": 7, "Mã TC": "User_007", "Tên Test Case": "Cập nhật thất bại - Email sai", "Mô tả": "Validation update email", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Nhập email sai định dạng và Lưu", "Dữ liệu test": "", "Kết quả mong đợi": "Lỗi: \"Email không hợp lệ\""},
        {"STT": 8, "Mã TC": "User_008", "Tên Test Case": "Quên mật khẩu", "Mô tả": "Forgot password flow", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Click Quên mật khẩu\n2. Nhập email đăng ký", "Dữ liệu test": "", "Kết quả mong đợi": "Hệ thống gửi mã/link reset về email"},
        {"STT": 9, "Mã TC": "User_009", "Tên Test Case": "Lỗi CSDL trong quản lý tài khoản", "Mô tả": "Error handling", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Thao tác khi mất kết nối", "Dữ liệu test": "", "Kết quả mong đợi": "Báo lỗi hệ thống, không crash"},
        {"STT": 10, "Mã TC": "User_010", "Tên Test Case": "Kiểm tra hiển thị thông tin sau cập nhật", "Mô tả": "Data persistence", "Điều kiện tiên quyết": "-", "Các bước thực hiện": "1. Cập nhật -> Đăng xuất -> Đăng nhập lại", "Dữ liệu test": "", "Kết quả mong đợi": "Thông tin mới vẫn được lưu và hiển thị đúng"}
    ]
}

def parse_steps(steps_str):
    if not steps_str: return []
    lines = [line.strip() for line in str(steps_str).split('\n') if line.strip()]
    parsed = []
    for i, line in enumerate(lines):
        match = re.match(r'^(\d+)[\.\s\)-]+(.*)', line)
        content = match.group(2).strip() if match else line
        parsed.append({"so_buoc": i+1, "noi_dung": content})
    return parsed

standardized = []
global_stt = 1
for sheet_name, rows in raw_data.items():
    for row in rows:
        standardized.append({
            "stt": global_stt,
            "ma_tc": row.get("Mã TC", f"TC_{global_stt}"),
            "ten_test_case": row.get("Tên Test Case", ""),
            "mo_ta": row.get("Mô tả", ""),
            "dieu_kien_tien_quyet": row.get("Điều kiện tiên quyết", ""),
            "cac_buoc_thuc_hien_goc": row.get("Các bước thực hiện", ""),
            "danh_sach_buoc": parse_steps(row.get("Các bước thực hiện", "")),
            "du_lieu_test_goc": row.get("Dữ liệu test", ""),
            "ket_qua_mong_doi": row.get("Kết quả mong đợi", ""),
            "ghi_chu_tu_dong_hoa": f"module={sheet_name}",
            "buoc_chi_tiet_ai": [],
            "du_lieu_test_ai": {},
            "trang_thai_review": "NEW"
        })
        global_stt += 1

output_path = r"d:\DATN - Mai\Testing\data\testcase_chuan_hoa.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(standardized, f, ensure_ascii=False, indent=2)

print(f"Successfully saved {len(standardized)} test cases to {output_path}")
