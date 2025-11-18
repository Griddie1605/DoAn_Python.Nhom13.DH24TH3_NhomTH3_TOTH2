import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# Import các hàm logic Back-end
from Logic.database_logic import (
    lay_danh_sach_gv_cho_combobox,
    lay_tat_ca_lop_cho_combobox,
    lay_tat_ca_mon_hoc_cho_combobox,
    lay_danh_sach_phan_cong,
    them_phan_cong,
    xoa_phan_cong
)

# Biến toàn cục
combo_gv = None
combo_lop_pc = None
combo_mon_hoc = None
entry_hoc_ky = None
entry_nam_hoc = None
tree_phan_cong = None 

# Biến map tra cứu
gv_map_pc = {}
lop_map_pc = {}
mh_map_pc = {}

# --- CÁC HÀM XỬ LÝ SỰ KIỆN ---

def cap_nhat_danh_sach_phan_cong():
    """Tải dữ liệu phân công và hiển thị lên Treeview"""
    print("[UI] Đang cập nhật danh sách phân công...")
    for row in tree_phan_cong.get_children():
        tree_phan_cong.delete(row)
    
    danh_sach = lay_danh_sach_phan_cong()
    
    for pc in danh_sach:
        # pc[0] là id_phan_cong
        tree_phan_cong.insert("", tk.END, values=pc)

def nap_danh_sach_combobox():
    """Nạp dữ liệu cho cả 3 ComboBox"""
    global gv_map_pc, lop_map_pc, mh_map_pc
    gv_map_pc.clear()
    lop_map_pc.clear()
    mh_map_pc.clear()
    
    try:
        # Nạp Giáo viên
        danh_sach_gv = lay_danh_sach_gv_cho_combobox()
        gv_display_list = []
        for (ma_gv, ten_gv) in danh_sach_gv:
            display = f"{ten_gv} ({ma_gv})"
            gv_display_list.append(display)
            gv_map_pc[display] = ma_gv
        combo_gv['values'] = gv_display_list
        
        # Nạp Lớp học
        danh_sach_lop = lay_tat_ca_lop_cho_combobox()
        lop_display_list = []
        for (ma_lop, ten_lop) in danh_sach_lop:
            display = f"{ten_lop} ({ma_lop})"
            lop_display_list.append(display)
            lop_map_pc[display] = ma_lop
        combo_lop_pc['values'] = lop_display_list

        # Nạp Môn học
        danh_sach_mh = lay_tat_ca_mon_hoc_cho_combobox()
        mh_display_list = []
        for (ma_mh, ten_mh) in danh_sach_mh:
            display = f"{ten_mh} ({ma_mh})"
            mh_display_list.append(display)
            mh_map_pc[display] = ma_mh
        combo_mon_hoc['values'] = mh_display_list

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải dữ liệu ComboBox: {e}")

def get_ma_from_display(map_dict, display_name):
    """Hàm tiện ích tra cứu mã từ tên hiển thị"""
    return map_dict.get(display_name, None)

def them_phan_cong_ui():
    print("[UI] Nút 'Phân công' được nhấn")
    # 1. Lấy dữ liệu
    gv_display = combo_gv.get()
    lop_display = combo_lop_pc.get()
    mh_display = combo_mon_hoc.get()
    hoc_ky = entry_hoc_ky.get()
    nam_hoc = entry_nam_hoc.get()
    
    # 2. Tra cứu Mã
    ma_gv = get_ma_from_display(gv_map_pc, gv_display)
    ma_lop = get_ma_from_display(lop_map_pc, lop_display)
    ma_mh = get_ma_from_display(mh_map_pc, mh_display)
    
    # 3. Kiểm tra
    if not (ma_gv and ma_lop and ma_mh and hoc_ky and nam_hoc):
        messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ các trường.")
        return
        
    # 4. Gọi Back-end
    success = them_phan_cong(ma_gv, ma_lop, ma_mh, hoc_ky, nam_hoc)
    
    if success:
        messagebox.showinfo("Thành công", "Đã thêm phân công thành công!")
        cap_nhat_danh_sach_phan_cong()
    else:
        messagebox.showerror("Lỗi", "Thêm phân công thất bại (Phân công này có thể đã tồn tại?)")

def xoa_phan_cong_ui():
    print("[UI] Nút 'Xóa Phân công' được nhấn")
    
    selected_item = tree_phan_cong.focus()
    if not selected_item:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một phân công để xóa.")
        return

    # Lấy ID phân công (giá trị đầu tiên trong hàng)
    id_phan_cong = tree_phan_cong.item(selected_item, 'values')[0]
    
    if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa phân công (ID: {id_phan_cong}) không?"):
        success = xoa_phan_cong(id_phan_cong)
        
        if success:
            messagebox.showinfo("Thành công", "Đã xóa phân công.")
            cap_nhat_danh_sach_phan_cong()
        else:
            messagebox.showerror("Lỗi", "Xóa thất bại.")

# --- HÀM CHÍNH TẠO GIAO DIỆN ---

def open_form_phan_cong(main_root):
    
    global combo_gv, combo_lop_pc, combo_mon_hoc, entry_hoc_ky, entry_nam_hoc, tree_phan_cong
    
    pc_window = tk.Toplevel(main_root)
    pc_window.title("Phân công Giảng dạy")
    pc_window.geometry("900x500") 
    pc_window.transient(main_root)
    pc_window.grab_set()

    # --- Frame 1: Form nhập liệu ---
    form_frame = ttk.LabelFrame(pc_window, text="Thêm phân công mới", padding=10)
    form_frame.pack(padx=10, pady=10, fill="x", side=tk.TOP)
    
    form_frame.columnconfigure(1, weight=1)
    form_frame.columnconfigure(3, weight=1)

    # Hàng 1: Giáo viên, Lớp
    ttk.Label(form_frame, text="Giáo viên:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    combo_gv = ttk.Combobox(form_frame, state="readonly", width=30)
    combo_gv.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Lớp học:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    combo_lop_pc = ttk.Combobox(form_frame, state="readonly", width=30)
    combo_lop_pc.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    # Hàng 2: Môn học, Học kỳ, Năm học
    ttk.Label(form_frame, text="Môn học:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    combo_mon_hoc = ttk.Combobox(form_frame, state="readonly", width=30)
    combo_mon_hoc.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(form_frame, text="Học kỳ:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_hoc_ky = ttk.Combobox(form_frame, values=["1", "2"])
    entry_hoc_ky.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    entry_hoc_ky.current(0) # Mặc định là học kỳ 1

    ttk.Label(form_frame, text="Năm học:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_nam_hoc = ttk.Entry(form_frame)
    entry_nam_hoc.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    # Tự động điền năm học hiện tại, ví dụ: 2024-2025
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    if current_month >= 8: # Sau tháng 8
        entry_nam_hoc.insert(0, f"{current_year}-{current_year + 1}")
    else:
        entry_nam_hoc.insert(0, f"{current_year - 1}-{current_year}")

    # Nút Thêm
    btn_them = ttk.Button(form_frame, text="Phân công", command=them_phan_cong_ui)
    btn_them.grid(row=2, column=3, padx=5, pady=10, sticky="e")
    
    # Nạp dữ liệu cho các ComboBox
    nap_danh_sach_combobox()

    # --- Frame 2: Bảng hiển thị (Treeview) ---
    tree_frame = ttk.LabelFrame(pc_window, text="Danh sách đã phân công", padding=10)
    tree_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP, padx=10, pady=5)

    columns = ("id", "giao_vien", "lop", "mon_hoc", "hoc_ky", "nam_hoc")
    tree_phan_cong = ttk.Treeview(tree_frame, columns=columns, show="headings")

    tree_phan_cong.heading("id", text="ID")
    tree_phan_cong.heading("giao_vien", text="Giáo viên")
    tree_phan_cong.heading("lop", text="Lớp học")
    tree_phan_cong.heading("mon_hoc", text="Môn học")
    tree_phan_cong.heading("hoc_ky", text="Học kỳ")
    tree_phan_cong.heading("nam_hoc", text="Năm học")
    
    tree_phan_cong.column("id", width=50, anchor=tk.CENTER)
    tree_phan_cong.column("giao_vien", width=200)
    tree_phan_cong.column("lop", width=150)
    tree_phan_cong.column("mon_hoc", width=150)
    tree_phan_cong.column("hoc_ky", width=80, anchor=tk.CENTER)
    tree_phan_cong.column("nam_hoc", width=100, anchor=tk.CENTER)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree_phan_cong.yview)
    tree_phan_cong.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree_phan_cong.pack(fill=tk.BOTH, expand=True)

    # Nút Xóa Phân công
    btn_xoa = ttk.Button(pc_window, text="Xóa phân công đã chọn", command=xoa_phan_cong_ui)
    btn_xoa.pack(pady=10, padx=10, side=tk.RIGHT)
    
    # --- Tải dữ liệu ban đầu ---
    cap_nhat_danh_sach_phan_cong()

    main_root.wait_window(pc_window)