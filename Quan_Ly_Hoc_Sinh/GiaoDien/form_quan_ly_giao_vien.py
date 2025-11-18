import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry 

# Import các hàm logic Back-end
from Logic.database_logic import (
    lay_tat_ca_giao_vien, 
    them_giao_vien,
    sua_giao_vien,
    xoa_giao_vien
)

# Biến toàn cục cho form này
entry_ma_gv = None
entry_ho_ten_gv = None
cal_ngay_sinh_gv = None
combo_gioi_tinh_gv = None
entry_email_gv = None
entry_sdt_gv = None
entry_chuyen_mon = None
tree_giao_vien = None 

# --- CÁC HÀM XỬ LÝ SỰ KIỆN ---

def cap_nhat_danh_sach_giao_vien():
    """Tải dữ liệu từ CSDL và hiển thị lên Treeview"""
    print("[UI] Đang cập nhật danh sách giáo viên...")
    for row in tree_giao_vien.get_children():
        tree_giao_vien.delete(row)
    
    danh_sach = lay_tat_ca_giao_vien()
    
    for gv in danh_sach:
        ngay_sinh_formatted = gv[2].strftime('%d/%m/%Y') if gv[2] else ""
        gv_data = list(gv)
        gv_data[2] = ngay_sinh_formatted
        
        tree_giao_vien.insert("", tk.END, values=gv_data)

def them_giao_vien_ui():
    print("[UI] Nút 'Thêm GV' được nhấn")
    ma_gv = entry_ma_gv.get()
    ho_ten = entry_ho_ten_gv.get()
    ngay_sinh = cal_ngay_sinh_gv.get_date().strftime('%Y-%m-%d')
    gioi_tinh = combo_gioi_tinh_gv.get()
    email = entry_email_gv.get()
    sdt = entry_sdt_gv.get()
    chuyen_mon = entry_chuyen_mon.get()
    
    if not ma_gv or not ho_ten:
        messagebox.showwarning("Thiếu thông tin", "Mã Giáo viên và Họ tên là bắt buộc.")
        return
        
    success = them_giao_vien(ma_gv, ho_ten, ngay_sinh, gioi_tinh, email, sdt, chuyen_mon)
    
    if success:
        messagebox.showinfo("Thành công", "Đã thêm giáo viên thành công!")
        cap_nhat_danh_sach_giao_vien() 
        lam_moi_form_gv()
    else:
        messagebox.showerror("Lỗi", "Thêm giáo viên thất bại (Mã GV có thể đã tồn tại?)")

def sua_giao_vien_ui():
    print("[UI] Nút 'Sửa GV' được nhấn")
    
    ma_gv = entry_ma_gv.get()
    ho_ten = entry_ho_ten_gv.get()
    ngay_sinh = cal_ngay_sinh_gv.get_date().strftime('%Y-%m-%d')
    gioi_tinh = combo_gioi_tinh_gv.get()
    email = entry_email_gv.get()
    sdt = entry_sdt_gv.get()
    chuyen_mon = entry_chuyen_mon.get()

    if not ma_gv:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một giáo viên để sửa.")
        return

    success = sua_giao_vien(ma_gv, ho_ten, ngay_sinh, gioi_tinh, email, sdt, chuyen_mon)
    
    if success:
        messagebox.showinfo("Thành công", "Cập nhật thông tin giáo viên thành công!")
        cap_nhat_danh_sach_giao_vien()
        lam_moi_form_gv()
    else:
        messagebox.showerror("Lỗi", "Cập nhật thất bại.")

def xoa_giao_vien_ui():
    print("[UI] Nút 'Xóa GV' được nhấn")
    
    ma_gv = entry_ma_gv.get()
    if not ma_gv:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một giáo viên để xóa.")
        return

    if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa giáo viên mã {ma_gv} không?"):
        success = xoa_giao_vien(ma_gv)
        
        if success:
            messagebox.showinfo("Thành công", "Đã xóa giáo viên.")
            cap_nhat_danh_sach_giao_vien()
            lam_moi_form_gv()
        else:
            messagebox.showerror("Lỗi", "Xóa thất bại (Giáo viên có thể đang chủ nhiệm hoặc được phân công dạy).")

def lam_moi_form_gv():
    """Xóa trắng các ô nhập liệu"""
    print("[UI] Làm mới form GV")
    entry_ma_gv.config(state='normal')
    entry_ma_gv.delete(0, tk.END)
    entry_ho_ten_gv.delete(0, tk.END)
    cal_ngay_sinh_gv.set_date(None) 
    combo_gioi_tinh_gv.set("")
    entry_email_gv.delete(0, tk.END)
    entry_sdt_gv.delete(0, tk.END)
    entry_chuyen_mon.delete(0, tk.END)   

def on_tree_select_gv(event):
    """Sự kiện khi nhấn vào một hàng trên Treeview -> Điền dữ liệu lên form"""
    selected_item = tree_giao_vien.focus()
    if not selected_item:
        return
        
    values = tree_giao_vien.item(selected_item, 'values')
    if not values:
        return

    lam_moi_form_gv()
    
    entry_ma_gv.insert(0, values[0])
    entry_ma_gv.config(state='disabled') 
    entry_ho_ten_gv.insert(0, values[1])
    cal_ngay_sinh_gv.set_date(values[2]) 
    combo_gioi_tinh_gv.set(values[3])
    entry_email_gv.insert(0, values[4])
    entry_sdt_gv.insert(0, values[5])
    entry_chuyen_mon.insert(0, values[6])


# --- HÀM CHÍNH TẠO GIAO DIỆN ---

def open_form_quan_ly_giao_vien(main_root):
    
    global entry_ma_gv, entry_ho_ten_gv, cal_ngay_sinh_gv, combo_gioi_tinh_gv
    global entry_email_gv, entry_sdt_gv, entry_chuyen_mon, tree_giao_vien
    
    gv_window = tk.Toplevel(main_root)
    gv_window.title("Quản lý Thông tin Giáo viên")
    gv_window.geometry("1000x550") 
    gv_window.transient(main_root)
    gv_window.grab_set()

    # --- Frame 1: Form nhập liệu ---
    form_frame = ttk.LabelFrame(gv_window, text="Thông tin giáo viên", padding=10)
    form_frame.pack(padx=10, pady=10, fill="x", side=tk.TOP)
    
    form_frame.columnconfigure(1, weight=1)
    form_frame.columnconfigure(3, weight=1)

    # Hàng 1: Mã GV, Họ tên
    ttk.Label(form_frame, text="Mã GV:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_ma_gv = ttk.Entry(form_frame)
    entry_ma_gv.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Họ tên:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_ho_ten_gv = ttk.Entry(form_frame)
    entry_ho_ten_gv.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    # Hàng 2: Ngày sinh, Giới tính
    ttk.Label(form_frame, text="Ngày sinh:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    cal_ngay_sinh_gv = DateEntry(form_frame, width=12, background='darkblue', 
                                 foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
    cal_ngay_sinh_gv.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Giới tính:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    combo_gioi_tinh_gv = ttk.Combobox(form_frame, values=["Nam", "Nữ", "Khác"], state="readonly")
    combo_gioi_tinh_gv.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    # Hàng 3: Email, SĐT
    ttk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_email_gv = ttk.Entry(form_frame)
    entry_email_gv.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="SĐT:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_sdt_gv = ttk.Entry(form_frame)
    entry_sdt_gv.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

    # Hàng 4: Chuyên môn
    ttk.Label(form_frame, text="Chuyên môn:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_chuyen_mon = ttk.Entry(form_frame)
    entry_chuyen_mon.grid(row=3, column=1, padx=5, pady=5, sticky="ew")


    # --- Frame 2: Các nút chức năng ---
    button_frame = ttk.Frame(gv_window, padding=10)
    button_frame.pack(fill="x", side=tk.TOP)

    btn_them = ttk.Button(button_frame, text="Thêm", command=them_giao_vien_ui)
    btn_them.pack(side=tk.LEFT, padx=5)

    btn_sua = ttk.Button(button_frame, text="Sửa", command=sua_giao_vien_ui)
    btn_sua.pack(side=tk.LEFT, padx=5)

    btn_xoa = ttk.Button(button_frame, text="Xóa", command=xoa_giao_vien_ui)
    btn_xoa.pack(side=tk.LEFT, padx=5)

    btn_lam_moi = ttk.Button(button_frame, text="Làm mới", command=lam_moi_form_gv)
    btn_lam_moi.pack(side=tk.LEFT, padx=5)

    # --- Frame 3: Bảng hiển thị (Treeview) ---
    tree_frame = ttk.Frame(gv_window, padding=10)
    tree_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    # Định nghĩa các cột
    columns = ("ma_gv", "ho_ten", "ngay_sinh", "gioi_tinh", "email", "sdt", "chuyen_mon")
    tree_giao_vien = ttk.Treeview(tree_frame, columns=columns, show="headings")

    tree_giao_vien.heading("ma_gv", text="Mã GV")
    tree_giao_vien.heading("ho_ten", text="Họ Tên")
    tree_giao_vien.heading("ngay_sinh", text="Ngày Sinh")
    tree_giao_vien.heading("gioi_tinh", text="Giới Tính")
    tree_giao_vien.heading("email", text="Email")
    tree_giao_vien.heading("sdt", text="SĐT")
    tree_giao_vien.heading("chuyen_mon", text="Chuyên môn")
    
    tree_giao_vien.column("ma_gv", width=80, anchor=tk.CENTER)
    tree_giao_vien.column("ho_ten", width=150)
    tree_giao_vien.column("ngay_sinh", width=100, anchor=tk.CENTER)
    tree_giao_vien.column("gioi_tinh", width=60, anchor=tk.CENTER)
    tree_giao_vien.column("email", width=150)
    tree_giao_vien.column("sdt", width=100)
    tree_giao_vien.column("chuyen_mon", width=100)

    # Thêm thanh cuộn
    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree_giao_vien.yview)
    tree_giao_vien.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree_giao_vien.pack(fill=tk.BOTH, expand=True)

    tree_giao_vien.bind("<<TreeviewSelect>>", on_tree_select_gv)

    # --- Tải dữ liệu ban đầu ---
    cap_nhat_danh_sach_giao_vien()

    main_root.wait_window(gv_window)