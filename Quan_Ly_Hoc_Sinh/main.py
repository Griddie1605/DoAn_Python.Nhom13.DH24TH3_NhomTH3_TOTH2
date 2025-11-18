import sys
import os

# Dòng này thêm thư mục gốc của dự án vào Python path
# để đảm bảo Python tìm thấy 2 thư mục GiaoDien và Logic
# (Chỉ là một kỹ thuật để import hoạt động ổn định)
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import hàm mở form đăng nhập từ file GiaoDien
from GiaoDien.form_dang_nhap import open_form_dang_nhap

if __name__ == "__main__":
    # Đây là điểm bắt đầu của toàn bộ ứng dụng
    print("Ứng dụng bắt đầu...")
    
    # Gọi hàm để mở cửa sổ đăng nhập
    open_form_dang_nhap()
    
    print("Ứng dụng đã đóng.") 