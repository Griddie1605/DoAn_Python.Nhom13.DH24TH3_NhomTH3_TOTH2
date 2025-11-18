import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry # Dùng để chọn ngày

# Import các hàm logic 
from Logic.database_logic import (
    lay_danh_sach_lop, 
    lay_tat_ca_hoc_sinh, 
    them_hoc_sinh,
    sua_hoc_sinh,
    xoa_hoc_sinh
)

# Biến toàn cục để lưu trữ các ô entry 
entry_ma_hs = None
entry_ho_ten = None
cal_ngay_sinh = None
combo_gioi_tinh = None
entry_dia_chi = None
entry_email = None
entry_sdt = None
combo_lop = None
tree_hoc_sinh = None # Bảng (Treeview) hiển thị

# --- CÁC HÀM XỬ LÝ SỰ KIỆN  ---

def cap_nhat_danh_sach_hoc_sinh():
    """Tải dữ liệu từ CSDL và hiển thị lên Treeview"""
    print("[UI] Đang cập nhật danh sách học sinh...")
    # Xóa tất cả dữ liệu cũ trên Treeview
    for row in tree_hoc_sinh.get_children():
        tree_hoc_sinh.delete(row)
    
    # Gọi Back-end để lấy dữ liệu mới
    danh_sach = lay_tat_ca_hoc_sinh()
    
    # Chèn dữ liệu mới vào Treeview
    for hs in danh_sach:
        # Đảm bảo định dạng ngày tháng đẹp (nếu cần)
        # hs[2] là ngay_sinh
        ngay_sinh_formatted = hs[2].strftime('%d/%m/%Y') if hs[2] else ""
        
        # Tạo một list có thể chỉnh sửa từ tuple
        hs_data = list(hs)
        hs_data[2] = ngay_sinh_formatted # Thay thế ngày sinh
        
        tree_hoc_sinh.insert("", tk.END, values=hs_data)

def nap_danh_sach_lop():
    """Lấy danh sách lớp từ CSDL và nạp vào ComboBox"""
    try:
        danh_sach = lay_danh_sach_lop()
        combo_lop['values'] = danh_sach
        if danh_sach:
            combo_lop.current(0) # Chọn phần tử đầu tiên
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải danh sách lớp: {e}")

def them_hoc_sinh_ui():
    print("[UI] Nút 'Thêm' được nhấn")
    # 1. Lấy dữ liệu từ các ô entry
    ma_hs = entry_ma_hs.get()
    ho_ten = entry_ho_ten.get()
    ngay_sinh = cal_ngay_sinh.get_date().strftime('%Y-%m-%d') # Format YYYY-MM-DD cho MySQL
    gioi_tinh = combo_gioi_tinh.get()
    dia_chi = entry_dia_chi.get()
    email = entry_email.get()
    sdt = entry_sdt.get()
    ma_lop = combo_lop.get()
    
    # 2. Kiểm tra dữ liệu (ví dụ đơn giản)
    if not ma_hs or not ho_ten:
        messagebox.showwarning("Thiếu thông tin", "Mã học sinh và Họ tên là bắt buộc.")
        return
        
    # 3. Gọi Back-end để thêm
    success = them_hoc_sinh(ma_hs, ho_ten, ngay_sinh, gioi_tinh, dia_chi, email, sdt, ma_lop)
    
    # 4. Xử lý kết quả
    if success:
        messagebox.showinfo("Thành công", "Đã thêm học sinh thành công!")
        cap_nhat_danh_sach_hoc_sinh() # Tải lại danh sách
        lam_moi_form() # Xóa trắng các ô
    else:
        messagebox.showerror("Lỗi", "Thêm học sinh thất bại (Mã HS có thể đã tồn tại?)")

def sua_hoc_sinh_ui():
    print("[UI] Nút 'Sửa' được nhấn")
    
    # 1. Lấy dữ liệu từ form
    ma_hs = entry_ma_hs.get()
    ho_ten = entry_ho_ten.get()
    ngay_sinh = cal_ngay_sinh.get_date().strftime('%Y-%m-%d')
    gioi_tinh = combo_gioi_tinh.get()
    dia_chi = entry_dia_chi.get()
    email = entry_email.get()
    sdt = entry_sdt.get()
    ma_lop = combo_lop.get()

    if not ma_hs:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một học sinh từ danh sách để sửa.")
        return

    # 2. Gọi Back-end
    success = sua_hoc_sinh(ma_hs, ho_ten, ngay_sinh, gioi_tinh, dia_chi, email, sdt, ma_lop)
    
    # 3. Xử lý kết quả
    if success:
        messagebox.showinfo("Thành công", "Cập nhật thông tin học sinh thành công!")
        cap_nhat_danh_sach_hoc_sinh()
        lam_moi_form()
    else:
        messagebox.showerror("Lỗi", "Cập nhật thất bại.")

def xoa_hoc_sinh_ui():
    print("[UI] Nút 'Xóa' được nhấn")
    
    ma_hs = entry_ma_hs.get()
    if not ma_hs:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một học sinh để xóa.")
        return

    # 2. Xác nhận
    if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa học sinh mã {ma_hs} không?"):
        # 3. Gọi Back-end
        success = xoa_hoc_sinh(ma_hs)
        
        # 4. Xử lý kết quả
        if success:
            messagebox.showinfo("Thành công", "Đã xóa học sinh.")
            cap_nhat_danh_sach_hoc_sinh()
            lam_moi_form()
        else:
            messagebox.showerror("Lỗi", "Xóa thất bại (Học sinh có thể đã có điểm).")

def lam_moi_form():
    """Xóa trắng các ô nhập liệu và bỏ chọn trên Treeview"""
    print("[UI] Làm mới form")
    entry_ma_hs.config(state='normal')
    entry_ma_hs.delete(0, tk.END)
    entry_ho_ten.delete(0, tk.END)
    cal_ngay_sinh.set_date(None) # Xóa ngày
    combo_gioi_tinh.set("")
    entry_dia_chi.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_sdt.delete(0, tk.END)
    combo_lop.set("")


def on_tree_select(event):
    """Sự kiện khi nhấn vào một hàng trên Treeview -> Điền dữ liệu lên form"""
    # Lấy item được chọn
    selected_item = tree_hoc_sinh.focus()
    if not selected_item:
        return
        
    # Lấy dữ liệu của item đó (dữ liệu này là từ lúc ta nạp vào)
    values = tree_hoc_sinh.item(selected_item, 'values')
    if not values:
        return

    # Xóa form cũ trước
    lam_moi_form()
    
    # Điền dữ liệu lên các ô entry
    entry_ma_hs.insert(0, values[0])
    entry_ma_hs.config(state='disabled') # Khóa ô Mã HS khi Sửa/Xóa
    entry_ho_ten.insert(0, values[1])
    
    # Chuyển đổi ngày tháng từ dd/mm/YYYY về đối tượng Date
    cal_ngay_sinh.set_date(values[2]) 
    
    combo_gioi_tinh.set(values[3])
    entry_dia_chi.insert(0, values[4])
    entry_email.insert(0, values[5])
    entry_sdt.insert(0, values[6])
    combo_lop.set(values[7])


# --- HÀM CHÍNH TẠO GIAO DIỆN ---

def open_form_quan_ly_hoc_sinh(main_root):
    """
    Hàm này mở cửa sổ Toplevel (cửa sổ con)
    để quản lý học sinh.
    """
    
    # Khai báo sử dụng các biến toàn cục (để các hàm khác có thể truy cập)
    global entry_ma_hs, entry_ho_ten, cal_ngay_sinh, combo_gioi_tinh
    global entry_dia_chi, entry_email, entry_sdt, combo_lop, tree_hoc_sinh
    
    hs_window = tk.Toplevel(main_root)
    hs_window.title("Quản lý Thông tin Học sinh")
    hs_window.geometry("1000x600") # Tăng kích thước cửa sổ
    hs_window.transient(main_root)
    hs_window.grab_set()

    # --- Frame 1: Form nhập liệu ---
    form_frame = ttk.LabelFrame(hs_window, text="Thông tin học sinh", padding=10)
    form_frame.pack(padx=10, pady=10, fill="x", side=tk.TOP)
    
    # Cấu hình grid co giãn
    form_frame.columnconfigure(1, weight=1)
    form_frame.columnconfigure(3, weight=1)

    # Hàng 1: Mã HS, Họ tên
    ttk.Label(form_frame, text="Mã HS:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_ma_hs = ttk.Entry(form_frame)
    entry_ma_hs.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Họ tên:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_ho_ten = ttk.Entry(form_frame)
    entry_ho_ten.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    # Hàng 2: Ngày sinh, Giới tính
    ttk.Label(form_frame, text="Ngày sinh:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    cal_ngay_sinh = DateEntry(form_frame, width=12, background='darkblue', 
                             foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
    cal_ngay_sinh.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Giới tính:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    combo_gioi_tinh = ttk.Combobox(form_frame, values=["Nam", "Nữ", "Khác"], state="readonly")
    combo_gioi_tinh.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    # Hàng 3: Địa chỉ
    ttk.Label(form_frame, text="Địa chỉ:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_dia_chi = ttk.Entry(form_frame)
    entry_dia_chi.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

    # Hàng 4: Email, SĐT
    ttk.Label(form_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_email = ttk.Entry(form_frame)
    entry_email.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="SĐT:").grid(row=3, column=2, padx=5, pady=5, sticky="w")
    entry_sdt = ttk.Entry(form_frame)
    entry_sdt.grid(row=3, column=3, padx=5, pady=5, sticky="ew")

    # Hàng 5: Lớp
    ttk.Label(form_frame, text="Lớp:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    combo_lop = ttk.Combobox(form_frame, state="readonly")
    combo_lop.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
    # Tải danh sách lớp ngay khi mở form
    nap_danh_sach_lop()


    # --- Frame 2: Các nút chức năng ---
    button_frame = ttk.Frame(hs_window, padding=10)
    button_frame.pack(fill="x", side=tk.TOP)

    btn_them = ttk.Button(button_frame, text="Thêm", command=them_hoc_sinh_ui)
    btn_them.pack(side=tk.LEFT, padx=5)

    btn_sua = ttk.Button(button_frame, text="Sửa", command=sua_hoc_sinh_ui)
    btn_sua.pack(side=tk.LEFT, padx=5)

    btn_xoa = ttk.Button(button_frame, text="Xóa", command=xoa_hoc_sinh_ui)
    btn_xoa.pack(side=tk.LEFT, padx=5)

    btn_lam_moi = ttk.Button(button_frame, text="Làm mới", command=lam_moi_form)
    btn_lam_moi.pack(side=tk.LEFT, padx=5)

    # --- Frame 3: Bảng hiển thị (Treeview) ---
    tree_frame = ttk.Frame(hs_window, padding=10)
    tree_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    # Định nghĩa các cột
    columns = ("ma_hs", "ho_ten", "ngay_sinh", "gioi_tinh", "dia_chi", "email", "sdt", "ma_lop")
    tree_hoc_sinh = ttk.Treeview(tree_frame, columns=columns, show="headings")

    # Đặt tiêu đề cho các cột
    tree_hoc_sinh.heading("ma_hs", text="Mã HS")
    tree_hoc_sinh.heading("ho_ten", text="Họ Tên")
    tree_hoc_sinh.heading("ngay_sinh", text="Ngày Sinh")
    tree_hoc_sinh.heading("gioi_tinh", text="Giới Tính")
    tree_hoc_sinh.heading("dia_chi", text="Địa Chỉ")
    tree_hoc_sinh.heading("email", text="Email")
    tree_hoc_sinh.heading("sdt", text="SĐT")
    tree_hoc_sinh.heading("ma_lop", text="Mã Lớp")
    
    # Đặt độ rộng cho các cột
    tree_hoc_sinh.column("ma_hs", width=80, anchor=tk.CENTER)
    tree_hoc_sinh.column("ho_ten", width=150)
    tree_hoc_sinh.column("ngay_sinh", width=100, anchor=tk.CENTER)
    tree_hoc_sinh.column("gioi_tinh", width=60, anchor=tk.CENTER)
    tree_hoc_sinh.column("dia_chi", width=200)
    tree_hoc_sinh.column("email", width=150)
    tree_hoc_sinh.column("sdt", width=100)
    tree_hoc_sinh.column("ma_lop", width=80, anchor=tk.CENTER)

    # Thêm thanh cuộn
    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree_hoc_sinh.yview)
    tree_hoc_sinh.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree_hoc_sinh.pack(fill=tk.BOTH, expand=True)

    # Gán sự kiện: Khi nhấn vào một hàng
    tree_hoc_sinh.bind("<<TreeviewSelect>>", on_tree_select)

    # --- Tải dữ liệu ban đầu ---
    cap_nhat_danh_sach_hoc_sinh()

    # Đợi cho đến khi cửa sổ này đóng
    main_root.wait_window(hs_window)