USE [master]
GO
/****** Object:  Database [DARKTHESTORE]    Script Date: 2026/03/07 21:28:27 ******/
CREATE DATABASE [DARKTHESTORE]

GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [DARKTHESTORE].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [DARKTHESTORE] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET ARITHABORT OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [DARKTHESTORE] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [DARKTHESTORE] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET  ENABLE_BROKER 
GO
ALTER DATABASE [DARKTHESTORE] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [DARKTHESTORE] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET RECOVERY FULL 
GO
ALTER DATABASE [DARKTHESTORE] SET  MULTI_USER 
GO
ALTER DATABASE [DARKTHESTORE] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [DARKTHESTORE] SET DB_CHAINING OFF 
GO
ALTER DATABASE [DARKTHESTORE] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [DARKTHESTORE] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [DARKTHESTORE] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [DARKTHESTORE] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'DARKTHESTORE', N'ON'
GO
ALTER DATABASE [DARKTHESTORE] SET QUERY_STORE = ON
GO
ALTER DATABASE [DARKTHESTORE] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [DARKTHESTORE]
GO
/****** Object:  Table [dbo].[DANHGIA]    Script Date: 2026/03/07 21:28:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DANHGIA](
	[ID_GH] [int] IDENTITY(1,1) NOT NULL,
	[NoiDung] [nvarchar](2000) NULL,
	[Diem] [int] NULL,
	[ID_KH] [int] NULL,
	[ID_SP] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_GH] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[DANHMUC]    Script Date: 2026/03/07 21:28:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DANHMUC](
	[ID_DM] [int] IDENTITY(1,1) NOT NULL,
	[TenDM] [nvarchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_DM] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[DONHANG]    Script Date: 2026/03/07 21:28:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DONHANG](
	[ID_DH] [int] IDENTITY(1,1) NOT NULL,
	[NgayLap] [date] NULL,
	[GhiChu] [nvarchar](255) NULL,
	[TrangThai] [nvarchar](30) NULL,
	[ID_KH] [int] NULL,
	[ID_KM] [int] NULL,
	[Ten] [nvarchar](255) NULL,
	[DiaChiGiaoHang] [nvarchar](4000) NULL,
	[SDT] [nvarchar](10) NULL,
	[PhuongthucTT] [nvarchar](255) NULL,
	[PhuongThucNhanHang] [nvarchar](1000) NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_DH] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[DONHANG_SANPHAM]    Script Date: 2026/03/07 21:28:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DONHANG_SANPHAM](
	[ID_DH] [int] NOT NULL,
	[ID_SP] [int] NOT NULL,
	[SoLuong] [int] NULL,
	[DonGia] [int] NULL,
 CONSTRAINT [pk1] PRIMARY KEY CLUSTERED 
(
	[ID_DH] ASC,
	[ID_SP] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[GIOHANG]    Script Date: 2026/03/07 21:28:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[GIOHANG](
	[ID_GH] [int] IDENTITY(1,1) NOT NULL,
	[ID_KH] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_GH] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[GIOHANG_SANPHAM]    Script Date: 2026/03/07 21:28:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[GIOHANG_SANPHAM](
	[ID_GH] [int] NOT NULL,
	[ID_SP] [int] NOT NULL,
	[SoLuong] [int] NULL,
 CONSTRAINT [pk] PRIMARY KEY CLUSTERED 
(
	[ID_GH] ASC,
	[ID_SP] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[KHACHHANG]    Script Date: 2026/03/07 21:28:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[KHACHHANG](
	[ID_KH] [int] IDENTITY(1,1) NOT NULL,
	[TenKH] [nvarchar](50) NULL,
	[DiaChi] [nvarchar](255) NULL,
	[SDT] [nvarchar](10) NULL,
	[GioTinh] [nvarchar](5) NULL,
	[NgaySinh] [date] NULL,
	[Email] [nvarchar](50) NULL,
	[TK] [nvarchar](20) NULL,
	[MK] [nvarchar](20) NULL,
	[PhanQuyen] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_KH] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[KHUYENMAI]    Script Date: 2026/03/07 21:28:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[KHUYENMAI](
	[ID_KM] [int] IDENTITY(1,1) NOT NULL,
	[GiamGia] [int] NULL,
	[Mota] [nvarchar](4000) NULL,
	[TrangThai] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_KM] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[QUANGCAO]    Script Date: 2026/03/07 21:28:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[QUANGCAO](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Loai] [nvarchar](20) NULL,
	[Url_Image] [nvarchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SANPHAM]    Script Date: 2026/03/07 21:28:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SANPHAM](
	[ID_SP] [int] IDENTITY(1,1) NOT NULL,
	[MaSP] [nvarchar](20) NULL,
	[TenSP] [nvarchar](255) NULL,
	[Gia] [int] NULL,
	[GiaBan] [int] NULL,
	[Mota] [nvarchar](max) NULL,
	[Status_SP] [int] NULL,
	[NgayTao] [date] NULL,
	[SoLuong] [int] NULL,
	[SoLuongBan] [int] NULL,
	[Images_url] [nvarchar](255) NULL,
	[ID_DM] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_SP] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[DANHGIA] ON 

INSERT [dbo].[DANHGIA] ([ID_GH], [NoiDung], [Diem], [ID_KH], [ID_SP]) VALUES (1, N'san pham chat luong tot
', 5, 3, 52)
INSERT [dbo].[DANHGIA] ([ID_GH], [NoiDung], [Diem], [ID_KH], [ID_SP]) VALUES (2, N'san pham chat luong tot
', 5, 3, 52)
INSERT [dbo].[DANHGIA] ([ID_GH], [NoiDung], [Diem], [ID_KH], [ID_SP]) VALUES (3, N'vùyvuyvfuy', 3, 4, 75)
SET IDENTITY_INSERT [dbo].[DANHGIA] OFF
GO
SET IDENTITY_INSERT [dbo].[DANHMUC] ON 

INSERT [dbo].[DANHMUC] ([ID_DM], [TenDM]) VALUES (12, N'HP Omen (Gaming)')
INSERT [dbo].[DANHMUC] ([ID_DM], [TenDM]) VALUES (16, N'Lenovo Legion (Gaming)')
INSERT [dbo].[DANHMUC] ([ID_DM], [TenDM]) VALUES (17, N'Asus VivoBook')
INSERT [dbo].[DANHMUC] ([ID_DM], [TenDM]) VALUES (20, N'Asus TUF Gaming')
INSERT [dbo].[DANHMUC] ([ID_DM], [TenDM]) VALUES (21, N'Asus ROG (Republic of Gamers)')
INSERT [dbo].[DANHMUC] ([ID_DM], [TenDM]) VALUES (23, N'Acer Swift')
INSERT [dbo].[DANHMUC] ([ID_DM], [TenDM]) VALUES (25, N'Acer Nitro (Gaming)')
INSERT [dbo].[DANHMUC] ([ID_DM], [TenDM]) VALUES (34, N'MSI Gaming GF/GL/GP')
SET IDENTITY_INSERT [dbo].[DANHMUC] OFF
GO
SET IDENTITY_INSERT [dbo].[DONHANG] ON 

INSERT [dbo].[DONHANG] ([ID_DH], [NgayLap], [GhiChu], [TrangThai], [ID_KH], [ID_KM], [Ten], [DiaChiGiaoHang], [SDT], [PhuongthucTT], [PhuongThucNhanHang]) VALUES (1, CAST(N'2025-12-22' AS Date), NULL, N'Đã huỷ', 1, NULL, N'Nguyễn Thanh Tùng', N'Hà Nội', N'0333893870', N'BANK_QR', N'Giao hàng')
INSERT [dbo].[DONHANG] ([ID_DH], [NgayLap], [GhiChu], [TrangThai], [ID_KH], [ID_KM], [Ten], [DiaChiGiaoHang], [SDT], [PhuongthucTT], [PhuongThucNhanHang]) VALUES (2, CAST(N'2025-12-22' AS Date), NULL, N'Đã huỷ', 1, NULL, N'Nguyễn Thanh Tùng', N'Hà Nội', N'0333893870', N'COD', N'Giao hàng')
INSERT [dbo].[DONHANG] ([ID_DH], [NgayLap], [GhiChu], [TrangThai], [ID_KH], [ID_KM], [Ten], [DiaChiGiaoHang], [SDT], [PhuongthucTT], [PhuongThucNhanHang]) VALUES (3, CAST(N'2025-12-23' AS Date), NULL, N'Đã giao', 4, 2, N'Anh Vũ', N'Hà nội', N'0931674365', N'COD', N'Giao hàng')
INSERT [dbo].[DONHANG] ([ID_DH], [NgayLap], [GhiChu], [TrangThai], [ID_KH], [ID_KM], [Ten], [DiaChiGiaoHang], [SDT], [PhuongthucTT], [PhuongThucNhanHang]) VALUES (4, CAST(N'2025-12-23' AS Date), NULL, N'Đã giao', 4, NULL, N'Anh Vũ abc', N'Hà nội', N'0931674365', N'BANK_QR', N'Giao hàng')
INSERT [dbo].[DONHANG] ([ID_DH], [NgayLap], [GhiChu], [TrangThai], [ID_KH], [ID_KM], [Ten], [DiaChiGiaoHang], [SDT], [PhuongthucTT], [PhuongThucNhanHang]) VALUES (5, CAST(N'2025-12-23' AS Date), NULL, N'Đã giao', 4, NULL, N'Anh Vũ', N'Hà nội', N'0931674365', N'COD', N'Giao hàng')
INSERT [dbo].[DONHANG] ([ID_DH], [NgayLap], [GhiChu], [TrangThai], [ID_KH], [ID_KM], [Ten], [DiaChiGiaoHang], [SDT], [PhuongthucTT], [PhuongThucNhanHang]) VALUES (6, CAST(N'2025-12-23' AS Date), NULL, N'Đã huỷ', 4, 4, N'Anh Vũ', N'Hà nội', N'0931674365', N'VNPAY', N'Giao hàng')
INSERT [dbo].[DONHANG] ([ID_DH], [NgayLap], [GhiChu], [TrangThai], [ID_KH], [ID_KM], [Ten], [DiaChiGiaoHang], [SDT], [PhuongthucTT], [PhuongThucNhanHang]) VALUES (7, CAST(N'2025-12-23' AS Date), NULL, N'Đã giao', 4, NULL, N'Anh Vũ', N'Hà nội', N'0931674365', N'COD', N'Giao hàng')
INSERT [dbo].[DONHANG] ([ID_DH], [NgayLap], [GhiChu], [TrangThai], [ID_KH], [ID_KM], [Ten], [DiaChiGiaoHang], [SDT], [PhuongthucTT], [PhuongThucNhanHang]) VALUES (8, CAST(N'2025-12-23' AS Date), NULL, N'Đang xác nhận', 5, NULL, N'tung ', N'HaNoi', N'0931674365', N'VNPAY', N'Giao hàng')
INSERT [dbo].[DONHANG] ([ID_DH], [NgayLap], [GhiChu], [TrangThai], [ID_KH], [ID_KM], [Ten], [DiaChiGiaoHang], [SDT], [PhuongthucTT], [PhuongThucNhanHang]) VALUES (9, CAST(N'2025-12-29' AS Date), NULL, N'Đã thanh toán', 4, 1, N'Anh Vũu', N'Hà nội', N'0931674365', N'VNPAY', N'Giao hàng')
SET IDENTITY_INSERT [dbo].[DONHANG] OFF
GO
INSERT [dbo].[DONHANG_SANPHAM] ([ID_DH], [ID_SP], [SoLuong], [DonGia]) VALUES (1, 51, 1, 52900000)
INSERT [dbo].[DONHANG_SANPHAM] ([ID_DH], [ID_SP], [SoLuong], [DonGia]) VALUES (2, 52, 7, 46500000)
INSERT [dbo].[DONHANG_SANPHAM] ([ID_DH], [ID_SP], [SoLuong], [DonGia]) VALUES (3, 53, 2, 39900000)
INSERT [dbo].[DONHANG_SANPHAM] ([ID_DH], [ID_SP], [SoLuong], [DonGia]) VALUES (3, 54, 1, 24500000)
INSERT [dbo].[DONHANG_SANPHAM] ([ID_DH], [ID_SP], [SoLuong], [DonGia]) VALUES (4, 51, 3, 52900000)
INSERT [dbo].[DONHANG_SANPHAM] ([ID_DH], [ID_SP], [SoLuong], [DonGia]) VALUES (5, 56, 2, 19500000)
INSERT [dbo].[DONHANG_SANPHAM] ([ID_DH], [ID_SP], [SoLuong], [DonGia]) VALUES (6, 52, 3, 46500000)
INSERT [dbo].[DONHANG_SANPHAM] ([ID_DH], [ID_SP], [SoLuong], [DonGia]) VALUES (7, 93, 3, 11500000)
INSERT [dbo].[DONHANG_SANPHAM] ([ID_DH], [ID_SP], [SoLuong], [DonGia]) VALUES (8, 53, 1, 39900000)
INSERT [dbo].[DONHANG_SANPHAM] ([ID_DH], [ID_SP], [SoLuong], [DonGia]) VALUES (9, 75, 1, 35500000)
GO
SET IDENTITY_INSERT [dbo].[GIOHANG] ON 

INSERT [dbo].[GIOHANG] ([ID_GH], [ID_KH]) VALUES (1, 1)
INSERT [dbo].[GIOHANG] ([ID_GH], [ID_KH]) VALUES (2, 4)
SET IDENTITY_INSERT [dbo].[GIOHANG] OFF
GO
INSERT [dbo].[GIOHANG_SANPHAM] ([ID_GH], [ID_SP], [SoLuong]) VALUES (1, 51, 5)
GO
SET IDENTITY_INSERT [dbo].[KHACHHANG] ON 

INSERT [dbo].[KHACHHANG] ([ID_KH], [TenKH], [DiaChi], [SDT], [GioTinh], [NgaySinh], [Email], [TK], [MK], [PhanQuyen]) VALUES (1, N'Nguyễn Thanh Tùng', N'Hà Nội', N'0333893870', N'Nam', CAST(N'2025-12-02' AS Date), N'tung24060808@gmail.com', N'tung24062004', N'abc123', 2)
INSERT [dbo].[KHACHHANG] ([ID_KH], [TenKH], [DiaChi], [SDT], [GioTinh], [NgaySinh], [Email], [TK], [MK], [PhanQuyen]) VALUES (3, N'Admin', N'HaNoi', N'', N'Nam', CAST(N'1900-01-01' AS Date), N'', N'admin', N'abc123', 1)
INSERT [dbo].[KHACHHANG] ([ID_KH], [TenKH], [DiaChi], [SDT], [GioTinh], [NgaySinh], [Email], [TK], [MK], [PhanQuyen]) VALUES (4, N'Anh Vũu', N'Hà nội', N'0931674365', N'Nam', CAST(N'2023-06-25' AS Date), N'Vule@gmail.com', N'anhvu', N'123', NULL)
INSERT [dbo].[KHACHHANG] ([ID_KH], [TenKH], [DiaChi], [SDT], [GioTinh], [NgaySinh], [Email], [TK], [MK], [PhanQuyen]) VALUES (5, N'tung ', N'HaNoi', N'0931674365', N'Nam', CAST(N'2011-06-17' AS Date), N'Vulet8322@gmail.com', N'thanhtung', N'abc123', 2)
SET IDENTITY_INSERT [dbo].[KHACHHANG] OFF
GO
SET IDENTITY_INSERT [dbo].[KHUYENMAI] ON 

INSERT [dbo].[KHUYENMAI] ([ID_KM], [GiamGia], [Mota], [TrangThai]) VALUES (1, 5, N'Giảm giá 5% ', 1)
INSERT [dbo].[KHUYENMAI] ([ID_KM], [GiamGia], [Mota], [TrangThai]) VALUES (2, 10, N'Giảm giá 10% ', 1)
INSERT [dbo].[KHUYENMAI] ([ID_KM], [GiamGia], [Mota], [TrangThai]) VALUES (3, 15, N'Giảm giá 15% ', 1)
INSERT [dbo].[KHUYENMAI] ([ID_KM], [GiamGia], [Mota], [TrangThai]) VALUES (4, 20, N'Giảm giá 20% ', 1)
INSERT [dbo].[KHUYENMAI] ([ID_KM], [GiamGia], [Mota], [TrangThai]) VALUES (5, 1000000, N'Giảm giá 1 triệu đồng', 1)
INSERT [dbo].[KHUYENMAI] ([ID_KM], [GiamGia], [Mota], [TrangThai]) VALUES (6, 2000000, N'Giảm giá 2 triệu đồng', 1)
INSERT [dbo].[KHUYENMAI] ([ID_KM], [GiamGia], [Mota], [TrangThai]) VALUES (7, 5000000, N'Giảm giá  5 triệu đồng', 1)
SET IDENTITY_INSERT [dbo].[KHUYENMAI] OFF
GO
SET IDENTITY_INSERT [dbo].[QUANGCAO] ON 

INSERT [dbo].[QUANGCAO] ([Id], [Loai], [Url_Image]) VALUES (1, N'Banner', N'banner-8ccb8b05.jpg')
INSERT [dbo].[QUANGCAO] ([Id], [Loai], [Url_Image]) VALUES (2, N'Banner', N'banner-a0d363e5.jpg')
SET IDENTITY_INSERT [dbo].[QUANGCAO] OFF
GO
SET IDENTITY_INSERT [dbo].[SANPHAM] ON 

INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (51, N'GIG01', N'Gigabyte Aorus Master 16', 55000000, 52900000, N'Laptop Gigabyte Aorus Master 16 là siêu phẩm gaming hàng đầu sở hữu màn hình 16 inch 2K 240Hz siêu mượt giúp loại bỏ hoàn toàn hiện tượng xé hình trong các trận đấu eSport đỉnh cao. Sức mạnh từ CPU Intel Core i7-13700H và card đồ họa RTX 4070 mang lại hiệu năng xử lý đồ họa cực mạnh cho mọi tựa game AAA hiện nay. Hệ thống tản nhiệt Windforce Infinity cùng 5 ống đồng giúp máy luôn mát mẻ và ổn định khi hoạt động ở cường độ cao.', 1, CAST(N'2025-12-22' AS Date), 47, 6, N'90370_laptop_gigabyte_gaming_aorus_master_16_byh_c5vne64sh_0008_layer_2.jpg;anh1.jpg;anh2.jpg', NULL)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (52, N'GIG02', N'Gigabyte Aorus 16X AI', 48000000, 46500000, N'Dòng laptop Gigabyte Aorus 16X AI 2024 tiên phong trong việc tích hợp công nghệ trí tuệ nhân tạo tối ưu hiệu suất với chip Intel Core i9 Gen 14 cực khủng. Thiết kế máy mang phong cách Aorus Beacon với dải đèn LED RGB huyền ảo tạo cảm hứng bất tận cho game thủ chuyên nghiệp. Màn hình QHD+ chuẩn màu sắc nét cùng hệ thống làm mát hiện đại giúp duy trì hiệu năng bền bỉ trong suốt thời gian dài chiến game hoặc làm việc đồ họa nặng.', 1, CAST(N'2025-12-22' AS Date), 45, 0, N'AORUS-MASTER-16-BYH-C5VNE64SH.jpg;anh3.jpg;anh4.jpg', 20)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (53, N'GIG03', N'Gigabyte Aero 16 OLED', 42000000, 39900000, N'Gigabyte Aero 16 OLED là chiếc máy trạm di động hoàn hảo dành cho nhà thiết kế với màn hình OLED 4K rực rỡ đạt chuẩn màu X-Rite Pantone chính xác tuyệt đối. Vỏ nhôm CNC nguyên khối cực kỳ sang trọng và bền bỉ nhưng vẫn giữ được trọng lượng lý tưởng 1.9kg cho việc di chuyển. Máy tích hợp đầy đủ các cổng kết nối tốc độ cao như Thunderbolt 4 và Wi-Fi 6E giúp việc truyền tải các tệp dữ liệu video 4K trở nên nhanh chóng và đơn giản hơn.', 1, CAST(N'2025-12-22' AS Date), 27, 6, N'93016_laptop_gigabyte_gaming_aero_x16_x16_1vh93vnc94dh_0007_layer_2.jpg;anh5.jpg;anh1.jpg', 17)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (54, N'GIG04', N'Gigabyte G6 MF i7', 26000000, 24500000, N'Mẫu laptop Gigabyte G6 MF sở hữu cấu hình quốc dân với vi xử lý Core i7 thế hệ 13 và card rời RTX 4050 6GB mạnh mẽ cân tốt các tựa game đình đám. Màn hình 16 inch tần số quét 165Hz mang lại góc nhìn rộng và trải nghiệm chuyển động mượt mà không độ trễ. Thiết kế tối giản tinh tế nhưng không kém phần mạnh mẽ với hệ thống tản nhiệt Windforce cải tiến giúp máy giải nhiệt nhanh chóng thoát khí nóng ra ngoài tối ưu.', 1, CAST(N'2025-12-22' AS Date), 59, 2, N'91338_laptop_gigabyte_gaming_g6_mf_72vn854kh_0002_layer_3.jpg;anh2.jpg;anh3.jpg', 17)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (55, N'GIG05', N'Gigabyte A16 Advantage', 28500000, 26900000, N'Sự kết hợp hoàn hảo từ AMD với chip Ryzen 7 7735HS và Radeon RX 7600S mang đến hiệu năng đồng bộ tuyệt vời trên dòng Gigabyte A16. Màn hình 16 inch 165Hz viền mỏng cùng công nghệ SmartShift điều phối năng lượng thông minh giúp tối ưu hóa khung hình trong game. Đây là lựa chọn tuyệt vời cho người dùng yêu thích hệ sinh thái AMD với khả năng xử lý đồ họa mượt mà và nhiệt độ hoạt động cực kỳ ổn định trong phân khúc.', 1, CAST(N'2025-12-22' AS Date), 25, 0, N'93014_laptop_gigabyte_gaming_a16_a16_cvhi3vnc93sh_0006_layer_2.jpg;anh4.jpg;anh5.jpg', 23)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (56, N'GIG06', N'Gigabyte G5 MF 2023', 21000000, 19500000, N'Gigabyte G5 MF là mẫu laptop gaming phổ thông sở hữu sức mạnh từ card đồ họa RTX 4050 mới nhất giúp các bạn sinh viên có thể vừa học tập vừa giải trí đỉnh cao. Máy có thiết kế gọn nhẹ hơn so với các đối thủ cùng phân khúc giúp linh hoạt mang theo đến trường. Bàn phím có đèn nền tùy chỉnh cùng đầy đủ các cổng kết nối cần thiết như HDMI và USB Type-C hỗ trợ tối đa cho việc trình chiếu và kết nối thiết bị ngoại vi.', 1, CAST(N'2025-12-22' AS Date), 38, 6, N'91338_laptop_gigabyte_gaming_g6_mf_72vn854kh_0003_layer_2.jpg;anh1.jpg;anh2.jpg', 34)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (57, N'GIG07', N'Gigabyte Aero 14 OLED', 38000000, 35900000, N'Laptop Gigabyte Aero 14 OLED định nghĩa lại khái niệm máy tính xách tay đồ họa siêu di động với kích thước 14 inch nhỏ gọn và màn hình OLED 2.8K siêu sắc nét. Máy được trang bị cấu hình mạnh mẽ đáp ứng tốt nhu cầu render video và chỉnh sửa ảnh chuyên nghiệp ở bất cứ đâu. Thời lượng pin dài cùng khả năng sạc nhanh qua cổng Type-C giúp người dùng an tâm làm việc cả ngày dài mà không cần lo lắng về nguồn điện.', 1, CAST(N'2025-12-22' AS Date), 15, 0, N'AERO-X16-1VH93VNC94DH.jpg;anh3.jpg;anh5.jpg', 21)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (58, N'GIG08', N'Gigabyte AORUS 17H', 59000000, 56500000, N'Gigabyte AORUS 17H là quái thú gaming với màn hình khổng lồ 17.3 inch tần số quét lên tới 360Hz chuyên dụng cho các game thủ chuyên nghiệp đòi hỏi tốc độ phản hồi nhanh nhất. Card đồ họa RTX 4080 bên trong cho phép chơi game ở mức thiết lập Ultra một cách dễ dàng. Hệ thống tản nhiệt đồ sộ cùng vỏ máy hoàn thiện tinh xảo giúp chiếc máy này trở thành một trong những laptop gaming mạnh mẽ nhất trên thị trường hiện nay.', 1, CAST(N'2025-12-22' AS Date), 10, 0, N'90370_laptop_gigabyte_gaming_aorus_master_16_byh_c5vne64sh_0008_layer_2.jpg;anh4.jpg;anh1.jpg', 12)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (59, N'MSI01', N'MSI Thin 15 B13UC', 18500000, 17500000, N'MSI Thin 15 B13UC là sự lựa chọn hàng đầu cho những ai tìm kiếm sự cân bằng giữa tính di động và sức mạnh chơi game với trọng lượng nhẹ chỉ 1.86kg. Máy trang bị vi xử lý Intel Core i7 Gen 13 và card rời RTX 3050 mang lại hiệu suất ổn định cho cả công việc và giải trí. Vỏ nhôm phay xước màu đen sang trọng cùng hệ thống tản nhiệt Cooler Boost độc quyền giúp máy luôn duy trì được trạng thái hoạt động tốt nhất dưới áp lực nặng.', 1, CAST(N'2025-12-22' AS Date), 55, 0, N'90600_laptop_msi_thin_15_b13uc_2044vn_0005_layer_3.jpg;anh2.jpg;anh3.jpg', 34)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (60, N'MSI02', N'MSI Cyborg 15 A12V', 22500000, 21500000, N'Laptop MSI Cyborg 15 sở hữu phong cách thiết kế xuyên thấu Translucent độc nhất vô nhị lấy cảm hứng từ thế giới Cyberpunk huyền bí cho phép bạn chiêm ngưỡng một phần linh kiện bên trong. Máy được trang bị card RTX 4050 hỗ trợ DLSS 3 cực mạnh cùng màn hình 144Hz mượt mà mang đến trải nghiệm hình ảnh tuyệt vời. Bàn phím gõ êm ái cùng hệ thống âm thanh Hi-Res Audio sống động làm tăng thêm hưng phấn trong từng trận chiến game gay cấn.', 1, CAST(N'2025-12-22' AS Date), 35, 0, N'87151_laptop_msi_gaming_cyborg_14_a13udx_099vn_i7.jpg;anh4.jpg;anh5.jpg', 34)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (61, N'MSI03', N'MSI Sword 16 HX White', 31000000, 29500000, N'MSI Sword 16 HX khoác lên mình lớp vỏ màu trắng ngọc trai quý phái kết hợp cùng bàn phím RGB 24 vùng rực rỡ tạo nên sự khác biệt hoàn toàn so với các dòng gaming đen truyền thống. Sức mạnh bên trong đến từ chip xử lý dòng HX hiệu năng cực cao và hệ thống tản nhiệt Shared-Pipe thế hệ mới giúp tối ưu hóa luồng khí lạnh vào linh kiện. Màn hình 16 inch chuẩn màu 100% sRGB mang lại hình ảnh trung thực cho cả chơi game và làm đồ họa.', 1, CAST(N'2025-12-22' AS Date), 20, 0, N'80964_laptop_msi_gaming_sword_16_hx_b14vfkg_045vn__2.jpg;anh1.jpg;anh2.jpg', 34)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (62, N'MSI04', N'MSI Katana 15 B13V', 28000000, 26900000, N'Laptop MSI Katana 15 lấy cảm hứng từ thanh kiếm huyền thoại của võ sĩ Samurai mang thiết kế sắc sảo và mạnh mẽ với sự góp mặt của card đồ họa RTX 4060 8GB VRAM. Máy được tối ưu hóa cho hiệu suất chơi game vượt trội với công nghệ MUX Switch cho phép xuất hình trực tiếp từ GPU rời giúp tăng tối đa FPS. Hệ thống tản nhiệt Cooler Boost 5 với 2 quạt và 6 ống dẫn nhiệt đảm bảo máy luôn mát mẻ kể cả khi chiến các trận game dài hàng giờ.', 1, CAST(N'2025-12-22' AS Date), 28, 0, N'70977_laptop_msi_gaming_katana_15_b13_4.jpg;anh3.jpg;anh4.jpg', 34)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (63, N'MSI05', N'MSI Modern 14 C13M', 14500000, 13800000, N'MSI Modern 14 C13M là người bạn đồng hành lý tưởng cho sinh viên và dân văn phòng với thiết kế siêu mỏng nhẹ và tông màu Urban Silver tinh tế lịch sự. Máy trang bị vi xử lý Intel Core i5 thế hệ 13 đảm bảo xử lý mượt mà các tác vụ văn phòng và lướt web đa nhiệm nhiều tab cùng lúc. Bản lề 180 độ linh hoạt cùng bàn phím có độ nảy tốt mang lại cảm giác làm việc thoải mái trong thời gian dài. Thời lượng pin ấn tượng giúp bạn yên tâm sử dụng cả ngày.', 1, CAST(N'2025-12-22' AS Date), 70, 0, N'anh5.jpg;anh1.jpg;anh2.jpg', 34)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (64, N'MSI06', N'MSI Prestige 16 AI', 35000000, 33500000, N'Dòng MSI Prestige 16 AI hướng tới phân khúc doanh nhân cao cấp với vỏ nhôm nguyên khối và màn hình tỉ lệ 16:10 mở rộng không gian làm việc tối đa. Máy tích hợp nhân xử lý AI thế hệ mới giúp tự động tối ưu pin và âm thanh cuộc họp tùy theo môi trường sử dụng xung quanh. Bảo mật vân tay và nhận diện khuôn mặt IR mang lại sự an toàn tuyệt đối cho dữ liệu cá nhân. Đây là sự kết hợp hoàn hảo giữa thẩm mỹ sang trọng và công nghệ phần cứng tiên tiến nhất.', 1, CAST(N'2025-12-22' AS Date), 12, 0, N'anh3.jpg;anh4.jpg;anh5.jpg', 34)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (65, N'MSI07', N'MSI Pulse 17 B13V', 33000000, 31900000, N'MSI Pulse 17 mang phong cách thiết kế Pulsating Armor đầy mạnh mẽ với cấu hình chip i7 Gen 13 và card đồ họa RTX 40 Series mang lại trải nghiệm gaming tầm cao. Màn hình lớn 17.3 inch tần số quét 144Hz cho không gian quan sát rộng lớn giúp bạn không bỏ lỡ bất kỳ chi tiết nào trong trận đấu. Hệ thống âm thanh Nahimic 3 giả lập vòm sống động mang lại cảm giác đắm chìm vào thế giới ảo cùng bàn phím RGB 4 vùng cực kỳ bắt mắt và chuyên nghiệp.', 1, CAST(N'2025-12-22' AS Date), 18, 0, N'82948_laptop_msi_thin_15_11.jpg;anh1.jpg;anh2.jpg', 34)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (66, N'MSI08', N'MSI Stealth 14 Studio', 45000000, 42900000, N'MSI Stealth 14 Studio là sự giao thoa hoàn hảo giữa dòng máy chơi game và máy trạm đồ họa chuyên nghiệp với chứng nhận NVIDIA Studio giúp tăng tốc hơn 110 ứng dụng sáng tạo. Thân máy mỏng nhẹ nhưng chứa đựng sức mạnh kinh ngạc từ card đồ họa RTX 4070 và màn hình QHD+ 240Hz sắc nét. Hệ thống tản nhiệt buồng hơi Vapor Chamber tiên tiến giúp duy trì hiệu năng đỉnh cao trong một thân máy siêu mỏng mà không gây ra hiện tượng giảm xung nhịp.', 1, CAST(N'2025-12-22' AS Date), 8, 0, N'87151_laptop_msi_gaming_cyborg_14_a13udx_099vn_i7_balo.jpg;anh3.jpg;anh4.jpg', 34)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (67, N'MSI09', N'MSI Crosshair 15', 29500000, 27500000, N'Laptop MSI Crosshair 15 phiên bản đặc biệt sở hữu phong cách thiết kế độc đáo với các điểm nhấn màu vàng đặc trưng cùng bàn phím Spectrum Backlight rực rỡ. Cấu hình máy tối ưu cho các game thủ bắn súng FPS với màn hình có tần số quét cao và thời gian phản hồi cực nhanh. Công nghệ âm thanh vòm giúp định vị tiếng bước chân kẻ địch chính xác trong game mang lại lợi thế chiến thắng tuyệt đối cho người chơi trong mọi tình huống giao tranh kịch tính.', 1, CAST(N'2025-12-22' AS Date), 22, 0, N'anh5.jpg;anh1.jpg;anh2.jpg', 34)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (68, N'MSI10', N'MSI Raider GE78 HX', 68000000, 65000000, N'MSI Raider GE78 HX là một trong những laptop gaming mạnh nhất thế giới hiện nay với dải đèn LED Mystic Light chạy dọc thân máy tạo hiệu ứng thị giác cực đỉnh. Máy được trang bị cấu hình khủng khiếp với Core i9-14900HX và RTX 4080 giúp chinh phục mọi thử thách đồ họa nặng nề nhất. Hệ thống 6 loa âm thanh Dynaudio cao cấp cùng màn hình chuẩn màu chuyên nghiệp biến chiếc máy này thành một rạp chiếu phim di động và cỗ máy chiến game không đối thủ.', 1, CAST(N'2025-12-22' AS Date), 5, 0, N'80964_laptop_msi_gaming_sword_16_hx_b14vfkg_045vn.jpg;anh3.jpg;anh4.jpg', 34)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (69, N'LEN01', N'Lenovo LOQ 15AHP9', 24500000, 23500000, N'Lenovo LOQ 15AHP9 là dòng máy gaming mới sở hữu độ bền đạt chuẩn quân đội Mỹ giúp người dùng yên tâm sử dụng trong thời gian dài mà không lo hỏng hóc. Chip Ryzen 7 Gen 8 mạnh mẽ kết hợp card rời RTX mang lại hiệu suất chơi game mượt mà ở mức thiết lập cao. Thiết kế tản nhiệt hốc sau thông minh cùng màn hình 144Hz chuẩn màu sRGB giúp chiếc máy này trở thành lựa chọn quốc dân cho sinh viên các ngành kỹ thuật và đồ họa hiện nay.', 1, CAST(N'2025-12-22' AS Date), 40, 0, N'92958_laptop_lenovo_gaming_loq_15ahp10_83jg0047vn_0010_layer_3.jpg;anh1.jpg;anh2.jpg', 16)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (70, N'LEN02', N'Lenovo Legion 5 16IRX9', 36000000, 34500000, N'Lenovo Legion 5 16IRX9 là sự kết hợp hoàn hảo giữa vẻ ngoài lịch lãm và sức mạnh gaming hủy diệt bên trong với hệ thống tản nhiệt Legion Coldfront 5.0 tiên tiến. Màn hình 16 inch 2K+ độ sáng 500 nits mang lại hình ảnh cực kỳ sống động và sắc nét trong mọi môi trường ánh sáng. Bàn phím TrueStrike huyền thoại cho cảm giác gõ phím chân thực và chính xác giúp bạn làm chủ mọi trận đấu cũng như xử lý công việc văn phòng hiệu quả nhất.', 1, CAST(N'2025-12-22' AS Date), 25, 0, N'91370_laptop_lenovo_legion_5_15ahp10_83ly004gvn_0009_layer_3.jpg;anh3.jpg;anh4.jpg', 16)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (71, N'LEN03', N'Lenovo Legion Slim 5', 32000000, 30500000, N'Laptop Lenovo Legion Slim 5 mang lại sự linh hoạt tối đa với thiết kế mỏng nhẹ hơn dòng Pro nhưng vẫn giữ nguyên sức mạnh từ card đồ họa RTX 40 Series hiện đại. Vỏ máy nhôm nguyên khối mang lại cảm giác cầm nắm chắc chắn và sang trọng phù hợp cho những ai thường xuyên phải di chuyển. Hệ thống AI Engine+ giúp tối ưu hóa khung hình tự động theo thời gian thực đảm bảo trải nghiệm chơi game luôn mượt mà nhất mà không cần tùy chỉnh thủ công.', 1, CAST(N'2025-12-22' AS Date), 15, 0, N'92958_laptop_lenovo_gaming_loq_15ahp10_83jg0047vn_0011_layer_2.jpg;anh5.jpg;anh1.jpg', 16)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (72, N'LEN04', N'Lenovo Yoga Slim 7 AI', 29000000, 27900000, N'Lenovo Yoga Slim 7 AI là mẫu laptop văn phòng cao cấp sở hữu màn hình OLED tuyệt đẹp với độ tương phản cực cao giúp mọi hình ảnh trở nên rực rỡ và chân thực. Máy tích hợp nhân xử lý AI chuyên dụng giúp tăng tốc các tác vụ thông minh như xóa phông cuộc họp hay lọc nhiễu âm thanh bằng phần cứng. Trọng lượng siêu nhẹ cùng thời lượng pin lên tới 15 tiếng biến chiếc máy này thành trợ thủ đắc lực cho giới doanh nhân và người dùng yêu thích sự thời thượng.', 1, CAST(N'2025-12-22' AS Date), 30, 0, N'anh2.jpg;anh3.jpg;anh4.jpg', 16)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (73, N'LEN05', N'Lenovo IdeaPad Gaming 3', 18000000, 16900000, N'Lenovo IdeaPad Gaming 3 là mẫu laptop gaming giá rẻ bền bỉ sở hữu thiết kế đơn giản nhưng đậm chất mạnh mẽ với vi xử lý Ryzen 5 và card đồ họa GTX chuyên dụng. Máy đáp ứng tốt nhu cầu học tập làm việc và giải trí với các tựa game online phổ biến hiện nay. Bàn phím có hành trình sâu và đèn nền màu xanh dịu mắt giúp bạn thoải mái làm việc vào ban đêm mà không gây mỏi mắt đồng thời hệ thống tản nhiệt hoạt động êm ái không gây ồn ào.', 1, CAST(N'2025-12-22' AS Date), 45, 0, N'anh5.jpg;anh1.jpg;anh2.jpg', 16)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (74, N'LEN06', N'Lenovo Legion Pro 7i', 65000000, 62000000, N'Lenovo Legion Pro 7i là đỉnh cao của dòng laptop gaming Lenovo với vi xử lý Core i9-14900HX và RTX 4080 mang lại sức mạnh không giới hạn cho mọi tác vụ nặng nhất. Máy sở hữu màn hình 240Hz đạt chuẩn màu 100% DCI-P3 lý tưởng cho cả game thủ chuyên nghiệp và những nhà làm phim chuyên nghiệp. Công nghệ tản nhiệt buồng hơi Vapor Chamber giúp máy duy trì được hiệu suất tối đa mà vẫn giữ được sự ổn định tuyệt vời trong suốt quá trình sử dụng lâu dài.', 1, CAST(N'2025-12-22' AS Date), 6, 0, N'91370_laptop_lenovo_legion_5_15ahp10_83ly004gvn_0010_layer_2.jpg;anh3.jpg;anh4.jpg', 16)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (75, N'HP01', N'HP Omen 16 2024 Black', 37000000, 35500000, N'HP Omen 16 phiên bản 2024 mang đến trải nghiệm gaming cao cấp với màn hình 16.1 inch 165Hz sắc nét và thiết kế tối giản sang trọng. Máy trang bị card đồ họa RTX 4060 8GB cùng công nghệ tản nhiệt Omen Tempest Cooling giúp duy trì nhiệt độ mát mẻ dù chơi game ở thiết lập đồ họa cao nhất. Phần mềm Omen Gaming Hub cho phép người dùng tùy chỉnh đèn nền RGB 4 vùng và tối ưu hóa tài nguyên hệ thống một cách thông minh chỉ với một cú click chuột.', 1, CAST(N'2025-12-22' AS Date), 19, 1, N'91362_laptop_hp_gaming_omen_16_ah0186tx_bx9s1pa_0003_layer_3.jpg;anh1.jpg;anh2.jpg', 12)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (76, N'HP02', N'HP Victus 15 FA1139', 21500000, 19900000, N'HP Victus 15 sở hữu thiết kế logo chữ V hiện đại cùng tông màu xanh Performance Blue cực kỳ bắt mắt thu hút mọi ánh nhìn của các bạn trẻ sinh viên. Máy được trang bị cấu hình Core i5 Gen 13 và card RTX 3050 giúp xử lý mượt mà các tác vụ học tập và chiến game ổn định ở độ phân giải Full HD. Hệ thống tản nhiệt được cải tiến với khe thoát nhiệt rộng hơn giúp máy giải tỏa nhiệt năng nhanh chóng mang lại độ bền cao và sự ổn định cho linh kiện bên trong.', 1, CAST(N'2025-12-22' AS Date), 50, 0, N'laptop-hp-gaming-victus-15-fa2731tx-b85lnpa_0003_Layer-3.jpg;anh3.jpg;anh4.jpg', 12)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (77, N'HP03', N'HP Omen 17 2024', 45000000, 42900000, N'Dành cho những ai cần không gian hiển thị cực lớn thì HP Omen 17 với màn hình 17.3 inch QHD 240Hz là sự lựa chọn không thể tuyệt vời hơn. Máy mang trong mình sức mạnh của RTX 4070 mang lại khả năng xử lý hình ảnh tuyệt đỉnh cho các tựa game thế giới mở rộng lớn. Bàn phím cơ quang học cho tốc độ phản hồi siêu nhanh cùng hệ thống âm thanh Bang & Olufsen cao cấp biến chiếc laptop này thành một cỗ máy giải trí tối thượng cho những game thủ khó tính nhất.', 1, CAST(N'2025-12-22' AS Date), 10, 0, N'91362_laptop_hp_gaming_omen_16_ah0186tx_bx9s1pa_0004_layer_2.jpg;anh5.jpg;anh1.jpg', 12)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (78, N'HP04', N'HP Victus 16 S0077', 25500000, 23900000, N'HP Victus 16 mang đến màn hình lớn hơn một chút so với bản 15 inch cùng tần số quét 144Hz giúp tăng cường trải nghiệm thị giác khi chơi các game hành động nhanh. Cấu hình chạy chip Ryzen 7 mới nhất cùng card đồ họa RTX 4050 mang lại hiệu năng ổn định và tiết kiệm điện năng vượt trội. Thiết kế bàn phím có cụm phím số đầy đủ hỗ trợ tốt cho việc nhập liệu văn phòng kết hợp với tản nhiệt hai quạt giúp máy hoạt động êm ái trong mọi tác vụ hàng ngày.', 1, CAST(N'2025-12-22' AS Date), 30, 0, N'laptop-hp-gaming-victus-15-fb3115ax-lahp0352_0004_Layer-1.jpg;anh2.jpg;anh3.jpg', 12)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (79, N'HP05', N'HP Pavilion Gaming 15', 18500000, 17200000, N'Dòng laptop HP Pavilion Gaming 15 sở hữu thiết kế góc cạnh đặc trưng với các đường nét cắt gọt táo bạo mang đậm phong cách gaming. Máy trang bị cấu hình vừa đủ để đáp ứng tốt các nhu cầu học tập đa phương tiện và giải trí với các tựa game phổ biến như LOL hay Dota 2. Màn hình IPS sắc nét cùng hệ thống loa kép phía trên bàn phím mang lại âm thanh trực diện sống động giúp bạn đắm chìm hoàn toàn vào những thước phim hay trận đấu kịch tính nhất.', 1, CAST(N'2025-12-22' AS Date), 40, 0, N'laptop-hp-gaming-victus-15-fb3115ax-lahp0352_0003_Layer-2.jpg;anh4.jpg;anh5.jpg', 12)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (80, N'HP06', N'HP Envy 16 2023', 38000000, 35900000, N'HP Envy 16 là dòng laptop multimedia cao cấp sở hữu màn hình cảm ứng độ phân giải cao giúp thao tác trực tiếp cực kỳ tiện lợi cho các nhà thiết kế đồ họa. Máy trang bị card đồ họa rời chuyên dụng hỗ trợ tăng tốc cho các phần mềm Adobe như Photoshop hay Premiere một cách mượt mà. Vỏ nhôm bạc nguyên khối cực kỳ tinh tế cùng camera độ phân giải cao hỗ trợ lọc nhiễu bằng AI giúp bạn có những cuộc gọi video họp trực tuyến vô cùng chuyên nghiệp và rõ nét.', 1, CAST(N'2025-12-22' AS Date), 15, 0, N'laptop-hp-gaming-victus-15-fa2731tx-b85lnpa_0004_Layer-2.jpg;anh1.jpg;anh2.jpg', 12)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (81, N'ACE01', N'Acer Nitro V 15 Pro', 25500000, 23900000, N'Acer Nitro V 15 Pro là phiên bản lột xác hoàn toàn về thẩm mỹ với thiết kế mỏng nhẹ hơn nhưng vẫn giữ được chất gaming mạnh mẽ vốn có của dòng Nitro. Máy được trang bị card RTX 4050 hỗ trợ công nghệ DLSS 3 và Frame Generation giúp chơi mượt mọi tựa game AAA hiện nay ở mức thiết lập đồ họa cao. Hệ thống tản nhiệt hai quạt cùng phần mềm NitroSense độc quyền cho phép bạn kiểm soát hoàn toàn tốc độ quạt và nhiệt độ linh kiện trong quá trình sử dụng nặng.', 1, CAST(N'2025-12-22' AS Date), 35, 0, N'90816_laptop_acer_gaming_nitro_lite_nl16_71g_71uj_nh_d59sv_002_0006_layer_3.jpg;anh3.jpg;anh4.jpg', 25)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (82, N'ACE02', N'Acer Swift Go 14 AI', 26500000, 24900000, N'Acer Swift Go 14 AI là mẫu laptop mỏng nhẹ dẫn đầu xu hướng công nghệ với màn hình OLED 2.8K siêu sắc nét mang lại màu sắc rực rỡ và độ sâu tuyệt đối. Máy tích hợp vi xử lý Intel Core Ultra mới nhất với nhân NPU chuyên dụng để xử lý các tác vụ AI nhanh chóng và tiết kiệm điện. Trọng lượng siêu nhẹ chỉ 1.3kg cùng vỏ nhôm nhám sang trọng giúp bạn dễ dàng mang máy đi làm việc tại quán cafe hay công tác xa mà không cảm thấy nặng nề vướng víu.', 1, CAST(N'2025-12-22' AS Date), 20, 0, N'86164_laptop_acer_swift_lite_14_ai_sfl14_51m_56hs_nx_j1hsv__2.jpg;anh5.jpg;anh1.jpg', 23)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (83, N'ACE03', N'Acer Nitro 5 Tiger', 22500000, 20900000, N'Acer Nitro 5 Tiger là dòng laptop gaming huyền thoại được rất nhiều game thủ tin dùng nhờ khả năng tản nhiệt cực tốt và hiệu năng mạnh mẽ trong tầm giá. Máy sở hữu bàn phím RGB 4 vùng cực đẹp cùng màn hình 144Hz cho trải nghiệm chơi game mượt mà nhất. Hệ thống âm thanh DTS:X Ultra mang lại lợi thế định vị âm thanh chính xác giúp bạn làm chủ mọi trận đấu FPS kịch tính cùng đồng đội mà không bỏ lỡ bất kỳ tiếng động nhỏ nào của đối thủ.', 1, CAST(N'2025-12-22' AS Date), 50, 0, N'90816_laptop_acer_gaming_nitro_lite_nl16_71g_71uj_nh_d59sv_002_0007_layer_2.jpg;anh2.jpg;anh3.jpg', 25)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (84, N'ACE04', N'Acer Predator Helios Neo 16', 36000000, 34500000, N'Laptop Acer Predator Helios Neo 16 thuộc phân khúc gaming cao cấp với thiết kế hầm hố và hệ thống tản nhiệt kim loại lỏng cực kỳ đẳng cấp. Màn hình 16 inch 165Hz đạt chuẩn màu 100% sRGB cho hình ảnh trung thực và sống động hơn bao giờ hết. Card đồ họa RTX 4060 bên trong máy được cấp tối đa điện năng giúp hiệu suất chơi game đạt mức cao nhất có thể giúp bạn tự tin chiến game ở mức cài đặt đồ họa cao mà không lo bị tụt khung hình.', 1, CAST(N'2025-12-22' AS Date), 15, 0, N'90816_laptop_acer_gaming_nitro_lite_nl16_71g_71uj_nh_d59sv_002_0006_layer_3.jpg;anh4.jpg;anh5.jpg', 25)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (85, N'ACE05', N'Acer Swift 3 Luna', 18500000, 17500000, N'Acer Swift 3 Luna sở hữu thiết kế mỏng nhẹ thời trang với lớp vỏ kim loại chắc chắn và bền bỉ đạt tiêu chuẩn quân đội về độ bền va đập. Màn hình của máy đạt chuẩn màu sắc chuyên nghiệp giúp người dùng có được những giây phút giải trí và làm việc đồ họa cơ bản vô cùng thoải mái. Thời lượng pin lên tới 10 tiếng giúp bạn yên tâm sử dụng cả ngày dài tại trường học hay công ty mà không cần mang theo bộ sạc cồng kềnh giúp tối ưu hóa sự linh hoạt.', 1, CAST(N'2025-12-22' AS Date), 25, 0, N'86164_laptop_acer_swift_lite_14_ai_sfl14_51m_56hs_nx_j1hsv__2.jpg;anh1.jpg;anh2.jpg', 23)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (86, N'ACE06', N'Acer Nitro 16 Phoenix', 31000000, 29500000, N'Acer Nitro 16 Phoenix là mẫu laptop gaming có màn hình tuyệt đẹp trong phân khúc với độ sáng cao và tần số quét 165Hz giúp hình ảnh mượt mà tuyệt đối. Máy trang bị cấu hình mạnh mẽ đáp ứng tốt cả nhu cầu chơi game nặng lẫn làm đồ họa chuyên nghiệp như dựng phim hay vẽ 3D. Hệ thống tản nhiệt được cải tiến đáng kể với 4 khe thoát gió giúp duy trì nhiệt độ ổn định tuyệt vời kể cả khi hoạt động liên tục trong môi trường nắng nóng khắc nghiệt.', 1, CAST(N'2025-12-22' AS Date), 18, 0, N'90816_laptop_acer_gaming_nitro_lite_nl16_71g_71uj_nh_d59sv_002_0006_layer_3.jpg;anh3.jpg;anh5.jpg', 25)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (87, N'ASU01', N'Asus ROG Zephyrus G14 AI', 39000000, 37500000, N'Asus ROG Zephyrus G14 là mẫu laptop gaming 14 inch mạnh mẽ nhất thế giới sở hữu màn hình OLED Nebula đạt chuẩn màu sắc chuyên nghiệp cho dân đồ họa. Máy trang bị hệ thống đèn AniMe Matrix độc đáo ở mặt lưng cho phép bạn hiển thị các hoạt ảnh và thông báo cá nhân hóa theo phong cách riêng. Sức mạnh từ vi xử lý Ryzen 9 tích hợp nhân AI cùng card đồ họa RTX 40 Series trong một thân máy siêu mỏng nhẹ chỉ 1.5kg biến nó thành siêu phẩm công nghệ hàng đầu.', 1, CAST(N'2025-12-22' AS Date), 12, 0, N'90954_laptop_asus_gaming_rog_zephyrus_ga403wr_qs103ws_0011_layer_2.jpg;anh1.jpg;anh2.jpg', 21)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (88, N'ASU02', N'Asus TUF Gaming F15 2024', 21500000, 19990000, N'Asus TUF Gaming F15 luôn dẫn đầu về độ bền bỉ đạt chuẩn quân đội Mỹ với khả năng chịu va đập và nhiệt độ khắc nghiệt cực tốt. Máy sở hữu viên pin khủng 90Wh cùng khả năng sạc nhanh giúp game thủ yên tâm chiến game ở bất cứ đâu mà không bị gián đoạn. Cấu hình i7 Gen 13 và card RTX mạnh mẽ cùng hệ thống tản nhiệt 4 khe gió giúp máy luôn mát mẻ mang lại tuổi thọ linh kiện cao nhất cho người dùng trong suốt quá trình sử dụng lâu dài nhiều năm.', 1, CAST(N'2025-12-22' AS Date), 50, 0, N'92299_laptop_asus_gaming_v16_v3607vh_rp024w_0011_layer_2.jpg;anh3.jpg;anh4.jpg', 20)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (89, N'ASU03', N'Asus ROG Strix G16', 35000000, 33900000, N'Asus ROG Strix G16 mang đến phong cách gaming rực rỡ với dải đèn LED Aura Sync bao quanh thân máy và bàn phím RGB 4 vùng cực kỳ bắt mắt. Màn hình Nebula 165Hz sắc nét cùng hệ thống tản nhiệt 3 quạt tiên tiến giúp GPU RTX 4060 luôn hoạt động ở mức điện năng cao nhất cho FPS cực khủng trong game. Đây là cỗ máy chiến game thực thụ dành cho những ai yêu thích sự mạnh mẽ và hiệu ứng ánh sáng rực rỡ đậm chất Republic of Gamers trên bàn làm việc.', 1, CAST(N'2025-12-22' AS Date), 20, 0, N'91358_laptop_asus_gaming_rog_strix_g615jpr_s5107w_0010_layer_2.jpg;anh5.jpg;anh1.jpg', 21)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (90, N'ASU04', N'Asus Vivobook K3605', 19500000, 18500000, N'Asus Vivobook K3605 là mẫu laptop hoàn hảo cho sinh viên cần sự kết hợp giữa mỏng nhẹ văn phòng và sức mạnh đồ họa với card rời RTX 2050 tích hợp. Màn hình 16 inch độ phân giải cao mang lại không gian làm việc rộng rãi cùng lớp phủ kháng khuẩn Asus Antimicrobial Guard bảo vệ sức khỏe người dùng. Thiết kế bản lề 180 độ cùng bàn phím có độ nảy tốt giúp máy trở thành công cụ học tập hiệu quả và giải trí mượt mà sau những giờ lên lớp căng thẳng.', 1, CAST(N'2025-12-22' AS Date), 40, 0, N'92844_laptop_asus_gaming_vivobook_k3605vc_rp431w_0007_layer_2.jpg;anh2.jpg;anh3.jpg', 17)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (91, N'ASU05', N'Asus TUF Gaming A16', 28000000, 26500000, N'Asus TUF Gaming A16 Advantage Edition là mẫu laptop full cấu hình AMD với sự tối ưu hóa tuyệt đối giữa CPU Ryzen và GPU Radeon mang lại hiệu năng ổn định và nhiệt độ cực mát. Màn hình 16 inch 165Hz chuẩn màu 100% sRGB cho hình ảnh trung thực tuyệt vời lý tưởng cho các bạn trẻ yêu thích cả chơi game và sáng tạo nội dung số. Vỏ máy màu cát Sandstorm độc đáo mang lại sự khác biệt hoàn toàn so với các dòng máy gaming đen xám thông thường hiện nay.', 1, CAST(N'2025-12-22' AS Date), 18, 0, N'91631_laptop_asus_gaming_tuf_fx607vj_rl034w_0010_layer_2.jpg;anh4.jpg;anh5.jpg', 20)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (92, N'ASU06', N'Asus ROG Flow X16', 48000000, 45900000, N'Asus ROG Flow X16 là chiếc laptop gaming xoay gập 360 độ độc đáo nhất thế giới với màn hình Mini-LED siêu rực rỡ cho độ sáng lên tới 1100 nits. Máy hỗ trợ bút cảm ứng giúp bạn có thể vẽ trực tiếp lên màn hình như một chiếc bảng vẽ chuyên dụng cực kỳ tiện lợi cho giới nghệ sĩ đồ họa. Mặc dù mỏng nhẹ nhưng máy vẫn trang bị cấu hình cực khủng với RTX 4070 và khả năng kết nối với eGPU XG Mobile bên ngoài để tăng sức mạnh đồ họa lên tầm cao mới.', 1, CAST(N'2025-12-22' AS Date), 8, 0, N'90954_laptop_asus_gaming_rog_zephyrus_ga403wr_qs103ws_0011_layer_2.jpg;anh1.jpg;anh3.jpg', 21)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (93, N'ASU07', N'Asus Vivobook Go 15', 12500000, 11500000, N'Asus Vivobook Go 15 là mẫu laptop giá rẻ tốt nhất cho sinh viên kinh tế văn phòng với thiết kế mỏng nhẹ tinh tế và tông màu bạc thời trang. Máy sở hữu màn hình Full HD chống chói cùng bàn phím có cụm phím số hỗ trợ cực tốt cho việc nhập liệu số liệu trên Excel. Công nghệ sạc nhanh giúp nạp 60% pin chỉ trong vòng 49 phút vô cùng tiện lợi cho những ai hay phải mang máy ra ngoài làm việc tại quán cafe hay thư viện trường học mỗi ngày.', 1, CAST(N'2025-12-22' AS Date), 57, 6, N'92844_laptop_asus_gaming_vivobook_k3605vc_rp431w_0007_layer_2.jpg;anh4.jpg;anh5.jpg', 17)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (94, N'ASU08', N'Asus ROG Strix Scar 18', 85000000, 82000000, N'Asus ROG Strix Scar 18 là ông vua của dòng laptop gaming với kích thước màn hình khổng lồ 18 inch tần số quét 240Hz sắc nét đến từng chi tiết. Trái tim của máy là Intel Core i9-14900HX kết hợp cùng card đồ họa RTX 4090 mang lại sức mạnh không đối thủ chinh phục mọi tựa game ở độ phân giải 4K. Hệ thống đèn LED RGB rực rỡ bao quanh cùng tản nhiệt 3 quạt với keo tản nhiệt kim loại lỏng giúp máy luôn hoạt động ở trạng thái đỉnh cao nhất.', 1, CAST(N'2025-12-22' AS Date), 4, 0, N'91358_laptop_asus_gaming_rog_strix_g615jpr_s5107w_0010_layer_2.jpg;anh1.jpg;anh2.jpg', 21)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (95, N'ASU09', N'Asus Zenbook 14 OLED', 28500000, 26900000, N'Asus Zenbook 14 OLED là biểu tượng của sự sang trọng với vỏ nhôm gốm plasma bền bỉ và màn hình OLED 2.8K đẹp không tì vết. Máy được chứng nhận Intel Evo về tốc độ phản hồi nhanh và thời lượng pin sử dụng thực tế cực dài trên 10 tiếng đồng hồ. Hệ thống âm thanh Harman Kardon trong trẻo cùng bàn phím gõ êm ái mang lại trải nghiệm làm việc và giải trí cao cấp nhất cho giới doanh nhân và người dùng yêu thích cái đẹp hoàn mỹ.', 1, CAST(N'2025-12-22' AS Date), 25, 0, N'anh3.jpg;anh4.jpg;anh5.jpg', 21)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (96, N'ASU10', N'Asus ExpertBook B5', 23000000, 21500000, N'Asus ExpertBook B5 là dòng laptop doanh nghiệp siêu bền bỉ với trọng lượng nhẹ chỉ 1.2kg và tính năng bảo mật vân tay kết hợp camera hồng ngoại IR nhận diện khuôn mặt. Máy đạt chuẩn quân đội về độ bền va đập và chống nước nhẹ cho bàn phím giúp bảo vệ linh kiện tối đa trong môi trường làm việc khắc nghiệt. Đầy đủ các cổng kết nối từ HDMI đến LAN RJ45 mà không cần dùng đến hub chuyển đổi giúp công việc của bạn luôn diễn ra liền mạch.', 1, CAST(N'2025-12-22' AS Date), 30, 0, N'anh1.jpg;anh2.jpg;anh3.jpg', 17)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (97, N'ASU11', N'Asus TUF Dash F15', 24000000, 22500000, N'Asus TUF Dash F15 mang thiết kế gaming lai văn phòng với độ mỏng ấn tượng chỉ 19.9mm và màu trắng Moon White cực kỳ thanh lịch. Máy được trang bị card đồ họa RTX 30 Series hiệu năng cao cùng tản nhiệt chống bụi mới giúp duy trì độ sạch sẽ cho hệ thống bên trong. Đây là mẫu máy dành cho những người cần một chiếc laptop vừa đủ mạnh để giải trí vừa đủ lịch sự để mang đi gặp đối tác hoặc làm việc trong môi trường chuyên nghiệp.', 1, CAST(N'2025-12-22' AS Date), 20, 0, N'92299_laptop_asus_gaming_v16_v3607vh_rp024w_0011_layer_2.jpg;anh4.jpg;anh5.jpg', 20)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (98, N'ASU12', N'Asus ROG Zephyrus M16', 55000000, 52900000, N'Asus ROG Zephyrus M16 sở hữu màn hình Nebula HDR 16 inch tỷ lệ 16:10 mở rộng góc nhìn cùng độ sáng cực cao cho trải nghiệm hình ảnh tuyệt mỹ. Máy trang bị cấu hình khủng Core i9 và RTX 4070 giúp xử lý mượt mà các project phim ảnh nặng nề nhất. Hệ thống 6 loa tích hợp công nghệ khử tiếng ồn AI hai chiều mang lại chất lượng cuộc gọi và giải trí vô cùng trong trẻo chuyên nghiệp xứng tầm một chiếc máy multimedia cao cấp nhất hiện nay.', 1, CAST(N'2025-12-22' AS Date), 6, 0, N'90954_laptop_asus_gaming_rog_zephyrus_ga403wr_qs103ws_0011_layer_2.jpg;anh1.jpg;anh2.jpg', 21)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (99, N'ASU13', N'Asus Vivobook S 14 OLED', 21500000, 19990000, N'Asus Vivobook S 14 OLED nổi bật với thiết kế phím Enter họa tiết sọc vằn cá tính và vỏ kim loại nhiều màu sắc năng động. Màn hình OLED chuẩn màu điện ảnh cùng vi xử lý dòng H hiệu năng cao giúp máy xử lý tốt các tác vụ đồ họa 2D và chỉnh sửa ảnh nhẹ nhàng. Trọng lượng nhẹ cùng sạc nhanh qua cổng USB-C giúp chiếc máy này trở thành người bạn đồng hành không thể thiếu cho các bạn trẻ Gen Z đam mê sáng tạo nội dung.', 1, CAST(N'2025-12-22' AS Date), 35, 0, N'92844_laptop_asus_gaming_vivobook_k3605vc_rp431w_0007_layer_2.jpg;anh3.jpg;anh4.jpg', 17)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (100, N'ASU14', N'Asus TUF Gaming A15 2024', 24500000, 22900000, N'Asus TUF Gaming A15 phiên bản 2024 sở hữu chip Ryzen 7000 Series mới nhất mang lại khả năng tiết kiệm pin vượt trội so với các đối thủ cùng phân khúc. Máy trang bị card đồ họa RTX 4050 cùng màn hình 144Hz chuẩn màu sRGB giúp hình ảnh game trở nên sống động và mượt mà hơn. Độ bền đạt chuẩn quân đội cùng hệ thống tản nhiệt 2 quạt 84 cánh giúp máy giải nhiệt nhanh chóng bảo vệ tối ưu cho phần cứng bên trong khi sử dụng liên tục nhiều giờ.', 1, CAST(N'2025-12-22' AS Date), 28, 0, N'91631_laptop_asus_gaming_tuf_fx607vj_rl034w_0010_layer_2.jpg;anh5.jpg;anh1.jpg', 20)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (101, N'SP099', N'Dell300', 15000000, 12000000, N'<p>Sản phẩm chất lượng cao</p>', 1, CAST(N'2025-12-22' AS Date), 40, NULL, N'dell300-1.jpg;dell300-2.jpg;dell300-3.jpg', 12)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (102, N'SP05', N'AcerAspire77', 535353535, 4545454, N'<p>Sản phẩm hiện đại</p>', 1, CAST(N'2025-12-22' AS Date), 54, NULL, N'aceraspire77-1.jpg;aceraspire77-2.jpg;aceraspire77-3.jpg', 16)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (103, N'SP080', N'Oke', 9, 7, N'<p>Oke</p>', 1, CAST(N'2025-12-22' AS Date), 2, NULL, N'oke-1.jpg;oke-2.jpg;oke-3.jpg', 20)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (114, N'sp0054', N'msi gf233', 15000000, 14500000, N'<p>tốt</p>', NULL, CAST(N'2025-12-25' AS Date), 1000, NULL, N'msi-gf233-1-bd9f.jpg', NULL)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (115, N'sp0055', N'msi gf233', 15000000, 14500000, N'<p>tốt</p>', NULL, CAST(N'2025-12-25' AS Date), 1000, NULL, N'default.jpg', NULL)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (116, N'sp0055', N'msi gf233', 15000000, 14500000, NULL, NULL, CAST(N'2025-12-25' AS Date), 1000, NULL, N'default.jpg', NULL)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (117, N'sp0055', N'msi gf233', 12444444, 12345666, NULL, NULL, CAST(N'2025-12-25' AS Date), 122, NULL, N'default.jpg', NULL)
INSERT [dbo].[SANPHAM] ([ID_SP], [MaSP], [TenSP], [Gia], [GiaBan], [Mota], [Status_SP], [NgayTao], [SoLuong], [SoLuongBan], [Images_url], [ID_DM]) VALUES (118, N'sp0055', N'msi gf233', 12444444, 12345666, NULL, NULL, CAST(N'2025-12-25' AS Date), 122, NULL, N'default.jpg', NULL)
SET IDENTITY_INSERT [dbo].[SANPHAM] OFF
GO
ALTER TABLE [dbo].[DANHGIA]  WITH CHECK ADD  CONSTRAINT [fk5] FOREIGN KEY([ID_KH])
REFERENCES [dbo].[KHACHHANG] ([ID_KH])
GO
ALTER TABLE [dbo].[DANHGIA] CHECK CONSTRAINT [fk5]
GO
ALTER TABLE [dbo].[DANHGIA]  WITH CHECK ADD  CONSTRAINT [fk6] FOREIGN KEY([ID_SP])
REFERENCES [dbo].[SANPHAM] ([ID_SP])
GO
ALTER TABLE [dbo].[DANHGIA] CHECK CONSTRAINT [fk6]
GO
ALTER TABLE [dbo].[DONHANG]  WITH CHECK ADD  CONSTRAINT [fk7] FOREIGN KEY([ID_KH])
REFERENCES [dbo].[KHACHHANG] ([ID_KH])
GO
ALTER TABLE [dbo].[DONHANG] CHECK CONSTRAINT [fk7]
GO
ALTER TABLE [dbo].[DONHANG]  WITH CHECK ADD  CONSTRAINT [fk8] FOREIGN KEY([ID_KM])
REFERENCES [dbo].[KHUYENMAI] ([ID_KM])
GO
ALTER TABLE [dbo].[DONHANG] CHECK CONSTRAINT [fk8]
GO
ALTER TABLE [dbo].[DONHANG_SANPHAM]  WITH CHECK ADD  CONSTRAINT [fk10] FOREIGN KEY([ID_SP])
REFERENCES [dbo].[SANPHAM] ([ID_SP])
GO
ALTER TABLE [dbo].[DONHANG_SANPHAM] CHECK CONSTRAINT [fk10]
GO
ALTER TABLE [dbo].[DONHANG_SANPHAM]  WITH CHECK ADD  CONSTRAINT [fk9] FOREIGN KEY([ID_DH])
REFERENCES [dbo].[DONHANG] ([ID_DH])
GO
ALTER TABLE [dbo].[DONHANG_SANPHAM] CHECK CONSTRAINT [fk9]
GO
ALTER TABLE [dbo].[GIOHANG]  WITH CHECK ADD  CONSTRAINT [fk1] FOREIGN KEY([ID_KH])
REFERENCES [dbo].[KHACHHANG] ([ID_KH])
GO
ALTER TABLE [dbo].[GIOHANG] CHECK CONSTRAINT [fk1]
GO
ALTER TABLE [dbo].[GIOHANG_SANPHAM]  WITH CHECK ADD  CONSTRAINT [fk3] FOREIGN KEY([ID_GH])
REFERENCES [dbo].[GIOHANG] ([ID_GH])
GO
ALTER TABLE [dbo].[GIOHANG_SANPHAM] CHECK CONSTRAINT [fk3]
GO
ALTER TABLE [dbo].[GIOHANG_SANPHAM]  WITH CHECK ADD  CONSTRAINT [fk4] FOREIGN KEY([ID_SP])
REFERENCES [dbo].[SANPHAM] ([ID_SP])
GO
ALTER TABLE [dbo].[GIOHANG_SANPHAM] CHECK CONSTRAINT [fk4]
GO
ALTER TABLE [dbo].[SANPHAM]  WITH CHECK ADD  CONSTRAINT [fk2] FOREIGN KEY([ID_DM])
REFERENCES [dbo].[DANHMUC] ([ID_DM])
GO
ALTER TABLE [dbo].[SANPHAM] CHECK CONSTRAINT [fk2]
GO
USE [master]
GO
ALTER DATABASE [DARKTHESTORE] SET  READ_WRITE 
GO
