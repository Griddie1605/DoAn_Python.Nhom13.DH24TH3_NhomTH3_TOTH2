import tkinter as tk
from tkinter import ttk, messagebox

# Import các form con
# Import form_quan_ly_hoc_sinh để gọi hàm mở form quản lý học sinh
from GiaoDien.form_quan_ly_hoc_sinh import open_form_quan_ly_hoc_sinh

#Import form_quan_ly_giao_vien để gọi hàm mở form quản lý giáo viên
from GiaoDien.form_quan_ly_giao_vien import open_form_quan_ly_giao_vien

#Import form_quan_ly_lop để gọi hàm mở form quản lý lớp
from GiaoDien.form_quan_ly_lop import open_form_quan_ly_lop

#Import form_quan_ly_mon_hoc để gọi hàm mở form quản lý môn học
from GiaoDien.form_quan_ly_mon_hoc import open_form_quan_ly_mon_hoc

#import form_phan_cong để gọi hàm mở form phân công
from GiaoDien.form_phan_cong import open_form_phan_cong

#import form_quan_ly_diem để gọi hàm mở form quản lý điểm
from GiaoDien.form_quan_ly_diem import open_form_quan_ly_diem

# --- HÀM CHÍNH TẠO GIAO DIỆN FORM CHÍNH ---
def open_form_chinh(vai_tro,ten_dang_nhap):
    """
    Hàm tạo Form Chính của ứng dụng Quản lý Học sinh.
    vai_tro: Vai trò ('admin', 'giao_vien'...)
    """
    
    # --- Hàm xử lý cho các nút ---
    
    def xu_ly_nut_qlhs():
        print(f"[FORM CHINH] Chức năng QL Học sinh được gọi")
        # Gọi hàm mở form QLHS (từ file ta vừa tạo ở Bước 1)
        # Truyền 'root' vào để nó biết ai là cửa sổ cha
        open_form_quan_ly_hoc_sinh(root)

    def xu_ly_nut_qldiem():
        print(f"[FORM CHINH] Chức năng QL Điểm được gọi bởi {ten_dang_nhap}")
        
        open_form_quan_ly_diem(root, vai_tro, ten_dang_nhap)
        
    def xu_ly_nut_qlgv():
        open_form_quan_ly_giao_vien(root)
        
    def xu_ly_nut_qllop():
        print(f"[FORM CHINH] Chức năng QL Lớp được gọi")
        open_form_quan_ly_lop(root)

    def xu_ly_nut_qlmh():
        print(f"[FORM CHINH] Chức năng QL Môn học được gọi")
        open_form_quan_ly_mon_hoc(root)
    
    def xu_ly_nut_qlpc():
        print(f"[FORM CHINH] Chức năng Phân công được gọi")
        open_form_phan_cong(root)
        
    def dang_xuat():
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?"):
            root.destroy()

    # --- Thiết kế giao diện Form Chính ---
    
    root = tk.Tk()
    root.title(f"Quản lý Học sinh - Chào mừng {ten_dang_nhap}(Vai trò {vai_tro})")
    root.geometry("900x400")
    root.eval('tk::PlaceWindow . center') # Đặt giữa màn hình

    style = ttk.Style(root)
    style.theme_use('clam')

    # --- Tạo Menu Bar (Thanh menu) ---
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # Menu Hệ thống
    he_thong_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Hệ thống", menu=he_thong_menu)
    he_thong_menu.add_command(label="Đăng xuất", command=dang_xuat)
    he_thong_menu.add_separator()
    he_thong_menu.add_command(label="Thoát", command=root.quit)

    # ---  Tạo 2 Frame chính ---

    # 1. Sidebar (Thanh điều hướng bên trái)
    sidebar_frame = ttk.Frame(root, width=200, style='Card.TFrame')
    sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    
    # Không cho sidebar co lại khi đặt nút vào
    sidebar_frame.pack_propagate(False) 

    # 2. Main content area (Khu vực nội dung chính bên phải)
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # --- Thêm các nút vào SIDEBAR ---
    label_menu = ttk.Label(sidebar_frame, text="Menu", 
                           font=("Arial", 16, "bold"), anchor="center")
    label_menu.pack(pady=10, fill="x")
    
    ttk.Separator(sidebar_frame).pack(fill="x", pady=5)

    # Dùng .pack() cho các nút trong sidebar
    btn_qlhs = ttk.Button(sidebar_frame, text="Quản lý Học sinh", 
                          command=xu_ly_nut_qlhs, style='Accent.TButton')
    btn_qlhs.pack(pady=5, padx=10, fill="x")

    btn_qldiem = ttk.Button(sidebar_frame, text="Quản lý Điểm số", 
                            command=xu_ly_nut_qldiem, style='Accent.TButton')
    btn_qldiem.pack(pady=5, padx=10, fill="x")

    btn_qlgv = ttk.Button(sidebar_frame, text="Quản lý Giáo viên", 
                          command=xu_ly_nut_qlgv, style='Accent.TButton')
    btn_qlgv.pack(pady=5, padx=10, fill="x")

    btn_qllop = ttk.Button(sidebar_frame, text="Quản lý Lớp học", 
                           command=xu_ly_nut_qllop, style='Accent.TButton')
    btn_qllop.pack(pady=5, padx=10, fill="x")
    
    btn_qlmh = ttk.Button(sidebar_frame, text="Quản lý Môn học", 
                           command=xu_ly_nut_qlmh, style='Accent.TButton')
    btn_qlmh.pack(pady=5, padx=10, fill="x")

    btn_qlpc = ttk.Button(sidebar_frame, text="Phân công Giảng dạy", 
                           command=xu_ly_nut_qlpc, style='Accent.TButton')
    btn_qlpc.pack(pady=5, padx=10, fill="x")

    # --- Thêm nội dung vào MAIN_FRAME ---
    label_welcome = ttk.Label(main_frame, text=f"Chào mừng bạn đến với hệ thống!", 
                              font=("Arial", 24, "bold"), anchor="center")
    label_welcome.pack(pady=50)
    
    label_info = ttk.Label(main_frame, text="Vui lòng chọn một chức năng từ thanh menu bên trái.", 
                           font=("Arial", 14), anchor="center")
    label_info.pack(pady=10)

    # --- Phân quyền (Dùng .pack_forget() thay vì .grid_remove()) ---
    if vai_tro == 'giao_vien':
        btn_qlgv.pack_forget()
        btn_qllop.pack_forget()
        btn_qlmh.pack_forget()
        btn_qlpc.pack_forget()
    elif vai_tro == 'hoc_sinh':
        btn_qlhs.pack_forget()
        btn_qldiem.pack_forget()
        btn_qlgv.pack_forget()
        btn_qllop.pack_forget()
        btn_qlmh.pack_forget()
        btn_qlpc.pack_forget()

    # --- Chạy Form Chính ---
    root.mainloop()