import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# Import các hàm logic Back-end
from Logic.database_logic import (
    tim_ma_giao_vien_tu_ten_dang_nhap,
    lay_lop_gv_day,
    lay_mon_gv_day_trong_lop,
    lay_tat_ca_lop_cho_combobox,
    lay_tat_ca_mon_hoc_cho_combobox,
    lay_hoc_sinh_va_diem,
    luu_diem_cho_hoc_sinh
)

# Biến toàn cục
combo_lop_diem = None
combo_mon_diem = None
combo_hoc_ky_diem = None
entry_nam_hoc_diem = None
tree_diem = None
entry_d1 = None
entry_d2 = None
entry_d3 = None
entry_d4 = None
entry_d5 = None
label_thong_tin_hs = None # Nhãn hiển thị HS đang chọn

# Biến map tra cứu
lop_map_diem = {}
mon_map_diem = {}

# Biến lưu trữ thông tin phân quyền
current_vai_tro = None
current_ma_gv = None # Mã GV nếu người đăng nhập là giáo viên

# --- CÁC HÀM XỬ LÝ SỰ KIỆN ---

def nap_combobox_lop(vai_tro, ma_gv):
    """Nạp ComboBox Lớp dựa trên vai trò"""
    global lop_map_diem
    lop_map_diem.clear()
    
    if vai_tro == 'admin':
        danh_sach_lop = lay_tat_ca_lop_cho_combobox() # Lấy tất cả các lớp
    else: # vai_tro == 'giao_vien'
        danh_sach_lop = lay_lop_gv_day(ma_gv) # Chỉ lấy lớp GV đó dạy
    
    lop_display_list = []
    for (ma_lop, ten_lop) in danh_sach_lop:
        display = f"{ten_lop} ({ma_lop})"
        lop_display_list.append(display)
        lop_map_diem[display] = ma_lop
    
    combo_lop_diem['values'] = lop_display_list
    if lop_display_list:
        combo_lop_diem.current(0)
    
    # Tự động kích hoạt nạp ComboBox Môn
    on_lop_selected(None)

def on_lop_selected(event):
    """Khi chọn Lớp, nạp ComboBox Môn"""
    global mon_map_diem
    mon_map_diem.clear()
    
    ma_lop = lop_map_diem.get(combo_lop_diem.get())
    if not ma_lop:
        combo_mon_diem['values'] = []
        return

    if current_vai_tro == 'admin':
        danh_sach_mon = lay_tat_ca_mon_hoc_cho_combobox() # Admin lấy tất cả môn
    else: # 'giao_vien'
        danh_sach_mon = lay_mon_gv_day_trong_lop(current_ma_gv, ma_lop) # GV chỉ lấy môn mình dạy lớp đó
        
    mon_display_list = []
    for (ma_mon, ten_mon) in danh_sach_mon:
        display = f"{ten_mon} ({ma_mon})"
        mon_display_list.append(display)
        mon_map_diem[display] = ma_mon
        
    combo_mon_diem['values'] = mon_display_list
    if mon_display_list:
        combo_mon_diem.current(0)

def xu_ly_tai_danh_sach_ui():
    """Nhấn nút 'Tải DS' -> Hiện danh sách HS và điểm"""
    # 1. Lấy thông tin
    ma_lop = lop_map_diem.get(combo_lop_diem.get())
    ma_mon = mon_map_diem.get(combo_mon_diem.get())
    hoc_ky = combo_hoc_ky_diem.get()
    nam_hoc = entry_nam_hoc_diem.get()
    
    if not (ma_lop and ma_mon and hoc_ky and nam_hoc):
        messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn đầy đủ Lớp, Môn, Học kỳ, Năm học.")
        return
        
    # 2. Xóa Treeview cũ
    for row in tree_diem.get_children():
        tree_diem.delete(row)
        
    # 3. Gọi Back-end
    danh_sach = lay_hoc_sinh_va_diem(ma_lop, ma_mon, hoc_ky, nam_hoc)
    
    # 4. Nạp dữ liệu
    for hs_diem in danh_sach:
        # hs_diem = (ma_hs, ho_ten, d1, d2, d3, d4, d5, id_diem)
        # Chỉ hiển thị 7 cột đầu
        tree_diem.insert("", tk.END, values=hs_diem[0:7])
    
    lam_moi_form_nhap_diem() # Xóa form nhập điểm

def on_tree_select_diem(event):
    """Khi nhấn vào 1 HS, điền điểm của họ vào Form Nhập điểm"""
    selected_item = tree_diem.focus()
    if not selected_item:
        return
        
    # values = (ma_hs, ho_ten, d1, d2, d3, d4, d5)
    values = tree_diem.item(selected_item, 'values')
    if not values:
        return

    lam_moi_form_nhap_diem()
    
    # Cập nhật nhãn
    label_thong_tin_hs.config(text=f"Nhập điểm cho: {values[1]} (Mã HS: {values[0]})")
    
    # Điền các điểm
    # (values[2] là d1, values[3] là d2,...)
    entry_d1.insert(0, values[2] if values[2] is not None else "")
    entry_d2.insert(0, values[3] if values[3] is not None else "")
    entry_d3.insert(0, values[4] if values[4] is not None else "")
    entry_d4.insert(0, values[5] if values[5] is not None else "")
    entry_d5.insert(0, values[6] if values[6] is not None else "")

def lam_moi_form_nhap_diem():
    """Chỉ xóa trắng các ô nhập điểm"""
    label_thong_tin_hs.config(text="Chọn một học sinh từ danh sách...")
    entry_d1.delete(0, tk.END)
    entry_d2.delete(0, tk.END)
    entry_d3.delete(0, tk.END)
    entry_d4.delete(0, tk.END)
    entry_d5.delete(0, tk.END)

def xu_ly_luu_diem_ui():
    """Lưu điểm cho HS đang được chọn"""
    # 1. Lấy thông tin HS đang chọn
    selected_item = tree_diem.focus()
    if not selected_item:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 học sinh để lưu điểm.")
        return
    
    ma_hs = tree_diem.item(selected_item, 'values')[0]
    
    # 2. Lấy thông tin chung
    ma_mon = mon_map_diem.get(combo_mon_diem.get())
    hoc_ky = combo_hoc_ky_diem.get()
    nam_hoc = entry_nam_hoc_diem.get()
    
    # 3. Lấy điểm từ Entry
    d1 = entry_d1.get()
    d2 = entry_d2.get()
    d3 = entry_d3.get()
    d4 = entry_d4.get()
    d5 = entry_d5.get()
    
    # 4. Gọi Back-end
    success = luu_diem_cho_hoc_sinh(ma_hs, ma_mon, hoc_ky, nam_hoc, d1, d2, d3, d4, d5)
    
    if success:
        messagebox.showinfo("Thành công", f"Đã lưu điểm cho học sinh {ma_hs}.")
        # Cập nhật lại Treeview để thấy điểm mới
        xu_ly_tai_danh_sach_ui() 
    else:
        messagebox.showerror("Lỗi", f"Lưu điểm thất bại cho {ma_hs}.")


# --- HÀM CHÍNH TẠO GIAO DIỆN ---

def open_form_quan_ly_diem(main_root, vai_tro, ten_dang_nhap):
    
    global combo_lop_diem, combo_mon_diem, combo_hoc_ky_diem, entry_nam_hoc_diem
    global tree_diem, entry_d1, entry_d2, entry_d3, entry_d4, entry_d5
    global label_thong_tin_hs, current_vai_tro, current_ma_gv
    
    # Lưu thông tin phân quyền
    current_vai_tro = vai_tro
    if vai_tro == 'giao_vien':
        current_ma_gv = tim_ma_giao_vien_tu_ten_dang_nhap(ten_dang_nhap)
        if current_ma_gv is None:
            messagebox.showerror("Lỗi nghiêm trọng", f"Không tìm thấy mã giáo viên cho {ten_dang_nhap}")
            return
    
    diem_window = tk.Toplevel(main_root)
    diem_window.title(f"Quản lý Điểm số ({vai_tro}: {ten_dang_nhap})")
    diem_window.geometry("1000x650") 
    diem_window.transient(main_root)
    diem_window.grab_set()

    # --- Frame 1: Lọc (Filter) ---
    filter_frame = ttk.LabelFrame(diem_window, text="Chọn Lớp và Môn học", padding=10)
    filter_frame.pack(padx=10, pady=10, fill="x", side=tk.TOP)
    
    ttk.Label(filter_frame, text="Lớp học:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    combo_lop_diem = ttk.Combobox(filter_frame, state="readonly", width=30)
    combo_lop_diem.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    # Gán sự kiện
    combo_lop_diem.bind("<<ComboboxSelected>>", on_lop_selected)
    
    ttk.Label(filter_frame, text="Môn học:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    combo_mon_diem = ttk.Combobox(filter_frame, state="readonly", width=30)
    combo_mon_diem.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    ttk.Label(filter_frame, text="Học kỳ:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    combo_hoc_ky_diem = ttk.Combobox(filter_frame, values=["1", "2"], state="readonly", width=5)
    combo_hoc_ky_diem.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    combo_hoc_ky_diem.current(0)
    
    ttk.Label(filter_frame, text="Năm học:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_nam_hoc_diem = ttk.Entry(filter_frame, width=10)
    entry_nam_hoc_diem.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    # Điền năm học
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    if current_month >= 8:
        entry_nam_hoc_diem.insert(0, f"{current_year}-{current_year + 1}")
    else:
        entry_nam_hoc_diem.insert(0, f"{current_year - 1}-{current_year}")
        
    btn_tai = ttk.Button(filter_frame, text="Tải Danh sách", command=xu_ly_tai_danh_sach_ui)
    btn_tai.grid(row=1, column=4, padx=10, pady=5)
    
    # Nạp ComboBox Lớp (kích hoạt toàn bộ)
    nap_combobox_lop(vai_tro, current_ma_gv)

    # --- Frame 2: Bảng điểm (Treeview) ---
    tree_frame = ttk.Frame(diem_window, padding=10)
    tree_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP, padx=10)

    columns = ("ma_hs", "ho_ten", "d15_1", "d15_2", "d1t_1", "d1t_2", "dck")
    tree_diem = ttk.Treeview(tree_frame, columns=columns, show="headings")

    tree_diem.heading("ma_hs", text="Mã HS")
    tree_diem.heading("ho_ten", text="Họ Tên")
    tree_diem.heading("d15_1", text="Điểm 15p (1)")
    tree_diem.heading("d15_2", text="Điểm 15p (2)")
    tree_diem.heading("d1t_1", text="Điểm 1 tiết (1)")
    tree_diem.heading("d1t_2", text="Điểm 1 tiết (2)")
    tree_diem.heading("dck", text="Điểm Cuối kỳ")
    
    tree_diem.column("ma_hs", width=80, anchor=tk.CENTER)
    tree_diem.column("ho_ten", width=150)
    tree_diem.column("d15_1", width=80, anchor=tk.CENTER)
    tree_diem.column("d15_2", width=80, anchor=tk.CENTER)
    tree_diem.column("d1t_1", width=90, anchor=tk.CENTER)
    tree_diem.column("d1t_2", width=90, anchor=tk.CENTER)
    tree_diem.column("dck", width=90, anchor=tk.CENTER)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree_diem.yview)
    tree_diem.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree_diem.pack(fill=tk.BOTH, expand=True)

    tree_diem.bind("<<TreeviewSelect>>", on_tree_select_diem)
    
    # --- Frame 3: Nhập điểm ---
    nhap_frame = ttk.LabelFrame(diem_window, text="Nhập/Sửa điểm", padding=10)
    nhap_frame.pack(padx=10, pady=10, fill="x", side=tk.TOP)
    
    label_thong_tin_hs = ttk.Label(nhap_frame, text="Chọn một học sinh từ danh sách...", font=("Arial", 10, "bold"))
    label_thong_tin_hs.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="w")
    
    ttk.Label(nhap_frame, text="15p (1):").grid(row=1, column=0, padx=5, pady=5)
    entry_d1 = ttk.Entry(nhap_frame, width=5)
    entry_d1.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(nhap_frame, text="15p (2):").grid(row=1, column=2, padx=5, pady=5)
    entry_d2 = ttk.Entry(nhap_frame, width=5)
    entry_d2.grid(row=1, column=3, padx=5, pady=5)
    
    ttk.Label(nhap_frame, text="1 Tiết (1):").grid(row=1, column=4, padx=5, pady=5)
    entry_d3 = ttk.Entry(nhap_frame, width=5)
    entry_d3.grid(row=1, column=5, padx=5, pady=5)
    
    ttk.Label(nhap_frame, text="1 Tiết (2):").grid(row=1, column=6, padx=5, pady=5)
    entry_d4 = ttk.Entry(nhap_frame, width=5)
    entry_d4.grid(row=1, column=7, padx=5, pady=5)
    
    ttk.Label(nhap_frame, text="Cuối kỳ:").grid(row=1, column=8, padx=5, pady=5)
    entry_d5 = ttk.Entry(nhap_frame, width=5)
    entry_d5.grid(row=1, column=9, padx=5, pady=5)
    
    btn_luu = ttk.Button(nhap_frame, text="Lưu điểm cho HS này", command=xu_ly_luu_diem_ui)
    btn_luu.grid(row=1, column=10, padx=20, pady=5, sticky="e")
    
    nhap_frame.columnconfigure(10, weight=1) # Đẩy nút Lưu sang phải
    
    main_root.wait_window(diem_window)