
CREATE DATABASE QuanLyHocSinh
    DEFAULT CHARACTER SET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

USE QuanLyHocSinh;


SET SQL_SAFE_UPDATES = 0; 
SET FOREIGN_KEY_CHECKS = 0; 

-- XÓA DỮ LIỆU CŨ 
DROP TABLE IF EXISTS DiemSo;
DROP TABLE IF EXISTS HocSinh;
DROP TABLE IF EXISTS LopHoc;

-- Bảng 1: Lớp học 
CREATE TABLE LopHoc (
    ma_lop VARCHAR(50) PRIMARY KEY,
    ten_lop VARCHAR(100) NOT NULL
);

-- Bảng 2: Học sinh 
CREATE TABLE HocSinh (
    ma_hs VARCHAR(50) PRIMARY KEY,
    ho_ten VARCHAR(150) NOT NULL,
    gioi_tinh VARCHAR(10),
    ngay_sinh DATE,
    
    ma_lop VARCHAR(50), -- Khóa ngoại
    
    CONSTRAINT fk_lop
    FOREIGN KEY (ma_lop) REFERENCES LopHoc(ma_lop)
    ON DELETE SET NULL -- Nếu xóa Lớp, HocSinh sẽ bị set ma_lop = NULL
    ON UPDATE CASCADE -- Nếu đổi ma_lop, HocSinh tự động cập nhật
);


CREATE TABLE DiemSo (
    id_diem INT PRIMARY KEY AUTO_INCREMENT, -- Khóa chính tự tăng
    
    ma_hs VARCHAR(50), -- Khóa ngoại liên kết với HocSinh
    
    mon_hoc VARCHAR(100) NOT NULL, -- Giữ đơn giản, không cần bảng MonHoc
    hoc_ky INT,
    nam_hoc VARCHAR(20),
    
    -- Các cột điểm
    diem_15p DECIMAL(4, 2),
    diem_1tiet DECIMAL(4, 2),
    diem_cuoi_ky DECIMAL(4, 2),
    
    ghi_chu VARCHAR(255),
    
    -- Khóa ngoại liên kết tới HocSinh
    CONSTRAINT fk_hocsinh
    FOREIGN KEY (ma_hs) REFERENCES HocSinh(ma_hs)
    ON DELETE CASCADE -- Nếu xóa Học sinh, Điểm của họ cũng bị xóa
);




INSERT INTO LopHoc (ma_lop, ten_lop) VALUES
('10A1', 'Lớp 10A1'),
('10A2', 'Lớp 10A2'),
('11A1', 'Lớp 11A1');


INSERT INTO HocSinh (ma_hs, ho_ten, gioi_tinh, ngay_sinh, ma_lop) VALUES
('HS001', 'Nguyễn Văn An', 'Nam', '2008-01-15', '10A1'),
('HS002', 'Trần Thị Bình', 'Nữ', '2008-03-20', '10A1'),
('HS003', 'Lê Văn Cường', 'Nam', '2007-05-10', '11A1');


INSERT INTO DiemSo (ma_hs, mon_hoc, hoc_ky, nam_hoc, diem_15p, diem_1tiet, diem_cuoi_ky, ghi_chu)
VALUES
('HS001', 'Toán', 1, '2024-2025', 8.0, 8.5, 9.0, 'Học tốt'),
('HS001', 'Lý', 1, '2024-2025', 7.0, 7.5, 8.0, NULL),
('HS002', 'Toán', 1, '2024-2025', 9.0, 9.0, 9.5, 'Phát biểu nhiều'),
('HS003', 'Toán', 1, '2024-2025', 6.0, 7.0, 7.0, 'Cần cố gắng');


SET FOREIGN_KEY_CHECKS = 1; 
SET SQL_SAFE_UPDATES = 1; 


SELECT * FROM LopHoc;
SELECT * FROM HocSinh;
SELECT * FROM DiemSo;