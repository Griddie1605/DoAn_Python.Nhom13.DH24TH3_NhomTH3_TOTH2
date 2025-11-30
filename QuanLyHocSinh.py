# 1. Imports
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import datetime

# ====== Kết nối MySQL ======
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Grid0378095005", 
            database="QuanLyHocSinh" 
        )
    except Error as e:
        messagebox.showerror("Lỗi CSDL", f"Không thể kết nối đến MySQL: {e}")
        return None

# ====== Các hàm chức năng  ======


def tim_kiem_hs(tu_khoa):
    #Có thể tìm kiếm bằng tên hoặc mã học sinh
    print(f" Đang tìm kiếm với từ khóa: {tu_khoa}")
    conn = connect_db()
    if conn is None: return []
    cur = conn.cursor()
    try:
        search_term = f"%{tu_khoa}%"
        sql_query = """
            SELECT hs.ma_hs, hs.ho_ten, hs.gioi_tinh, hs.ngay_sinh, lop.ten_lop, hs.ma_lop 
            FROM HocSinh hs
            LEFT JOIN LopHoc lop ON hs.ma_lop = lop.ma_lop
            WHERE hs.ho_ten LIKE %s OR hs.ma_hs LIKE %s
            ORDER BY hs.ma_hs
        """
        cur.execute(sql_query, (search_term, search_term))
        results = cur.fetchall()
        return results
    except Error as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {e}")
        return []
    finally:
        conn.close()

lop_map = {} 

def load_lop_hoc_combobox():
    """Tải dữ liệu 2 cột (ma_lop, ten_lop) vào ComboBox"""
    print("Đang tải danh sách lớp...")
    global lop_map
    lop_map.clear()
    conn = connect_db()
    if conn is None: return
    cur = conn.cursor()
    try:
        cur.execute("SELECT ma_lop, ten_lop FROM LopHoc")
        lop_display_list = []
        for (ma_lop, ten_lop) in cur.fetchall():
            display_name = f"{ten_lop} ({ma_lop})"
            lop_display_list.append(display_name)
            lop_map[display_name] = ma_lop
        cbb_lop['values'] = lop_display_list
    except Error as e:
        messagebox.showerror("Lỗi", f"Không thể tải danh sách lớp: {e}")
    finally:
        conn.close()

def get_display_name_from_ma_lop(ma_lop_can_tim):
    """Tiện ích: Tìm tên hiển thị từ ma_lop"""
    for display_name, ma_lop in lop_map.items():
        if ma_lop == ma_lop_can_tim:
            return display_name
    return ""

def clear_input():
    entry_ma_hs.config(state='normal')
    entry_ma_hs.delete(0, tk.END)
    entry_ho_ten.delete(0, tk.END)
    gender_var.set("Nam")
    date_entry.entry.delete(0, tk.END)
    cbb_lop.set("")
    if tree.focus():
        tree.selection_remove(tree.focus())

def _update_treeview(data_list):
    for i in tree.get_children():
        tree.delete(i)
    for row in data_list:
        display_values = list(row[:5])
        if row[3]: 
            display_values[3] = row[3].strftime('%d/%m/%Y')
        tree.insert("", tk.END, values=display_values, tags=(row[5],))

def load_data():
    print(" Đang tải dữ liệu học sinh...")
    conn = connect_db()
    if conn is None: return
    cur = conn.cursor()
    try:
        sql_query = """
            SELECT hs.ma_hs, hs.ho_ten, hs.gioi_tinh, hs.ngay_sinh, lop.ten_lop, hs.ma_lop 
            FROM HocSinh hs
            LEFT JOIN LopHoc lop ON hs.ma_lop = lop.ma_lop
            ORDER BY hs.ma_hs
        """
        cur.execute(sql_query)
        _update_treeview(cur.fetchall()) # Gọi hàm nạp dữ liệu
        entry_tim_kiem.delete(0, tk.END)
    except Error as e:
        messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")
    finally:
        conn.close()
        print("Tải dữ liệu thành công")

# Hàm thêm học sinh
def them_hs():
    ma_hs = entry_ma_hs.get()
    ho_ten = entry_ho_ten.get()
    gioi_tinh = gender_var.get()
    ngay_sinh_str = date_entry.entry.get()
    
    lop_display_name = cbb_lop.get()
    ma_lop_chon = lop_map.get(lop_display_name, None)
    
    if not ma_hs or not ho_ten or not ma_lop_chon:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ Mã HS, Họ tên và Lớp.")
        return
        
    try:
        ngay_sinh_obj = datetime.datetime.strptime(ngay_sinh_str, "%d/%m/%Y")
        ngay_sinh_sql = ngay_sinh_obj.strftime('%Y-%m-%d')
    except ValueError:
        messagebox.showwarning("Sai định dạng", "Ngày sinh phải đúng định dạng dd/mm/yyyy.")
        return
        
    conn = connect_db()
    if conn is None: return
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO HocSinh (ma_hs, ho_ten, gioi_tinh, ngay_sinh, ma_lop) VALUES (%s, %s, %s, %s, %s)",
                    (ma_hs, ho_ten, gioi_tinh, ngay_sinh_sql, ma_lop_chon))
        conn.commit()
        messagebox.showinfo("Thành công", "Thêm học sinh thành công!")
        load_data()
        clear_input()
    except Error as e:
        conn.rollback()
        messagebox.showerror("Lỗi", f"Không thể thêm: {e}")
    finally:
        conn.close()

# Hàm sửa dữ liệu học sinh
def sua_hs():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một học sinh trên bảng để sửa.")
        return
        
    values = tree.item(selected)["values"]
    tags = tree.item(selected)["tags"]
    
    clear_input()
    
    entry_ma_hs.insert(0, values[0])
    entry_ma_hs.config(state='disabled')
    entry_ho_ten.insert(0, values[1])
    gender_var.set(values[2])
    
    date_entry.entry.delete(0, tk.END)
    date_entry.entry.insert(0, values[3])
    
    ma_lop_cua_hs = tags[0] if tags else None
    cbb_lop.set(get_display_name_from_ma_lop(ma_lop_cua_hs))

# Hàm lưu học sinh
def luu_hs():
    ma_hs = entry_ma_hs.get()
    ho_ten = entry_ho_ten.get()
    gioi_tinh = gender_var.get()
    ngay_sinh_str = date_entry.entry.get()
    lop_display_name = cbb_lop.get()
    ma_lop_chon = lop_map.get(lop_display_name, None)

    if not ma_hs:
        messagebox.showwarning("Chưa chọn", "Vui lòng nhấn nút 'Sửa' và chọn học sinh trước khi Lưu.")
        return
    if not ma_lop_chon:
        messagebox.showwarning("Thiếu Lớp", "Vui lòng chọn Lớp.")
        return

    try:
        ngay_sinh_obj = datetime.datetime.strptime(ngay_sinh_str, "%d/%m/%Y")
        ngay_sinh_sql = ngay_sinh_obj.strftime('%Y-%m-%d')
    except ValueError:
        messagebox.showwarning("Sai định dạng", "Ngày sinh phải đúng định dạng dd/mm/yyyy.")
        return

    conn = connect_db()
    if conn is None: return
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE HocSinh 
            SET ho_ten=%s, gioi_tinh=%s, ngay_sinh=%s, ma_lop=%s
            WHERE ma_hs=%s
        """, (ho_ten, gioi_tinh, ngay_sinh_sql, ma_lop_chon, ma_hs))
        
        conn.commit()
        messagebox.showinfo("Thành công", "Cập nhật học sinh thành công!")
        load_data()
        clear_input()
    except Error as e:
        conn.rollback()
        messagebox.showerror("Lỗi", f"Không thể cập nhật: {e}")
    finally:
        conn.close()

# Hàm xóa học sinh
def xoa_hs():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn học sinh để xóa")
        return
        
    ma_hs = tree.item(selected)["values"][0]
    
    if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa học sinh mã {ma_hs}?"):
        return

    conn = connect_db()
    if conn is None: return
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM HocSinh WHERE ma_hs=%s", (ma_hs,))
        conn.commit()
        messagebox.showinfo("Thành công", "Xóa học sinh thành công!")
        load_data()
        clear_input()
    except Error as e:
        conn.rollback()
        if e.errno == 1451:
             messagebox.showerror("Lỗi", f"Không thể xóa học sinh {ma_hs} vì đã có điểm số liên quan.")
        else:
            messagebox.showerror("Lỗi", f"Không thể xóa: {e}")
    finally:
        conn.close()

# Hàm tìm kiếm học sinh
def tim_kiem_hs():
    tu_khoa = entry_tim_kiem.get()
    if not tu_khoa:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Mã hoặc Tên học sinh để tìm.")
        return
    
    results = tim_kiem_hs(tu_khoa)
    if not results:
        messagebox.showinfo("Thông báo", f"Không tìm thấy học sinh nào với từ khóa: {tu_khoa}")
    
    _update_treeview(results)
    clear_input()

# --- HÀM MỞ FORM QUẢN LÝ ĐIỂM SỐ ---
def mo_form_diem_so_ui():
    """
    Mở cửa sổ Toplevel để quản lý điểm của học sinh
    """
    print("Nút Quản lý Điểm")
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một học sinh trên bảng để xem điểm.")
        return
        
    ma_hs = tree.item(selected)["values"][0]
    ho_ten = tree.item(selected)["values"][1]
    
    # --- Tạo cửa sổ mới (Toplevel) ---
    diem_window = tk.Toplevel(root)
    diem_window.title(f"Quản lý Điểm - {ho_ten} ({ma_hs})")
    diem_window.geometry("800x500")
    diem_window.transient(root) # Luôn ở trên cửa sổ chính
    diem_window.grab_set() # Khóa tương tác với cửa sổ chính
    
    # --- (MỚI) Các hàm nội bộ của Form Điểm ---
    
    def load_diem_treeview():
        """Nạp điểm của HS này vào Bảng điểm"""
        for i in tree_diem.get_children():
            tree_diem.delete(i)
        
        data = lay_diem_cua_hoc_sinh(ma_hs) # Gọi Back-end
        for row in data:
            tree_diem.insert("", tk.END, values=row)

    def them_diem_moi_ui():
        """Thêm một dòng điểm mới cho học sinh này"""
        mon_hoc = entry_mon.get()
        hoc_ky = cbb_hoc_ky.get()
        nam_hoc = entry_nam_hoc.get()
        d15p = entry_d15p.get()
        d1t = entry_d1t.get()
        dck = entry_dck.get()
        ghi_chu = entry_ghi_chu.get()
        
        if not (mon_hoc and hoc_ky and nam_hoc):
            messagebox.showwarning("Thiếu thông tin", "Môn, Học kỳ, Năm học là bắt buộc.", parent=diem_window)
            return
            
        if them_diem_moi(ma_hs, mon_hoc, hoc_ky, nam_hoc, d15p, d1t, dck, ghi_chu):
            messagebox.showinfo("Thành công", "Thêm điểm thành công.", parent=diem_window)
            load_diem_treeview() # Tải lại bảng điểm
            # Xóa các ô entry
            entry_mon.delete(0, tk.END)
            entry_d15p.delete(0, tk.END)
            entry_d1t.delete(0, tk.END)
            entry_dck.delete(0, tk.END)
            entry_ghi_chu.delete(0, tk.END)
        else:
            messagebox.showerror("Lỗi", "Thêm điểm thất bại.", parent=diem_window)
            
    def xoa_diem_da_chon_ui():
        """Xóa dòng điểm được chọn trên Bảng điểm"""
        selected_diem = tree_diem.focus()
        if not selected_diem:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn dòng điểm để xóa.", parent=diem_window)
            return
            
        # Cột đầu tiên (values[0]) chính là id_diem
        id_diem = tree_diem.item(selected_diem)["values"][0]
        
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa dòng điểm (ID: {id_diem}) này không?", parent=diem_window):
            if xoa_diem(id_diem):
                messagebox.showinfo("Thành công", "Xóa điểm thành công.", parent=diem_window)
                load_diem_treeview() # Tải lại bảng
            else:
                 messagebox.showerror("Lỗi", "Xóa điểm thất bại.", parent=diem_window)

    # --- (MỚI) Thiết kế giao diện Form Điểm ---
    
    # Frame Nhập liệu (Giống Form chính)
    form_diem_frame = ttk.Labelframe(diem_window, text="Thêm điểm mới", padding=10)
    form_diem_frame.pack(padx=10, pady=10, fill="x")
    
    ttk.Label(form_diem_frame, text="Môn học:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_mon = ttk.Entry(form_diem_frame)
    entry_mon.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_diem_frame, text="Học kỳ:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    cbb_hoc_ky = ttk.Combobox(form_diem_frame, values=["1", "2"], state="readonly", width=5)
    cbb_hoc_ky.grid(row=0, column=3, padx=5, pady=5, sticky="w")
    cbb_hoc_ky.current(0)
    
    ttk.Label(form_diem_frame, text="Năm học:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
    entry_nam_hoc = ttk.Entry(form_diem_frame, width=10)
    entry_nam_hoc.grid(row=0, column=5, padx=5, pady=5, sticky="w")
    entry_nam_hoc.insert(0, "2024-2025") # Gợi ý
    
    ttk.Label(form_diem_frame, text="Điểm 15p:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_d15p = ttk.Entry(form_diem_frame, width=7)
    entry_d15p.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    ttk.Label(form_diem_frame, text="Điểm 1 tiết:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_d1t = ttk.Entry(form_diem_frame, width=7)
    entry_d1t.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    
    ttk.Label(form_diem_frame, text="Điểm Cuối kỳ:").grid(row=1, column=4, padx=5, pady=5, sticky="w")
    entry_dck = ttk.Entry(form_diem_frame, width=7)
    entry_dck.grid(row=1, column=5, padx=5, pady=5, sticky="w")
    
    ttk.Label(form_diem_frame, text="Ghi chú:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_ghi_chu = ttk.Entry(form_diem_frame)
    entry_ghi_chu.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
    
    btn_them_diem = ttk.Button(form_diem_frame, text="Thêm Điểm", command=them_diem_moi_ui, bootstyle="success")
    btn_them_diem.grid(row=2, column=4, columnspan=2, padx=5, pady=5, sticky="e")
    
    form_diem_frame.columnconfigure(1, weight=1)
    
    # Frame Bảng điểm
    tree_diem_frame = ttk.Labelframe(diem_window, text=f"Bảng điểm của {ho_ten}", padding=10)
    tree_diem_frame.pack(padx=10, pady=5, fill="both", expand=True)
    
    diem_cols = ("id", "mon_hoc", "hoc_ky", "nam_hoc", "d15p", "d1t", "dck", "ghi_chu")
    tree_diem = ttk.Treeview(tree_diem_frame, columns=diem_cols, show="headings", height=5)
    
    tree_diem.heading("id", text="ID")
    tree_diem.heading("mon_hoc", text="Môn học")
    tree_diem.heading("hoc_ky", text="Học kỳ")
    tree_diem.heading("nam_hoc", text="Năm học")
    tree_diem.heading("d15p", text="15p")
    tree_diem.heading("d1t", text="1 Tiết")
    tree_diem.heading("dck", text="Cuối kỳ")
    tree_diem.heading("ghi_chu", text="Ghi chú")
    
    tree_diem.column("id", width=40, anchor="center")
    tree_diem.column("mon_hoc", width=100)
    tree_diem.column("hoc_ky", width=50, anchor="center")
    tree_diem.column("nam_hoc", width=80, anchor="center")
    tree_diem.column("d15p", width=50, anchor="center")
    tree_diem.column("d1t", width=50, anchor="center")
    tree_diem.column("dck", width=50, anchor="center")
    tree_diem.column("ghi_chu", width=150)
    
    diem_scrollbar = ttk.Scrollbar(tree_diem_frame, orient=tk.VERTICAL, command=tree_diem.yview)
    tree_diem.configure(yscroll=diem_scrollbar.set)
    diem_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree_diem.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Nút Xóa và Đóng
    btn_frame_diem = ttk.Frame(diem_window)
    btn_frame_diem.pack(padx=10, pady=10, fill="x")
    
    btn_xoa_diem = ttk.Button(btn_frame_diem, text="Xóa Dòng Điểm Đã Chọn", command=xoa_diem_da_chon_ui, bootstyle="danger-outline")
    btn_xoa_diem.pack(side=tk.LEFT)
    
    btn_dong_diem = ttk.Button(btn_frame_diem, text="Đóng", command=diem_window.destroy, bootstyle="secondary")
    btn_dong_diem.pack(side=tk.RIGHT)
    
    # Tải dữ liệu ban đầu cho Form Điểm
    load_diem_treeview()
    
# ====== Quản lý điểm số ======
#Hàm lấy điểm của học sinh
def lay_diem_cua_hoc_sinh(ma_hs):
    conn = connect_db()
    if conn is None: return []
    cur = conn.cursor()
    try:
        # Lấy các cột tương ứng với bảng DiemSo
        sql_query = """
            SELECT id_diem, mon_hoc, hoc_ky, nam_hoc, diem_15p, diem_1tiet, diem_cuoi_ky, ghi_chu 
            FROM DiemSo 
            WHERE ma_hs = %s
            ORDER BY nam_hoc, hoc_ky, mon_hoc
        """
        cur.execute(sql_query, (ma_hs,))
        results = cur.fetchall()
        return results
    except Error as e:
        messagebox.showerror("Lỗi", f"Không thể tải điểm của học sinh: {e}")
        return []
    finally:
        conn.close()

# Hàm thêm điểm mới cho học sinh
def them_diem_moi(ma_hs, mon_hoc, hoc_ky, nam_hoc, d15p, d1t, dck, ghi_chu):
    conn = connect_db()
    if conn is None: return False
    cur = conn.cursor()
    try:
        # Chuyển đổi rỗng thành None
        d15p = d15p if d15p else None
        d1t = d1t if d1t else None
        dck = dck if dck else None
        
        sql_query = """
            INSERT INTO DiemSo (ma_hs, mon_hoc, hoc_ky, nam_hoc, diem_15p, diem_1tiet, diem_cuoi_ky, ghi_chu)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql_query, (ma_hs, mon_hoc, hoc_ky, nam_hoc, d15p, d1t, dck, ghi_chu))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        messagebox.showerror("Lỗi", f"Không thể thêm điểm: {e}")
        return False
    finally:
        conn.close()

# Hàm xóa điểm dựa trên id_diem
def xoa_diem(id_diem):
    conn = connect_db()
    if conn is None: return False
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM DiemSo WHERE id_diem = %s", (id_diem,))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        messagebox.showerror("Lỗi", f"Không thể xóa điểm: {e}")
        return False
    finally:
        conn.close()

# ====== 4. Cửa sổ chính ======
root = ttk.Window(themename="litera") 
root.title("Quản lý Học sinh")
root.geometry("1000x550") 
root.resizable(False, False)

root.columnconfigure(0, weight=6) 
root.columnconfigure(1, weight=4)
root.rowconfigure(0, weight=1)

# ====== Frame bên trái ======
left_frame = ttk.Frame(root)
#Dùng grid để đặt frame
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

left_frame.rowconfigure(1, weight=1) # Hàng 1 (bảng) co giãn
left_frame.columnconfigure(0, weight=1) # Cột 0 (bảng) co giãn

# --- Frame Tìm kiếm ---
frame_search = ttk.Labelframe(left_frame, text="Tìm kiếm", padding=10)
frame_search.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

entry_tim_kiem = ttk.Entry(frame_search, width=30)
entry_tim_kiem.pack(side=tk.LEFT, padx=5, fill="x", expand=True)

btn_tim = ttk.Button(frame_search, text="Tìm", command=tim_kiem_hs, bootstyle="info")
btn_tim.pack(side=tk.LEFT, padx=5)
btn_tai_lai = ttk.Button(frame_search, text="Tải lại DS", command=load_data, bootstyle="secondary-outline")
btn_tai_lai.pack(side=tk.LEFT, padx=5)

# ---Bảng danh sách---
tree_frame = ttk.Frame(left_frame)
tree_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

style = ttk.Style()
style.configure("Treeview", rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

columns = ("ma_hs", "ho_ten", "gioi_tinh", "ngay_sinh", "lop")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10, bootstyle="primary")

# tree.heading và tree.column ...
tree.heading("ma_hs", text="Mã HS")
tree.heading("ho_ten", text="Họ Tên")
tree.heading("gioi_tinh", text="Giới tính")
tree.heading("ngay_sinh", text="Ngày sinh")
tree.heading("lop", text="Tên Lớp")
tree.column("ma_hs", width=80, anchor="center")
tree.column("ho_ten", width=150)
tree.column("gioi_tinh", width=70, anchor="center")
tree.column("ngay_sinh", width=100, anchor="center")
tree.column("lop", width=120, anchor="center")

scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview, bootstyle="primary-round")
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# ====== Frame bên phải(button) ======
right_frame = ttk.Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# --- Tiêu đề  ---
lbl_title = ttk.Label(right_frame, text="QUẢN LÝ HỌC SINH", 
                      font=("Arial", 18, "bold"), bootstyle="primary")
lbl_title.pack(pady=10)

# ---  Frame nhập thông tin ---
frame_info = ttk.Labelframe(right_frame, text="Thông tin chi tiết", padding=15)
frame_info.pack(pady=5, padx=10, fill="x")

# Sắp xếp dạng grid trong frame_info
frame_info.columnconfigure(1, weight=1) # Chỉ 1 cột co giãn

# Hàng 0
ttk.Label(frame_info, text="Mã HS:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_ma_hs = ttk.Entry(frame_info, width=25)
entry_ma_hs.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Hàng 1
ttk.Label(frame_info, text="Họ tên:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_ho_ten = ttk.Entry(frame_info, width=25)
entry_ho_ten.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Hàng 2
ttk.Label(frame_info, text="Lớp:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
cbb_lop = ttk.Combobox(frame_info, state="readonly", width=30)
cbb_lop.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Hàng 3
ttk.Label(frame_info, text="Ngày sinh:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
date_entry = ttk.DateEntry(frame_info, width=30, dateformat="%d/%m/%Y") 
date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
date_entry.entry.delete(0, tk.END)

# Hàng 4
ttk.Label(frame_info, text="Phái:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
gender_frame = ttk.Frame(frame_info)
gender_frame.grid(row=4, column=1, padx=5, pady=5, sticky="w")
gender_var = tk.StringVar(value="Nam")
ttk.Radiobutton(gender_frame, text="Nam", variable=gender_var, value="Nam", bootstyle="primary").pack(side=tk.LEFT)
ttk.Radiobutton(gender_frame, text="Nữ", variable=gender_var, value="Nữ", bootstyle="primary").pack(side=tk.LEFT, padx=10)

# --- Frame các Button ---
frame_btn = ttk.Frame(right_frame)
frame_btn.pack(pady=20) 

ttk.Button(frame_btn, text="Thêm", width=8, command=them_hs, bootstyle="success").grid(row=0, column=0, padx=5)
ttk.Button(frame_btn, text="Lưu", width=8, command=luu_hs, bootstyle="primary").grid(row=0, column=1, padx=5)
ttk.Button(frame_btn, text="Sửa", width=8, command=sua_hs, bootstyle="info").grid(row=0, column=2, padx=5)
ttk.Button(frame_btn, text="Hủy", width=8, command=clear_input, bootstyle="secondary").grid(row=0, column=3, padx=5)
ttk.Button(frame_btn, text="Xóa", width=8, command=xoa_hs, bootstyle="danger").grid(row=0, column=4, padx=5)

# ---  NÚT QUẢN LÝ ĐIỂM ---
frame_diem_btn = ttk.Frame(right_frame)
frame_diem_btn.pack(pady=10, fill="x")
ttk.Button(frame_diem_btn, text="Quản lý Điểm (Cho HS đã chọn)", 
           command=mo_form_diem_so_ui, bootstyle="success-outline").pack(fill="x", padx=10)
# Button Thoát 
frame_thoat = ttk.Frame(right_frame)
frame_thoat.pack(pady=10, fill="x")
ttk.Button(frame_thoat, text="Thoát", command=root.quit, bootstyle="light-outline").pack(side=tk.RIGHT, padx=10)

# ====== Chạy ứng dụng ======
load_lop_hoc_combobox() 
load_data() 
root.mainloop()