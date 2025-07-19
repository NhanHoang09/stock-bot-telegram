# 📈 Stock Bot - Telegram Bot cho Thị trường Chứng khoán Việt Nam

## 🎯 Mô tả

Stock Bot là một Telegram Bot được xây dựng bằng Python, cung cấp thông tin chi tiết về thị trường chứng khoán Việt Nam. Bot sử dụng thư viện `vnstock` để lấy dữ liệu từ các sàn giao dịch và cung cấp thông tin về giá cổ phiếu, thông tin công ty, và chỉ số tài chính.

## ✨ Tính năng chính

### 📊 Thông tin Công ty (`/company <mã>`)

- Thông tin cơ bản về công ty
- Thông tin tổng quan (vốn điều lệ, số cổ phiếu)
- Chỉ số tài chính cơ bản
- Thông tin giao dịch hiện tại

### 💹 Giá Cổ phiếu (`/stock <mã>`)

- Giá hiện tại của cổ phiếu
- Thông tin giao dịch chi tiết
- Lưu trữ lịch sử giá vào database

### 💰 Chỉ số Tài chính (`/financial <mã>`)

- Chỉ tiêu định giá (P/E, P/B, ROE, ROA)
- Báo cáo kết quả kinh doanh
- Bảng cân đối kế toán
- Báo cáo lưu chuyển tiền tệ

### 🎨 Loading Animation

- Hiệu ứng loading động với spinner emoji
- Animation theo chủ đề (công ty, cổ phiếu, tiền tệ)
- Phản hồi trực quan cho người dùng

## 🛠️ Công nghệ sử dụng

- **Python 3.8+**
- **python-telegram-bot** - Telegram Bot API
- **vnstock** - Thư viện dữ liệu chứng khoán Việt Nam
- **SQLAlchemy** - ORM cho database
- **Docker** - Containerization
- **Docker Compose** - Orchestration

## 📁 Cấu trúc Project

```
stock-bot/
├── commands/              # Các lệnh bot
│   └── stock/
│       ├── company.py     # Lệnh /company
│       ├── stock.py       # Lệnh /stock
│       └── financial.py   # Lệnh /financial
├── utils/                 # Tiện ích
│   ├── loading.py         # Loading animation
│   ├── formatters.py      # Format dữ liệu
│   └── stock_info.py      # Thông tin cổ phiếu
├── migrations/            # Database migrations
├── bot_new.py            # Bot launcher chính
├── run.py                # Entry point
├── requirements.txt      # Dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker orchestration
└── README.md           # Documentation
```

## 🚀 Cài đặt và Chạy

### 1. Clone Repository

```bash
git clone <repository-url>
cd stock-bot
```

### 2. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình Environment

```bash
cp .env.example .env
# Chỉnh sửa .env với token bot của bạn
```

### 4. Chạy với Docker (Khuyến nghị)

```bash
docker-compose up -d
```

### 5. Chạy trực tiếp

```bash
python run.py
```

## 📱 Sử dụng Bot

### Lệnh cơ bản:

- `/company VNM` - Thông tin công ty VNM
- `/stock VNM` - Giá cổ phiếu VNM
- `/financial VNM` - Chỉ số tài chính VNM

### Ví dụ sử dụng:

```
/company VNM
🏢 Thông tin doanh nghiệp VNM:
📊 Thông tin cơ bản:
🏢 Tên: Công ty Cổ phần Sữa Việt Nam
📍 Địa chỉ: 184 Nguyễn Thị Minh Khai, Quận 3, TP.HCM
📞 Điện thoại: 028-3930-9919
🌐 Website: www.vinamilk.com.vn
```

## 🔧 Cấu hình

### Environment Variables (.env):

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
DATABASE_URL=sqlite:///users.db
```

### Docker Configuration:

- **Port:** 8080
- **Database:** SQLite
- **Volume:** ./data:/app/data

## 📊 Database Schema

### Users Table:

- `id` - User ID
- `username` - Telegram username
- `first_name` - First name
- `last_name` - Last name
- `created_at` - Registration date

### Stock Prices Table:

- `id` - Primary key
- `symbol` - Stock symbol
- `price` - Current price
- `timestamp` - Price timestamp

## 🎨 Loading Animation

Bot sử dụng hệ thống loading animation với:

- **Spinner emoji:** ⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏
- **Themed animations:** Company 🏢, Stock 📈, Money 💰
- **Real-time updates:** Cập nhật từng bước xử lý

## 🤝 Đóng góp

1. Fork project
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

Project này được phân phối dưới MIT License. Xem file `LICENSE` để biết thêm chi tiết.

## 📞 Liên hệ

- **Email:** [your-email@example.com]
- **Telegram:** [@your-telegram]
- **GitHub:** [your-github-profile]

## 🙏 Cảm ơn

- [vnstock](https://github.com/thinh-vu/vnstock) - Thư viện dữ liệu chứng khoán Việt Nam
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [Docker](https://www.docker.com/) - Containerization platform

---

⭐ **Nếu project này hữu ích, hãy cho một star!** ⭐
