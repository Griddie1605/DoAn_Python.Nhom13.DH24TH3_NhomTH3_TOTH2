/*
Do An Chuyen De Python
DATABASE Quan Ly Hoc Sinh
*/
CREATE DATABASE Quan_Ly_Hoc_Sinh
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;

USE Quan_Ly_Hoc_Sinh;

-- TABLE TaiKhoan
CREATE TABLE TaiKhoan(
	id_tai_khoan int primary key auto_increment,
    ten_dang_nhap varchar(100) not null unique,
    mat_khau varchar(100) not null,
    vai_tro varchar(50) not null   -- 'admin', 'giao vien', 'hoc sinh'
);

-- TABLE GiaoVien
CREATE TABLE GiaoVien(
	ma_giao_vien varchar(50) primary key,
    ho_ten varchar(100) not null,
    ngay_sinh date,
    gioi_tinh varchar(10),
    email varchar(100) unique,
    so_dien_thoai varchar(20),
    chuyen_mon varchar(100),
    
    id_tai_khoan int unique,
    foreign key (id_tai_khoan) references TaiKhoan(id_tai_khoan)
);

-- TABLE LopHoc
CREATE TABLE LopHoc(
	ma_lop varchar(50) primary key,
    ten_lop varchar(100) not null,
    nien_khoa varchar(20),
    
    ma_giao_vien_chu_nhiem varchar(50),
    foreign key (ma_giao_vien_chu_nhiem) references GiaoVien(ma_giao_vien)
);

-- TABLE HocSinh
CREATE TABLE HocSinh(
	ma_hoc_sinh VARCHAR(50) PRIMARY KEY,
    ho_ten VARCHAR(100) NOT NULL,
    ngay_sinh DATE NOT NULL,
    gioi_tinh VARCHAR(10),
    dia_chi VARCHAR(255),
    email VARCHAR(100) UNIQUE,
    so_dien_thoai VARCHAR(20),
    
    ma_lop VARCHAR(50),
    id_tai_khoan INT UNIQUE,
    
    FOREIGN KEY (ma_lop) REFERENCES LopHoc(ma_lop),
    FOREIGN KEY (id_tai_khoan) REFERENCES TaiKhoan(id_tai_khoan)
);

-- TABLE MonHoc
CREATE TABLE MonHoc(
	ma_mon_hoc VARCHAR(50) PRIMARY KEY,
    ten_mon_hoc VARCHAR(100) NOT NULL
);

-- TABLE PhanCongGiangDay
CREATE TABLE PhanCongGiangDay(
	id_phan_cong INT PRIMARY KEY AUTO_INCREMENT,
    ma_giao_vien VARCHAR(50),
    ma_lop VARCHAR(50),
    ma_mon_hoc VARCHAR(50),
    hoc_ky INT,
    nam_hoc VARCHAR(20),
    
    FOREIGN KEY (ma_giao_vien) REFERENCES GiaoVien(ma_giao_vien),
    FOREIGN KEY (ma_lop) REFERENCES LopHoc(ma_lop),
    FOREIGN KEY (ma_mon_hoc) REFERENCES MonHoc(ma_mon_hoc),
    
    UNIQUE(ma_giao_vien, ma_lop, ma_mon_hoc, hoc_ky, nam_hoc)
);

-- TABLE DiemSo
	CREATE TABLE DiemSo(
	id_diem INT PRIMARY KEY AUTO_INCREMENT,
    
    ma_hoc_sinh VARCHAR(50),
    ma_mon_hoc VARCHAR(50),
    
    hoc_ky INT,
    nam_hoc VARCHAR(20),
    
    diem_15phut_1 DECIMAL(4, 2),
    diem_15phut_2 DECIMAL(4, 2),
    diem_1tiet_1 DECIMAL(4, 2),
    diem_1tiet_2 DECIMAL(4, 2),
    diem_cuoi_ky DECIMAL(4, 2),
    
    FOREIGN KEY (ma_hoc_sinh) REFERENCES HocSinh(ma_hoc_sinh) ON DELETE CASCADE,
    FOREIGN KEY (ma_mon_hoc) REFERENCES MonHoc(ma_mon_hoc) ON DELETE CASCADE,
    
    UNIQUE (ma_hoc_sinh, ma_mon_hoc, hoc_ky, nam_hoc)
);

SET SQL_SAFE_UPDATES = 0;
SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM DiemSo;
DELETE FROM PhanCongGiangDay;
DELETE FROM HocSinh;
DELETE FROM LopHoc;
DELETE FROM MonHoc;
DELETE FROM GiaoVien;
DELETE FROM TaiKhoan;

SET FOREIGN_KEY_CHECKS = 1; 
SET SQL_SAFE_UPDATES = 1;

ALTER TABLE TaiKhoan AUTO_INCREMENT = 1;
ALTER TABLE PhanCongGiangDay AUTO_INCREMENT = 1;
ALTER TABLE DiemSo AUTO_INCREMENT = 1;

-- Du lieu mau de test chuong trinh
-- 1. TAI KHOAN (DE DANG NHAP)
INSERT INTO TaiKhoan (ten_dang_nhap, mat_khau, vai_tro) VALUES ('admin', '123', 'admin');
-- (Không cần lưu ID admin)

INSERT INTO TaiKhoan (ten_dang_nhap, mat_khau, vai_tro) VALUES ('gv001', '123', 'giao_vien');
SET @gv1_id = LAST_INSERT_ID(); -- Lưu ID GV001

INSERT INTO TaiKhoan (ten_dang_nhap, mat_khau, vai_tro) VALUES ('gv002', '123', 'giao_vien');
SET @gv2_id = LAST_INSERT_ID(); -- Lưu ID GV002

INSERT INTO TaiKhoan (ten_dang_nhap, mat_khau, vai_tro) VALUES ('hs001', '123', 'hoc_sinh');
SET @hs1_id = LAST_INSERT_ID(); -- Lưu ID HS001

INSERT INTO TaiKhoan (ten_dang_nhap, mat_khau, vai_tro) VALUES ('hs002', '123', 'hoc_sinh');
SET @hs2_id = LAST_INSERT_ID(); -- Lưu ID HS002

INSERT INTO TaiKhoan (ten_dang_nhap, mat_khau, vai_tro) VALUES ('hs003', '123', 'hoc_sinh');
SET @hs3_id = LAST_INSERT_ID(); -- Lưu ID HS003

-- 2. GIAO VIEN
INSERT INTO GiaoVien (ma_giao_vien, ho_ten, ngay_sinh, gioi_tinh, email, so_dien_thoai, chuyen_mon, id_tai_khoan) VALUES
('GV001', 'Co Nguyen Thi A', '1985-05-10', 'Nu','coa@email.com','090111222', 'Toan', @gv1_id), -- LINE KET VOI TAI KHOAN 'gv001' (ID=2)
('GV002', 'Thay Tran Van B', '1980-08-15', 'Nam','thayb@email.com', '090333444', 'Ly', @gv2_id);

-- 3. MON HOC
INSERT INTO MonHoc (ma_mon_hoc, ten_mon_hoc) VALUES
('TOAN', 'Toan Hoc'),
('LY', 'Vat Ly'),
('HOA', 'Hoa Hoc');

-- 4. LOP HOC 
INSERT INTO LopHoc (ma_lop, ten_lop, nien_khoa, ma_giao_vien_chu_nhiem) VALUES
('10A1', 'Lop 10A1', '2024-2027', 'GV001'),
('10A2', 'Lop 10A2', '2024-2027', 'GV002');

-- 5. HOC SINH 
INSERT INTO HocSinh (ma_hoc_sinh, ho_ten, ngay_sinh, gioi_tinh, dia_chi, email, so_dien_thoai, ma_lop, id_tai_khoan) VALUES
('HS001', 'Tran Binh Trong', '2008-01-01', 'Nam', '123 Nguyen Trai','trong_dth235799@student.agu.edu.vn', '0911111111', '10A1', @hs1_id),
('HS002', 'Tong Thanh Vinh', '2008-02-02', 'Nam', '456 Le Loi','vinh_dth235816@student.agu.edu.vn', '0922222222', '10A1', @hs2_id),
('HS003', 'Le Van Cuong', '2008-03-03', 'Nam', '789 Tran Hung Dao','cuong_dth123456@student.agu.edu.vn', '0933333333', '10A2', @hs3_id);

-- 6. PHAN CONG GIANG DAY
INSERT INTO PhanCongGiangDay (ma_giao_vien, ma_lop, ma_mon_hoc, hoc_ky, nam_hoc) VALUES
('GV001', '10A1', 'TOAN', 1, '2024-2025'), -- GV001 DAY TOAN LOP 10A1
('GV001', '10A2', 'TOAN', 1, '2024-2025'), -- GV001 DAY TOAN LOP 10A2
('GV002', '10A1', 'LY', 1, '2024-2025'),   -- GV002 DAY LY LOP 10A1
('GV002', '10A2', 'LY', 1, '2024-2025');   -- GV002 DAY LY LOP 10A2

-- 7. DIEM SO
INSERT INTO DiemSo (ma_hoc_sinh, ma_mon_hoc, hoc_ky, nam_hoc, diem_15phut_1, diem_1tiet_1, diem_cuoi_ky) VALUES
('HS001', 'TOAN', 1, '2024-2025', 9.0, 9.5, 10.0), -- An, MON TOAN
('HS002', 'TOAN', 1, '2024-2025', 8.0, 8.5, 9.0),  -- Bình, MON TOAN
('HS001', 'LY', 1, '2024-2025', 7.0, 7.0, 7.5);   -- An, MON LY

-- -----------------------------------------------------
SELECT * FROM TaiKhoan;
SELECT * FROM GiaoVien;
SELECT * FROM LopHoc;
SELECT * FROM HocSinh;
SELECT * FROM PhanCongGiangDay;
SELECT * FROM DiemSo;
