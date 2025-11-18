import tkinter as tk
from tkinter import ttk, messagebox

# Import các hàm logic Back-end
from Logic.database_logic import (
    lay_tat_ca_mon_hoc,
    them_mon_hoc,
    sua_mon_hoc,
    xoa_mon_hoc
)

# Biến toàn cục
entry_ma_mh = None
entry_ten_mh = None
tree_mon_hoc = None 

# --- CÁC HÀM XỬ LÝ SỰ KIỆN ---

def cap_nhat_danh_sach_mon_hoc():
    """Tải dữ liệu môn học và hiển thị lên Treeview"""
    print("[UI] Đang cập nhật danh sách môn học...")
    for row in tree_mon_hoc.get_children():
        tree_mon_hoc.delete(row)
    
    danh_sach = lay_tat_ca_mon_hoc()
    
    for mh in danh_sach:
        tree_mon_hoc.insert("", tk.END, values=mh)

def them_mon_hoc_ui():
    print("[UI] Nút 'Thêm Môn' được nhấn")
    ma_mh = entry_ma_mh.get()
    ten_mh = entry_ten_mh.get()
    
    if not ma_mh or not ten_mh:
        messagebox.showwarning("Thiếu thông tin", "Mã Môn học và Tên Môn học là bắt buộc.")
        return
        
    success = them_mon_hoc(ma_mh, ten_mh)
    
    if success:
        messagebox.showinfo("Thành công", "Đã thêm môn học thành công!")
        cap_nhat_danh_sach_mon_hoc() 
        lam_moi_form_mh()
    else:
        messagebox.showerror("Lỗi", "Thêm môn học thất bại (Mã Môn học có thể đã tồn tại?)")

def sua_mon_hoc_ui():
    print("[UI] Nút 'Sửa Môn' được nhấn")
    
    ma_mh = entry_ma_mh.get()
    ten_mh = entry_ten_mh.get()

    if not ma_mh:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một môn học để sửa.")
        return

    success = sua_mon_hoc(ma_mh, ten_mh)
    
    if success:
        messagebox.showinfo("Thành công", "Cập nhật thông tin môn học thành công!")
        cap_nhat_danh_sach_mon_hoc()
        lam_moi_form_mh()
    else:
        messagebox.showerror("Lỗi", "Cập nhật thất bại.")

def xoa_mon_hoc_ui():
    print("[UI] Nút 'Xóa Môn' được nhấn")
    
    ma_mh = entry_ma_mh.get()
    if not ma_mh:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một môn học để xóa.")
        return

    if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa môn học mã {ma_mh} không?"):
        success = xoa_mon_hoc(ma_mh)
        
        if success:
            messagebox.showinfo("Thành công", "Đã xóa môn học.")
            cap_nhat_danh_sach_mon_hoc()
            lam_moi_form_mh()
        else:
            messagebox.showerror("Lỗi", "Xóa thất bại (Môn học có thể đã có điểm hoặc được phân công).")

def lam_moi_form_mh():
    print("[UI] Làm mới form Môn học")
    entry_ma_mh.config(state='normal')
    entry_ma_mh.delete(0, tk.END)
    entry_ten_mh.delete(0, tk.END)
    
def on_tree_select_mh(event):
    selected_item = tree_mon_hoc.focus()
    if not selected_item:
        return
        
    values = tree_mon_hoc.item(selected_item, 'values')
    if not values:
        return

    lam_moi_form_mh()
    
    entry_ma_mh.insert(0, values[0])
    entry_ma_mh.config(state='disabled') 
    entry_ten_mh.insert(0, values[1])


# --- HÀM CHÍNH TẠO GIAO DIỆN ---

def open_form_quan_ly_mon_hoc(main_root):
    
    global entry_ma_mh, entry_ten_mh, tree_mon_hoc
    
    mh_window = tk.Toplevel(main_root)
    mh_window.title("Quản lý Môn học")
    mh_window.geometry("600x400") 
    mh_window.transient(main_root)
    mh_window.grab_set()

    # --- Frame 1: Form nhập liệu ---
    form_frame = ttk.LabelFrame(mh_window, text="Thông tin môn học", padding=10)
    form_frame.pack(padx=10, pady=10, fill="x", side=tk.TOP)
    
    form_frame.columnconfigure(1, weight=1)

    # Hàng 1: Mã Môn học, Tên Môn học
    ttk.Label(form_frame, text="Mã Môn học:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_ma_mh = ttk.Entry(form_frame)
    entry_ma_mh.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Tên Môn học:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_ten_mh = ttk.Entry(form_frame)
    entry_ten_mh.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    # --- Frame 2: Các nút chức năng ---
    button_frame = ttk.Frame(mh_window, padding=10)
    button_frame.pack(fill="x", side=tk.TOP)

    btn_them = ttk.Button(button_frame, text="Thêm", command=them_mon_hoc_ui)
    btn_them.pack(side=tk.LEFT, padx=5)
    btn_sua = ttk.Button(button_frame, text="Sửa", command=sua_mon_hoc_ui)
    btn_sua.pack(side=tk.LEFT, padx=5)
    btn_xoa = ttk.Button(button_frame, text="Xóa", command=xoa_mon_hoc_ui)
    btn_xoa.pack(side=tk.LEFT, padx=5)
    btn_lam_moi = ttk.Button(button_frame, text="Làm mới", command=lam_moi_form_mh)
    btn_lam_moi.pack(side=tk.LEFT, padx=5)

    # --- Frame 3: Bảng hiển thị (Treeview) ---
    tree_frame = ttk.Frame(mh_window, padding=10)
    tree_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    columns = ("ma_mh", "ten_mh")
    tree_mon_hoc = ttk.Treeview(tree_frame, columns=columns, show="headings")

    tree_mon_hoc.heading("ma_mh", text="Mã Môn học")
    tree_mon_hoc.heading("ten_mh", text="Tên Môn học")
    
    tree_mon_hoc.column("ma_mh", width=100, anchor=tk.CENTER)
    tree_mon_hoc.column("ten_mh", width=300)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree_mon_hoc.yview)
    tree_mon_hoc.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree_mon_hoc.pack(fill=tk.BOTH, expand=True)

    tree_mon_hoc.bind("<<TreeviewSelect>>", on_tree_select_mh)

    # --- Tải dữ liệu ban đầu ---
    cap_nhat_danh_sach_mon_hoc()

    main_root.wait_window(mh_window)