import tkinter as tk
from tkinter import ttk, messagebox

# Import các hàm logic Back-end
from Logic.database_logic import (
    lay_danh_sach_gv_cho_combobox,
    lay_tat_ca_lop,
    them_lop,
    sua_lop,
    xoa_lop
)

# Biến toàn cục
entry_ma_lop = None
entry_ten_lop = None
entry_nien_khoa = None
combo_gvcn = None
tree_lop = None 

# Biến để lưu trữ map giữa Tên GV và Mã GV
# Ví dụ: {'Cô A': 'GV001', 'Thầy B': 'GV002'}
gv_map = {}

# --- CÁC HÀM XỬ LÝ SỰ KIỆN ---

def cap_nhat_danh_sach_lop():
    """Tải dữ liệu lớp và hiển thị lên Treeview"""
    print("[UI] Đang cập nhật danh sách lớp...")
    for row in tree_lop.get_children():
        tree_lop.delete(row)
    
    danh_sach = lay_tat_ca_lop()
    
    for lop in danh_sach:
        # lop[4] là ten_gv, nếu là None (do LEFT JOIN) thì hiển thị ""
        ten_gv = lop[4] if lop[4] else "Chưa gán"
        # Tạo tuple mới để hiển thị
        display_data = (lop[0], lop[1], lop[2], ten_gv)
        
        tree_lop.insert("", tk.END, values=display_data, 
                        # Lưu trữ dữ liệu gốc (bao gồm mã gvcn) vào tag
                        tags=(lop[3],)) 

def nap_danh_sach_gvcn():
    """Nạp danh sách GV vào ComboBox và tạo map tra cứu"""
    global gv_map
    gv_map.clear() # Xóa map cũ
    try:
        danh_sach_gv = lay_danh_sach_gv_cho_combobox()
        
        # Tạo danh sách tên để hiển thị
        gv_display_list = []
        for (ma_gv, ten_gv) in danh_sach_gv:
            display_name = f"{ten_gv} ({ma_gv})" # Hiển thị: Cô A (GV001)
            gv_display_list.append(display_name)
            gv_map[display_name] = ma_gv # Tạo map: {'Cô A (GV001)': 'GV001'}
            
        combo_gvcn['values'] = gv_display_list
        
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải danh sách giáo viên: {e}")

def get_ma_gv_from_display_name(display_name):
    """Hàm tiện ích để tra cứu Mã GV từ Tên hiển thị"""
    return gv_map.get(display_name, None) # Trả về None nếu không tìm thấy

def get_display_name_from_ma_gv(ma_gv_can_tim):
    """Hàm tiện ích để tra cứu Tên hiển thị từ Mã GV"""
    for display_name, ma_gv in gv_map.items():
        if ma_gv == ma_gv_can_tim:
            return display_name
    return "" # Trả về rỗng nếu không tìm thấy

def them_lop_ui():
    print("[UI] Nút 'Thêm Lớp' được nhấn")
    ma_lop = entry_ma_lop.get()
    ten_lop = entry_ten_lop.get()
    nien_khoa = entry_nien_khoa.get()
    gvcn_display_name = combo_gvcn.get()
    
    # Tra cứu Mã GV từ tên hiển thị
    ma_gvcn = get_ma_gv_from_display_name(gvcn_display_name)
    
    if not ma_lop or not ten_lop:
        messagebox.showwarning("Thiếu thông tin", "Mã Lớp và Tên Lớp là bắt buộc.")
        return
        
    success = them_lop(ma_lop, ten_lop, nien_khoa, ma_gvcn)
    
    if success:
        messagebox.showinfo("Thành công", "Đã thêm lớp học thành công!")
        cap_nhat_danh_sach_lop()
        lam_moi_form_lop()
    else:
        messagebox.showerror("Lỗi", "Thêm lớp thất bại (Mã Lớp có thể đã tồn tại?)")

def sua_lop_ui():
    print("[UI] Nút 'Sửa Lớp' được nhấn")
    
    ma_lop = entry_ma_lop.get()
    ten_lop = entry_ten_lop.get()
    nien_khoa = entry_nien_khoa.get()
    gvcn_display_name = combo_gvcn.get()
    ma_gvcn = get_ma_gv_from_display_name(gvcn_display_name)

    if not ma_lop:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một lớp để sửa.")
        return

    success = sua_lop(ma_lop, ten_lop, nien_khoa, ma_gvcn)
    
    if success:
        messagebox.showinfo("Thành công", "Cập nhật thông tin lớp thành công!")
        cap_nhat_danh_sach_lop()
        lam_moi_form_lop()
    else:
        messagebox.showerror("Lỗi", "Cập nhật thất bại.")

def xoa_lop_ui():
    print("[UI] Nút 'Xóa Lớp' được nhấn")
    
    ma_lop = entry_ma_lop.get()
    if not ma_lop:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một lớp để xóa.")
        return

    if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa lớp {ma_lop} không? (Học sinh thuộc lớp này sẽ bị ảnh hưởng)"):
        success = xoa_lop(ma_lop)
        
        if success:
            messagebox.showinfo("Thành công", "Đã xóa lớp học.")
            cap_nhat_danh_sach_lop()
            lam_moi_form_lop()
        else:
            messagebox.showerror("Lỗi", "Xóa thất bại (Lớp có thể vẫn còn học sinh).")

def lam_moi_form_lop():
    print("[UI] Làm mới form Lớp")
    entry_ma_lop.config(state='normal')
    entry_ma_lop.delete(0, tk.END)
    entry_ten_lop.delete(0, tk.END)
    entry_nien_khoa.delete(0, tk.END)
    combo_gvcn.set("")
    
def on_tree_select_lop(event):
    selected_item = tree_lop.focus()
    if not selected_item:
        return
        
    # values = (ma_lop, ten_lop, nien_khoa, ten_gvcn)
    values = tree_lop.item(selected_item, 'values') 
    # tag[0] = ma_gvcn
    tags = tree_lop.item(selected_item, 'tags')
    
    if not values:
        return

    lam_moi_form_lop()
    
    entry_ma_lop.insert(0, values[0])
    entry_ma_lop.config(state='disabled') 
    entry_ten_lop.insert(0, values[1])
    entry_nien_khoa.insert(0, values[2])
    
    # Tìm tên hiển thị dựa trên Mã GVCN (lưu trong tag)
    ma_gvcn_cu = tags[0] if tags else None
    display_name_can_chon = get_display_name_from_ma_gv(ma_gvcn_cu)
    combo_gvcn.set(display_name_can_chon)


# --- HÀM CHÍNH TẠO GIAO DIỆN ---

def open_form_quan_ly_lop(main_root):
    
    global entry_ma_lop, entry_ten_lop, entry_nien_khoa, combo_gvcn, tree_lop
    
    lop_window = tk.Toplevel(main_root)
    lop_window.title("Quản lý Lớp học")
    lop_window.geometry("800x500") 
    lop_window.transient(main_root)
    lop_window.grab_set()

    # --- Frame 1: Form nhập liệu ---
    form_frame = ttk.LabelFrame(lop_window, text="Thông tin lớp học", padding=10)
    form_frame.pack(padx=10, pady=10, fill="x", side=tk.TOP)
    
    form_frame.columnconfigure(1, weight=1)

    # Hàng 1: Mã Lớp, Tên Lớp
    ttk.Label(form_frame, text="Mã Lớp:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_ma_lop = ttk.Entry(form_frame)
    entry_ma_lop.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Tên Lớp:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_ten_lop = ttk.Entry(form_frame)
    entry_ten_lop.grid(row=0, column=3, padx=5, pady=5, sticky="ew", columnspan=2)

    # Hàng 2: Niên khóa, GVCN
    ttk.Label(form_frame, text="Niên khóa:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_nien_khoa = ttk.Entry(form_frame)
    entry_nien_khoa.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="GV Chủ nhiệm:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    combo_gvcn = ttk.Combobox(form_frame, state="readonly")
    combo_gvcn.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
    # Nạp danh sách GV ngay khi mở
    nap_danh_sach_gvcn()


    # --- Frame 2: Các nút chức năng ---
    button_frame = ttk.Frame(lop_window, padding=10)
    button_frame.pack(fill="x", side=tk.TOP)

    btn_them = ttk.Button(button_frame, text="Thêm", command=them_lop_ui)
    btn_them.pack(side=tk.LEFT, padx=5)
    btn_sua = ttk.Button(button_frame, text="Sửa", command=sua_lop_ui)
    btn_sua.pack(side=tk.LEFT, padx=5)
    btn_xoa = ttk.Button(button_frame, text="Xóa", command=xoa_lop_ui)
    btn_xoa.pack(side=tk.LEFT, padx=5)
    btn_lam_moi = ttk.Button(button_frame, text="Làm mới", command=lam_moi_form_lop)
    btn_lam_moi.pack(side=tk.LEFT, padx=5)

    # --- Frame 3: Bảng hiển thị (Treeview) ---
    tree_frame = ttk.Frame(lop_window, padding=10)
    tree_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    columns = ("ma_lop", "ten_lop", "nien_khoa", "gvcn")
    tree_lop = ttk.Treeview(tree_frame, columns=columns, show="headings")

    tree_lop.heading("ma_lop", text="Mã Lớp")
    tree_lop.heading("ten_lop", text="Tên Lớp")
    tree_lop.heading("nien_khoa", text="Niên khóa")
    tree_lop.heading("gvcn", text="GV Chủ nhiệm")
    
    tree_lop.column("ma_lop", width=100, anchor=tk.CENTER)
    tree_lop.column("ten_lop", width=200)
    tree_lop.column("nien_khoa", width=100, anchor=tk.CENTER)
    tree_lop.column("gvcn", width=200)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree_lop.yview)
    tree_lop.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree_lop.pack(fill=tk.BOTH, expand=True)

    tree_lop.bind("<<TreeviewSelect>>", on_tree_select_lop)

    # --- Tải dữ liệu ban đầu ---
    cap_nhat_danh_sach_lop()

    main_root.wait_window(lop_window)