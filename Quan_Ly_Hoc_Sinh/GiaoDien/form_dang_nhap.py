import tkinter as tk
from tkinter import ttk, messagebox

#Import hàm logic từ file back-end
from Logic.database_logic import kiem_tra_dang_nhap

#import ham mo form Chinh
from GiaoDien.form_chinh import open_form_chinh

def open_form_dang_nhap():
    
    # --- Hàm xử lý sự kiện cho button ---
    def xu_ly_dang_nhap_button():
        #Lấy dữ liệu từ ô Entry 
        ten_dang_nhap = entry_user.get()
        mat_khau = entry_pass.get()
        
        print(f"Đang thử đăng nhập với: {ten_dang_nhap} / {mat_khau}")

        #Kiểm tra rỗng
        if not ten_dang_nhap or not mat_khau:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ Tên đăng nhập và Mật khẩu.")
            return

       
        vai_tro = kiem_tra_dang_nhap(ten_dang_nhap, mat_khau)
        
        # 4. Xử lý kết quả trả về 
        if vai_tro:
            root.destroy()  # Đóng form đăng nhập
            
            open_form_chinh(vai_tro,ten_dang_nhap)  # Mở form chính, truyền vai trò và tên đăng nhập
            
        else:
            messagebox.showerror("Thất bại", "Sai Tên đăng nhập hoặc Mật khẩu!")


    # --- Thiết kế giao diện ---
    root = tk.Tk()
    root.title("Đăng nhập - Quản lý Học sinh")
    root.geometry("300x150")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center') # Đặt giữa màn hình

    style = ttk.Style(root)
    style.theme_use('clam')

    main_frame = ttk.Frame(root, padding="20 20 20 20")
    main_frame.pack(expand=True, fill=tk.BOTH)

    # Tên đăng nhập
    label_user = ttk.Label(main_frame, text="Tên đăng nhập:")
    label_user.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entry_user = ttk.Entry(main_frame, width=25)
    entry_user.grid(row=0, column=1, padx=5, pady=5)

    # Mật khẩu
    label_pass = ttk.Label(main_frame, text="Mật khẩu:")
    label_pass.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    entry_pass = ttk.Entry(main_frame, width=25, show="*")
    entry_pass.grid(row=1, column=1, padx=5, pady=5)

    # Frame cho các Button
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=2, column=0, columnspan=2, pady=10)

    # Button Đăng nhập 
    button_login = ttk.Button(button_frame, text="Đăng nhập", command=xu_ly_dang_nhap_button)
    button_login.pack(side=tk.LEFT, padx=10)

    # Button Thoát
    button_exit = ttk.Button(button_frame, text="Thoát", command=root.quit)
    button_exit.pack(side=tk.RIGHT, padx=10)

    root.mainloop()