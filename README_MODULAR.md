# 📊 Stock Bot - Cấu Trúc Modular

## 🎯 Tổng Quan

Bot đã được tái cấu trúc từ file `bot.py` dài 2800+ dòng thành cấu trúc modular dễ maintain và mở rộng.

## 📁 Cấu Trúc Thư Mục

```
stock-bot/
├── bot.py                 # File bot cũ (2800+ dòng)
├── bot_new.py            # File bot mới (modular)
├── split_commands.py     # Script tách commands
├── commands/             # Package chứa tất cả commands
│   ├── __init__.py
│   ├── basic/           # Commands cơ bản
│   │   ├── __init__.py
│   │   ├── start.py     # /start command
│   │   └── help.py      # /help command
│   ├── stock/           # Commands cổ phiếu
│   │   ├── __init__.py
│   │   ├── stock.py     # /stock command
│   │   ├── etf.py       # /etf command
│   │   ├── history.py   # /history command
│   │   ├── realtime.py  # /realtime command
│   │   ├── financial.py # /financial command
│   │   └── company.py   # /company command
│   ├── market/          # Commands thị trường
│   │   ├── __init__.py
│   │   ├── market.py    # /market command
│   │   ├── top.py       # /top command
│   │   ├── sector.py    # /sector command
│   │   └── index.py     # /index commands
│   ├── funds/           # Commands quỹ đầu tư
│   │   ├── __init__.py
│   │   └── funds.py     # /funds commands
│   ├── news/            # Commands tin tức
│   │   ├── __init__.py
│   │   └── news.py      # /news commands
│   ├── filter/          # Commands bộ lọc
│   │   ├── __init__.py
│   │   └── filter.py    # /filter commands
│   └── analysis/        # Commands phân tích
│       ├── __init__.py
│       └── commodities.py # /commodities commands
├── utils/               # Package tiện ích
│   ├── __init__.py
│   ├── formatters.py    # Hàm format dữ liệu
│   └── stock_info.py    # Hàm lấy thông tin cổ phiếu
└── requirements.txt
```

## 🚀 Cách Sử Dụng

### 1. Chạy Bot Cũ (bot.py)

```bash
python bot.py
```

### 2. Chạy Bot Mới (modular)

```bash
python bot_new.py
```

### 3. Tách Commands Từ File Cũ

```bash
python split_commands.py
```

## 📊 Phân Loại Commands

### 🔹 Basic Commands (2 commands)

- `/start` - Khởi tạo bot
- `/help` - Hướng dẫn sử dụng

### 🔹 Stock Commands (6 commands)

- `/stock` - Giá cổ phiếu
- `/etf` - ETF
- `/history` - Lịch sử giá
- `/realtime` - Giá thời gian thực
- `/financial` - Chỉ số tài chính
- `/company` - Thông tin doanh nghiệp

### 🔹 Market Commands (5 commands)

- `/market` - Thị trường
- `/top` - Top cổ phiếu
- `/sector` - Ngành nghề
- `/index` - Chỉ số thị trường
- `/index_detail` - Chi tiết chỉ số
- `/index_history` - Lịch sử chỉ số
- `/index_compare` - So sánh chỉ số
- `/index_sector` - Chỉ số ngành

### 🔹 Fund Commands (6 commands)

- `/funds` - Danh sách quỹ
- `/fund_detail` - Chi tiết quỹ
- `/fund_performance` - Hiệu suất quỹ
- `/fund_compare` - So sánh quỹ
- `/fund_sector` - Quỹ theo ngành
- `/fund_ranking` - Xếp hạng quỹ

### 🔹 News Commands (6 commands)

- `/news` - Tin tức thị trường
- `/news_stock` - Tin tức cổ phiếu
- `/market_news` - Tin tức tổng hợp
- `/events` - Sự kiện thị trường
- `/calendar` - Lịch sự kiện
- `/announcements` - Công bố thông tin

### 🔹 Filter Commands (7 commands)

- `/filter_pe` - Lọc theo P/E
- `/filter_roe` - Lọc theo ROE
- `/filter_market_cap` - Lọc theo vốn hóa
- `/filter_volume` - Lọc theo khối lượng
- `/filter_price` - Lọc theo giá
- `/filter_sector` - Lọc theo ngành
- `/screener` - Bộ lọc tổng hợp

### 🔹 Analysis Commands (3 commands)

- `/gold` - Giá vàng
- `/metals` - Kim loại quý
- `/commodities` - Hàng hóa

## 🛠️ Lợi Ích Cấu Trúc Modular

### ✅ Dễ Maintain

- Mỗi command trong file riêng
- Dễ tìm và sửa lỗi
- Code ngắn gọn, dễ đọc

### ✅ Dễ Mở Rộng

- Thêm command mới dễ dàng
- Không ảnh hưởng code cũ
- Tổ chức theo chức năng

### ✅ Tái Sử Dụng

- Utils functions dùng chung
- Import/export dễ dàng
- Giảm duplicate code

### ✅ Team Development

- Nhiều người làm cùng lúc
- Conflict ít xảy ra
- Code review dễ dàng

## 📝 Cách Thêm Command Mới

### 1. Tạo File Module

```python
# commands/new_category/new_command.py
from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd

async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mô tả command mới"""
    # Code implementation
    pass
```

### 2. Import Vào bot_new.py

```python
from commands.new_category.new_command import new_command

# Trong main()
app.add_handler(CommandHandler("new_command", new_command))
```

### 3. Thêm Vào Help

Cập nhật file `commands/basic/help.py`

## 🔧 Migration Guide

### Từ Bot Cũ Sang Bot Mới

1. Backup file `bot.py` cũ
2. Chạy `python split_commands.py`
3. Test bot mới: `python bot_new.py`
4. Nếu OK, đổi tên `bot_new.py` thành `bot.py`

### Rollback

```bash
# Nếu có vấn đề, quay lại bot cũ
mv bot.py bot_new.py
mv bot.py.backup bot.py
```

## 📊 Thống Kê

- **File cũ**: 1 file, 2800+ dòng
- **File mới**: 15+ files, 50-200 dòng/file
- **Commands**: 38 commands
- **Modules**: 8 categories
- **Utils**: 2 helper modules

## 🎯 Kết Luận

Cấu trúc modular giúp:

- ✅ Code dễ đọc và maintain
- ✅ Dễ dàng thêm tính năng mới
- ✅ Team development hiệu quả
- ✅ Giảm bugs và conflicts
- ✅ Tái sử dụng code tốt hơn

---

**🔗 Liên hệ**: @nhanhoang09
