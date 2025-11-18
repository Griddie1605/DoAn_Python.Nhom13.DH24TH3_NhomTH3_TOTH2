import mysql.connector
from mysql.connector import Error

def tao_ket_noi():
    """Hàm tạo kết nối đến CSDL MySQL"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',          
            user='root',               
            password='Grid0378095005',  
            database='Quan_Ly_Hoc_Sinh' 
        )
        print("Kết nối MySQL thành công ")
    except Error as e:
        print(f"Lỗi khi kết nối đến MySQL: {e}")
    return connection

def kiem_tra_dang_nhap(ten_dang_nhap, mat_khau):
    """
    Hàm kiểm tra logic đăng nhập.
    Kết nối CSDL, truy vấn bảng TaiKhoan.
    Trả về 'vai_tro' nếu thành công, trả về None nếu thất bại.
    """
    connection = tao_ket_noi()
    if connection is None:
        return None # Không thể kết nối

    cursor = None
    try:
        cursor = connection.cursor()
        
        # Câu lệnh SQL (dùng %s để tránh SQL Injection)
        # So sánh mật khẩu 
        sql_query = """
            SELECT vai_tro FROM TaiKhoan 
            WHERE ten_dang_nhap = %s AND mat_khau = %s
        """
        
        # Dữ liệu truyền vào
        data_tuple = (ten_dang_nhap, mat_khau)
        
        cursor.execute(sql_query, data_tuple)
        
        # Lấy kết quả
        result = cursor.fetchone() # Lấy 1 hàng kết quả
        
        if result:
            # result là một tuple, ví dụ ('admin',). Ta lấy phần tử đầu tiên
            vai_tro = result[0]
            print(f" Đăng nhập thành công. Vai trò: {vai_tro}")
            return vai_tro
        else:
            # Không tìm thấy hàng nào khớp
            print(" Sai tên đăng nhập hoặc mật khẩu.")
            return None
            
    except Error as e:
        print(f"Lỗi khi truy vấn: {e}")
        return None
        
    finally:
        # Luôn đóng cursor và connection
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Đã đóng kết nối MySQL.")
          
          
            
            
            
# --- CÁC HÀM MỚI CHO NGHIỆP VỤ QUẢN LÝ HỌC SINH ---

def lay_danh_sach_lop():
    """Lấy danh sách mã lớp để nạp vào ComboBox"""
    connection = tao_ket_noi()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = "SELECT ma_lop FROM LopHoc"
        cursor.execute(sql_query)
        
        # Lấy tất cả kết quả
        results = cursor.fetchall() 
        
        # Chuyển đổi từ [('10A1',), ('10A2',)] sang ['10A1', '10A2']
        lop_list = [row[0] for row in results]
        
        print(f"[BACK-END LOGIC] Lấy danh sách lớp thành công: {lop_list}")
        return lop_list
        
    except Error as e:
        print(f"Lỗi khi lấy danh sách lớp: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def lay_tat_ca_hoc_sinh():
    """Lấy tất cả học sinh từ CSDL để hiển thị lên Treeview"""
    connection = tao_ket_noi()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor()
        # Lấy tất cả các cột
        sql_query = "SELECT ma_hoc_sinh, ho_ten, ngay_sinh, gioi_tinh, dia_chi, email, so_dien_thoai, ma_lop FROM HocSinh"
        cursor.execute(sql_query)
        
        results = cursor.fetchall()
        print("[BACK-END LOGIC] Lấy danh sách học sinh thành công.")
        # Trả về danh sách các tuple, ví dụ: [ ('HS001', 'An', ...), ('HS002', 'Binh', ...) ]
        return results
        
    except Error as e:
        print(f"Lỗi khi lấy danh sách học sinh: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def them_hoc_sinh(ma_hs, ho_ten, ngay_sinh, gioi_tinh, dia_chi, email, sdt, ma_lop):
    """Thêm một học sinh mới vào CSDL"""
    connection = tao_ket_noi()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = """
            INSERT INTO HocSinh 
            (ma_hoc_sinh, ho_ten, ngay_sinh, gioi_tinh, dia_chi, email, so_dien_thoai, ma_lop)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        data_tuple = (ma_hs, ho_ten, ngay_sinh, gioi_tinh, dia_chi, email, sdt, ma_lop)
        
        cursor.execute(sql_query, data_tuple)
        connection.commit() # Rất quan trọng: commit() để lưu thay đổi
        
        print(f"[BACK-END LOGIC] Thêm học sinh {ma_hs} thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi thêm học sinh: {e}")
        connection.rollback() # Hoàn tác nếu có lỗi
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def sua_hoc_sinh(ma_hs, ho_ten, ngay_sinh, gioi_tinh, dia_chi, email, sdt, ma_lop):
    """Cập nhật thông tin học sinh dựa theo ma_hs"""
    connection = tao_ket_noi()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = """
            UPDATE HocSinh
            SET ho_ten = %s, ngay_sinh = %s, gioi_tinh = %s, 
                dia_chi = %s, email = %s, so_dien_thoai = %s, ma_lop = %s
            WHERE ma_hoc_sinh = %s
        """
        # Chú ý: ma_hs nằm ở cuối cùng trong tuple
        data_tuple = (ho_ten, ngay_sinh, gioi_tinh, dia_chi, email, sdt, ma_lop, ma_hs)
        
        cursor.execute(sql_query, data_tuple)
        connection.commit()
        
        print(f"[BACK-END LOGIC] Sửa học sinh {ma_hs} thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi sửa học sinh: {e}")
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def xoa_hoc_sinh(ma_hs):
    """Xóa học sinh dựa trên ma_hs"""
    connection = tao_ket_noi()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = "DELETE FROM HocSinh WHERE ma_hoc_sinh = %s"
        data_tuple = (ma_hs,) # (Phải có dấu phẩy để nó hiểu là tuple 1 phần tử)
        
        cursor.execute(sql_query, data_tuple)
        connection.commit()
        
        print(f"[BACK-END LOGIC] Xóa học sinh {ma_hs} thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi xóa học sinh: {e}")
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            
            
            
            
            
# --- CÁC HÀM MỚI CHO NGHIỆP VỤ QUẢN LÝ GIÁO VIÊN ---

def lay_tat_ca_giao_vien():
    """Lấy tất cả giáo viên từ CSDL"""
    connection = tao_ket_noi()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = "SELECT ma_giao_vien, ho_ten, ngay_sinh, gioi_tinh, email, so_dien_thoai, chuyen_mon FROM GiaoVien"
        cursor.execute(sql_query)
        
        results = cursor.fetchall()
        print("[BACK-END LOGIC] Lấy danh sách giáo viên thành công.")
        return results
        
    except Error as e:
        print(f"Lỗi khi lấy danh sách giáo viên: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def them_giao_vien(ma_gv, ho_ten, ngay_sinh, gioi_tinh, email, sdt, chuyen_mon):
    """Thêm một giáo viên mới (chưa xử lý tài khoản)"""
    connection = tao_ket_noi()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = """
            INSERT INTO GiaoVien 
            (ma_giao_vien, ho_ten, ngay_sinh, gioi_tinh, email, so_dien_thoai, chuyen_mon)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data_tuple = (ma_gv, ho_ten, ngay_sinh, gioi_tinh, email, sdt, chuyen_mon)
        
        cursor.execute(sql_query, data_tuple)
        connection.commit()
        
        print(f"[BACK-END LOGIC] Thêm giáo viên {ma_gv} thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi thêm giáo viên: {e}")
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def sua_giao_vien(ma_gv, ho_ten, ngay_sinh, gioi_tinh, email, sdt, chuyen_mon):
    """Cập nhật thông tin giáo viên"""
    connection = tao_ket_noi()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = """
            UPDATE GiaoVien
            SET ho_ten = %s, ngay_sinh = %s, gioi_tinh = %s, 
                email = %s, so_dien_thoai = %s, chuyen_mon = %s
            WHERE ma_giao_vien = %s
        """
        data_tuple = (ho_ten, ngay_sinh, gioi_tinh, email, sdt, chuyen_mon, ma_gv)
        
        cursor.execute(sql_query, data_tuple)
        connection.commit()
        
        print(f"[BACK-END LOGIC] Sửa giáo viên {ma_gv} thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi sửa giáo viên: {e}")
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def xoa_giao_vien(ma_gv):
    """Xóa giáo viên"""
    connection = tao_ket_noi()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = "DELETE FROM GiaoVien WHERE ma_giao_vien = %s"
        data_tuple = (ma_gv,)
        
        cursor.execute(sql_query, data_tuple)
        connection.commit()
        
        print(f"[BACK-END LOGIC] Xóa giáo viên {ma_gv} thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi xóa giáo viên: {e}")
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            
            
            
            
            
# --- CÁC HÀM MỚI CHO NGHIỆP VỤ QUẢN LÝ LỚP HỌC ---

def lay_danh_sach_gv_cho_combobox():
    """Lấy Mã GV và Tên GV để nạp vào ComboBox chủ nhiệm"""
    connection = tao_ket_noi()
    if connection is None:
        return [] # Trả về list rỗng

    cursor = None
    try:
        cursor = connection.cursor()
        # Chỉ lấy 2 cột cần thiết
        sql_query = "SELECT ma_giao_vien, ho_ten FROM GiaoVien"
        cursor.execute(sql_query)
        
        results = cursor.fetchall() 
        # results sẽ là [ ('GV001', 'Cô A'), ('GV002', 'Thầy B') ]
        print("[BACK-END LOGIC] Lấy danh sách GV cho ComboBox thành công.")
        return results
        
    except Error as e:
        print(f"Lỗi khi lấy danh sách GV (ComboBox): {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def lay_tat_ca_lop():
    """Lấy thông tin lớp học, JOIN với GiaoVien để lấy Tên GVCN"""
    connection = tao_ket_noi()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor()
        # Dùng LEFT JOIN phòng trường hợp có lớp chưa được gán GVCN
        sql_query = """
            SELECT 
                LopHoc.ma_lop, 
                LopHoc.ten_lop, 
                LopHoc.nien_khoa, 
                LopHoc.ma_giao_vien_chu_nhiem,
                GiaoVien.ho_ten 
            FROM LopHoc
            LEFT JOIN GiaoVien ON LopHoc.ma_giao_vien_chu_nhiem = GiaoVien.ma_giao_vien
        """
        cursor.execute(sql_query)
        
        results = cursor.fetchall()
        print("[BACK-END LOGIC] Lấy danh sách lớp học thành công.")
        # Ví dụ: [ ('10A1', 'Lớp 10A1', '2024-2027', 'GV001', 'Cô A'), ... ]
        return results
        
    except Error as e:
        print(f"Lỗi khi lấy danh sách lớp học: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def them_lop(ma_lop, ten_lop, nien_khoa, ma_gvcn):
    """Thêm một lớp học mới"""
    connection = tao_ket_noi()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = """
            INSERT INTO LopHoc 
            (ma_lop, ten_lop, nien_khoa, ma_giao_vien_chu_nhiem)
            VALUES (%s, %s, %s, %s)
        """
        # Nếu ma_gvcn rỗng, gán nó là None
        if not ma_gvcn: 
            ma_gvcn = None
            
        data_tuple = (ma_lop, ten_lop, nien_khoa, ma_gvcn)
        
        cursor.execute(sql_query, data_tuple)
        connection.commit()
        
        print(f"[BACK-END LOGIC] Thêm lớp {ma_lop} thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi thêm lớp: {e}")
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def sua_lop(ma_lop, ten_lop, nien_khoa, ma_gvcn):
    """Cập nhật thông tin lớp học"""
    connection = tao_ket_noi()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = """
            UPDATE LopHoc
            SET ten_lop = %s, nien_khoa = %s, ma_giao_vien_chu_nhiem = %s
            WHERE ma_lop = %s
        """
        if not ma_gvcn:
            ma_gvcn = None
            
        data_tuple = (ten_lop, nien_khoa, ma_gvcn, ma_lop)
        
        cursor.execute(sql_query, data_tuple)
        connection.commit()
        
        print(f"[BACK-END LOGIC] Sửa lớp {ma_lop} thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi sửa lớp: {e}")
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def xoa_lop(ma_lop):
    """Xóa lớp học"""
    connection = tao_ket_noi()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = "DELETE FROM LopHoc WHERE ma_lop = %s"
        data_tuple = (ma_lop,)
        
        cursor.execute(sql_query, data_tuple)
        connection.commit()
        
        print(f"[BACK-END LOGIC] Xóa lớp {ma_lop} thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi xóa lớp: {e}")
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()           







# --- CÁC HÀM MỚI CHO NGHIỆP VỤ QUẢN LÝ MÔN HỌC ---

def lay_tat_ca_mon_hoc():
    """Lấy tất cả môn học từ CSDL"""
    connection = tao_ket_noi()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = "SELECT ma_mon_hoc, ten_mon_hoc FROM MonHoc"
        cursor.execute(sql_query)
        
        results = cursor.fetchall()
        print("[BACK-END LOGIC] Lấy danh sách môn học thành công.")
        return results
        
    except Error as e:
        print(f"Lỗi khi lấy danh sách môn học: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def them_mon_hoc(ma_mh, ten_mh):
    """Thêm một môn học mới"""
    connection = tao_ket_noi()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = """
            INSERT INTO MonHoc (ma_mon_hoc, ten_mon_hoc)
            VALUES (%s, %s)
        """
        data_tuple = (ma_mh, ten_mh)
        
        cursor.execute(sql_query, data_tuple)
        connection.commit()
        
        print(f"[BACK-END LOGIC] Thêm môn học {ma_mh} thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi thêm môn học: {e}")
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def sua_mon_hoc(ma_mh, ten_mh):
    """Cập nhật thông tin môn học"""
    connection = tao_ket_noi()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = """
            UPDATE MonHoc
            SET ten_mon_hoc = %s
            WHERE ma_mon_hoc = %s
        """
        data_tuple = (ten_mh, ma_mh)
        
        cursor.execute(sql_query, data_tuple)
        connection.commit()
        
        print(f"[BACK-END LOGIC] Sửa môn học {ma_mh} thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi sửa môn học: {e}")
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def xoa_mon_hoc(ma_mh):
    """Xóa môn học"""
    connection = tao_ket_noi()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = "DELETE FROM MonHoc WHERE ma_mon_hoc = %s"
        data_tuple = (ma_mh,)
        
        cursor.execute(sql_query, data_tuple)
        connection.commit()
        
        print(f"[BACK-END LOGIC] Xóa môn học {ma_mh} thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi xóa môn học: {e}")
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close() 







# --- CÁC HÀM MỚI CHO NGHIỆP VỤ PHÂN CÔNG GIẢNG DẠY ---

def lay_tat_ca_lop_cho_combobox():
    """Chỉ lấy mã lớp và tên lớp cho ComboBox"""
    connection = tao_ket_noi()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = "SELECT ma_lop, ten_lop FROM LopHoc"
        cursor.execute(sql_query)
        results = cursor.fetchall()
        print("[BACK-END LOGIC] Lấy danh sách lớp (ComboBox) thành công.")
        return results # Trả về list of tuples: [('10A1', 'Lớp 10A1'), ...]
        
    except Error as e:
        print(f"Lỗi khi lấy danh sách lớp (ComboBox): {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def lay_tat_ca_mon_hoc_cho_combobox():
    """Chỉ lấy mã môn và tên môn cho ComboBox"""
    connection = tao_ket_noi()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = "SELECT ma_mon_hoc, ten_mon_hoc FROM MonHoc"
        cursor.execute(sql_query)
        results = cursor.fetchall()
        print("[BACK-END LOGIC] Lấy danh sách môn học (ComboBox) thành công.")
        return results # Trả về list of tuples: [('TOAN', 'Toán'), ...]
        
    except Error as e:
        print(f"Lỗi khi lấy danh sách môn học (ComboBox): {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def lay_danh_sach_phan_cong():
    """Lấy toàn bộ bảng phân công, JOIN để lấy tên"""
    connection = tao_ket_noi()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor()
        # JOIN 4 bảng: PhanCong, GiaoVien, LopHoc, MonHoc
        sql_query = """
            SELECT 
                pc.id_phan_cong,
                gv.ho_ten,
                lh.ten_lop,
                mh.ten_mon_hoc,
                pc.hoc_ky,
                pc.nam_hoc
            FROM PhanCongGiangDay pc
            JOIN GiaoVien gv ON pc.ma_giao_vien = gv.ma_giao_vien
            JOIN LopHoc lh ON pc.ma_lop = lh.ma_lop
            JOIN MonHoc mh ON pc.ma_mon_hoc = mh.ma_mon_hoc
            ORDER BY gv.ho_ten, lh.ten_lop
        """
        cursor.execute(sql_query)
        
        results = cursor.fetchall()
        print("[BACK-END LOGIC] Lấy danh sách phân công thành công.")
        # Ví dụ: [ (1, 'Cô A', 'Lớp 10A1', 'Toán', 1, '2024-2025'), ... ]
        return results
        
    except Error as e:
        print(f"Lỗi khi lấy danh sách phân công: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def them_phan_cong(ma_gv, ma_lop, ma_mh, hoc_ky, nam_hoc):
    """Thêm một phân công giảng dạy mới"""
    connection = tao_ket_noi()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = """
            INSERT INTO PhanCongGiangDay 
            (ma_giao_vien, ma_lop, ma_mon_hoc, hoc_ky, nam_hoc)
            VALUES (%s, %s, %s, %s, %s)
        """
        data_tuple = (ma_gv, ma_lop, ma_mh, hoc_ky, nam_hoc)
        
        cursor.execute(sql_query, data_tuple)
        connection.commit()
        
        print(f"[BACK-END LOGIC] Thêm phân công thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi thêm phân công: {e}")
        connection.rollback()
        return False # Có thể là lỗi UNIQUE (phân công đã tồn tại)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def xoa_phan_cong(id_phan_cong):
    """Xóa phân công dựa trên ID tự tăng của nó"""
    connection = tao_ket_noi()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = "DELETE FROM PhanCongGiangDay WHERE id_phan_cong = %s"
        data_tuple = (id_phan_cong,)
        
        cursor.execute(sql_query, data_tuple)
        connection.commit()
        
        print(f"[BACK-END LOGIC] Xóa phân công {id_phan_cong} thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi xóa phân công: {e}")
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            
            
            
            


# --- CÁC HÀM MỚI CHO NGHIỆP VỤ QUẢN LÝ ĐIỂM ---

def tim_ma_giao_vien_tu_ten_dang_nhap(ten_dang_nhap):
    """Tìm ma_giao_vien từ ten_dang_nhap (username)"""
    connection = tao_ket_noi()
    if connection is None:
        return None

    cursor = None
    try:
        cursor = connection.cursor()
        # JOIN 2 bảng TaiKhoan và GiaoVien
        sql_query = """
            SELECT gv.ma_giao_vien 
            FROM GiaoVien gv
            JOIN TaiKhoan tk ON gv.id_tai_khoan = tk.id_tai_khoan
            WHERE tk.ten_dang_nhap = %s
        """
        cursor.execute(sql_query, (ten_dang_nhap,))
        
        result = cursor.fetchone()
        if result:
            print(f"[BACK-END LOGIC] Tìm thấy {ten_dang_nhap} là GV mã: {result[0]}")
            return result[0] # Trả về ma_giao_vien
        else:
            print(f"[BACK-END LOGIC] Không tìm thấy GV cho {ten_dang_nhap}")
            return None
        
    except Error as e:
        print(f"Lỗi khi tìm mã giáo viên: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def lay_lop_gv_day(ma_giao_vien):
    """Lấy danh sách (ma_lop, ten_lop) mà GV được phân công"""
    connection = tao_ket_noi()
    if connection is None: return []
    cursor = None
    try:
        cursor = connection.cursor()
        # Lấy các lớp phân biệt (DISTINCT)
        sql_query = """
            SELECT DISTINCT lh.ma_lop, lh.ten_lop
            FROM PhanCongGiangDay pc
            JOIN LopHoc lh ON pc.ma_lop = lh.ma_lop
            WHERE pc.ma_giao_vien = %s
            ORDER BY lh.ten_lop
        """
        cursor.execute(sql_query, (ma_giao_vien,))
        results = cursor.fetchall()
        print(f"[BACK-END LOGIC] GV {ma_giao_vien} dạy các lớp: {results}")
        return results
    except Error as e:
        print(f"Lỗi khi lấy lớp GV dạy: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if connection and connection.is_connected(): connection.close()

def lay_mon_gv_day_trong_lop(ma_giao_vien, ma_lop):
    """Lấy danh sách (ma_mon_hoc, ten_mon_hoc) mà GV dạy cho 1 lớp cụ thể"""
    connection = tao_ket_noi()
    if connection is None: return []
    cursor = None
    try:
        cursor = connection.cursor()
        sql_query = """
            SELECT DISTINCT mh.ma_mon_hoc, mh.ten_mon_hoc
            FROM PhanCongGiangDay pc
            JOIN MonHoc mh ON pc.ma_mon_hoc = mh.ma_mon_hoc
            WHERE pc.ma_giao_vien = %s AND pc.ma_lop = %s
            ORDER BY mh.ten_mon_hoc
        """
        cursor.execute(sql_query, (ma_giao_vien, ma_lop))
        results = cursor.fetchall()
        print(f"[BACK-END LOGIC] GV {ma_giao_vien} dạy môn {results} cho lớp {ma_lop}")
        return results
    except Error as e:
        print(f"Lỗi khi lấy môn GV dạy: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if connection and connection.is_connected(): connection.close()

def lay_hoc_sinh_va_diem(ma_lop, ma_mon_hoc, hoc_ky, nam_hoc):
    """
    Lấy danh sách HS của 1 lớp VÀ điểm số (nếu có) của môn đó.
    Đây là hàm JOIN phức tạp.
    """
    connection = tao_ket_noi()
    if connection is None: return []
    cursor = None
    try:
        cursor = connection.cursor()
        # Dùng LEFT JOIN từ HocSinh -> DiemSo
        # Để lấy TẤT CẢ học sinh, kể cả học sinh chưa có điểm
        sql_query = """
            SELECT 
                hs.ma_hoc_sinh, 
                hs.ho_ten,
                ds.diem_15phut_1,
                ds.diem_15phut_2,
                ds.diem_1tiet_1,
                ds.diem_1tiet_2,
                ds.diem_cuoi_ky,
                ds.id_diem -- Dùng để biết HS đã có điểm hay chưa (NULL or NOT NULL)
            FROM HocSinh hs
            LEFT JOIN DiemSo ds ON hs.ma_hoc_sinh = ds.ma_hoc_sinh
                AND ds.ma_mon_hoc = %s
                AND ds.hoc_ky = %s
                AND ds.nam_hoc = %s
            WHERE hs.ma_lop = %s
            ORDER BY hs.ho_ten
        """
        cursor.execute(sql_query, (ma_mon_hoc, hoc_ky, nam_hoc, ma_lop))
        results = cursor.fetchall()
        print("[BACK-END LOGIC] Lấy danh sách HS và điểm thành công.")
        
        return results
    except Error as e:
        print(f"Lỗi khi lấy HS và điểm: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if connection and connection.is_connected(): connection.close()

def luu_diem_cho_hoc_sinh(ma_hs, ma_mh, hoc_ky, nam_hoc, d1, d2, d3, d4, d5):
    """
    Lưu điểm (hoặc cập nhật nếu đã tồn tại).
    Đây là lệnh UPSERT (UPDATE + INSERT).
    """
    connection = tao_ket_noi()
    if connection is None: return False
    cursor = None
    
    # Chuyển đổi điểm rỗng ("") thành None (NULL) cho CSDL
    diem_data = (
        d1 if d1 else None,
        d2 if d2 else None,
        d3 if d3 else None,
        d4 if d4 else None,
        d5 if d5 else None,
    )
    
    try:
        cursor = connection.cursor()
        # Cú pháp đặc biệt của MySQL: INSERT ... ON DUPLICATE KEY UPDATE
        # Nó yêu cầu 1 RÀNG BUỘC UNIQUE (mà ta đã tạo)
        sql_query = """
            INSERT INTO DiemSo 
                (ma_hoc_sinh, ma_mon_hoc, hoc_ky, nam_hoc, 
                 diem_15phut_1, diem_15phut_2, diem_1tiet_1, diem_1tiet_2, diem_cuoi_ky)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                diem_15phut_1 = VALUES(diem_15phut_1),
                diem_15phut_2 = VALUES(diem_15phut_2),
                diem_1tiet_1 = VALUES(diem_1tiet_1),
                diem_1tiet_2 = VALUES(diem_1tiet_2),
                diem_cuoi_ky = VALUES(diem_cuoi_ky)
        """
        data_tuple = (ma_hs, ma_mh, hoc_ky, nam_hoc) + diem_data
        
        cursor.execute(sql_query, data_tuple)
        connection.commit()
        # In ra 1 phần để debug
        print(f"[BACK-END LOGIC] Lưu điểm cho {ma_hs} - {ma_mh} thành công.")
        return True
        
    except Error as e:
        print(f"Lỗi khi lưu điểm cho {ma_hs}: {e}")
        connection.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if connection and connection.is_connected(): connection.close()
        
        
        
        
        