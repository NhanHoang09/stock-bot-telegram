# 📊 Stock Bot System Architecture Diagram

## 🎯 Mô tả

File `system-architecture.drawio` chứa diagram chi tiết về kiến trúc hệ thống Stock Bot, mô tả đầy đủ các thành phần, luồng dữ liệu và tính năng của bot.

## 🔗 Cách sử dụng

### 1. Mở với Draw.io

- Truy cập [draw.io](https://app.diagrams.net/)
- Chọn **File** → **Open from** → **Device**
- Chọn file `system-architecture.drawio`

### 2. Mở với VS Code

- Cài extension **Draw.io Integration**
- Mở file `.drawio` trong VS Code
- Chỉnh sửa trực tiếp trong editor

## 🏗️ Kiến trúc Hệ thống

### 📱 User Interface Layer

- **👤 User**: Người dùng cuối
- **📱 Telegram Platform**: Telegram Bot API, Message Handling

### 🤖 Application Layer

- **🤖 Stock Bot Application**: Core bot logic
- **📋 Commands Module**: Các lệnh bot (/company, /stock, /financial)
- **🛠️ Utils Module**: Loading animation, formatters, helpers

### 🗄️ Data Layer

- **🗄️ Database**: SQLite với user records và stock history
- **📊 VNStock API**: External API cho dữ liệu chứng khoán

### 🐳 Infrastructure Layer

- **🐳 Docker Container**: Containerized deployment

## 📡 Data Sources

### 🏢 Các Sàn Giao Dịch

1. **HOSE** (Ho Chi Minh Stock Exchange)

   - VNM, VIC, VHM
   - Large-cap stocks

2. **HNX** (Hanoi Stock Exchange)

   - SHB, VND, SHS
   - Mid-cap stocks

3. **UPCOM** (Unlisted Public Company Market)

   - Small-cap stocks
   - Growth companies

4. **VCI** (Vietcombank Securities)
   - Real-time data
   - Market depth

## ✨ Bot Features

### 📊 Company Information (`/company`)

- Thông tin cơ bản công ty
- Dữ liệu tổng quan
- Chỉ số tài chính cơ bản
- Thông tin giao dịch hiện tại

### 💹 Stock Price (`/stock`)

- Giá cổ phiếu real-time
- Thay đổi giá và phần trăm
- Khối lượng giao dịch
- Dữ liệu lịch sử

### 💰 Financial Data (`/financial`)

- Chỉ tiêu định giá (P/E, P/B, ROE, ROA)
- Báo cáo kết quả kinh doanh
- Bảng cân đối kế toán
- Báo cáo lưu chuyển tiền tệ

### 🎨 Loading Animation

- Spinner emoji động
- Animation theo chủ đề
- Real-time updates
- Progress feedback

## 🔄 Data Flow

### 1. User Request Flow

```
User → Telegram Platform → Stock Bot → Commands Module
```

### 2. Data Retrieval Flow

```
Commands Module → VNStock API → Data Sources (HOSE/HNX/UPCOM/VCI)
```

### 3. Data Storage Flow

```
Stock Bot → Database (User Records, Stock History)
```

### 4. Response Flow

```
Database/VNStock API → Utils Module → Stock Bot → Telegram → User
```

## 🛠️ Technical Stack

### 🐍 Backend

- **Python 3.8+**: Core programming language
- **python-telegram-bot**: Telegram Bot API wrapper
- **vnstock**: Vietnamese stock market data library
- **SQLAlchemy**: ORM for database operations

### 🗄️ Database

- **SQLite**: Lightweight database
- **User Records**: User information and preferences
- **Stock Price History**: Historical price data
- **Transaction Logs**: Bot usage logs

### 🐳 Deployment

- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Environment Isolation**: Consistent deployment

## 📈 Performance Metrics

### ⚡ Performance

- **Response Time**: < 3 seconds
- **Real-time Data**: Live market updates
- **Stock Coverage**: 1000+ symbols
- **Animation**: Smooth loading experience

### 🔄 Scalability

- **Containerized**: Easy scaling
- **Modular Design**: Extensible architecture
- **API Integration**: External data sources
- **Error Handling**: Robust error management

## 🎨 Visual Elements

### 🎨 Color Coding

- **🔵 Blue**: Data flow arrows
- **🟢 Green**: Data sources and external APIs
- **🟡 Yellow**: Core application components
- **🟣 Purple**: User interface elements
- **🔴 Red**: Database and storage

### 📊 Diagram Sections

1. **System Architecture**: Main components and connections
2. **Data Sources**: External market data providers
3. **Bot Features**: Available commands and capabilities
4. **Technical Stack**: Technologies and tools used
5. **Performance Metrics**: System performance indicators

## 🔧 Customization

### Thêm Components

1. Mở file trong draw.io
2. Thêm shapes từ library
3. Kết nối với arrows
4. Cập nhật colors và styles

### Chỉnh sửa Data Flow

1. Thêm/move arrows
2. Cập nhật labels
3. Thay đổi colors
4. Thêm annotations

### Export Options

- **PNG**: High-quality images
- **PDF**: Document format
- **SVG**: Scalable vector graphics
- **HTML**: Web format

## 📋 Maintenance

### Cập nhật Diagram

- Thêm tính năng mới
- Cập nhật data sources
- Thay đổi architecture
- Cải thiện performance

### Version Control

- Commit changes to git
- Tag versions
- Document updates
- Review changes

---

## 🎯 Kết luận

Diagram này cung cấp cái nhìn tổng quan về:

- **Kiến trúc hệ thống** Stock Bot
- **Luồng dữ liệu** từ user đến data sources
- **Tính năng** và capabilities của bot
- **Công nghệ** và tools được sử dụng
- **Performance** và scalability metrics

**📊 Diagram này giúp hiểu rõ cách hệ thống hoạt động và dễ dàng mở rộng trong tương lai!**
