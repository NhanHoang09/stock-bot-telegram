# 📊 Stock Bot Flow Chart - Chi Tiết Commands & VNStock Classes

## 🎯 Mô tả

File `stock-bot-flowchart.drawio` chứa flow chart chi tiết về cách hoạt động của Stock Bot, bao gồm:

- **Flow chart rõ ràng** từ user input đến response
- **Liệt kê đầy đủ commands** và cách xử lý
- **Chi tiết VNStock classes** được sử dụng cho từng command
- **Bảng mapping** command ↔ VNStock class ↔ Methods ↔ Data

## 🔄 Flow Chart Overview

### 📱 User Journey:

```
START → User Input → Command Parser → Command Router → Specific Command → Loading → VNStock Class → Data Processing → Database Storage → Format Response → Send Response → END
```

### 🎨 Color Coding:

- **🟢 Green**: Start/End points, VNStock classes
- **🟣 Purple**: User interaction
- **🟡 Yellow**: Processing logic, Response formatting
- **🔵 Blue**: Decision points, Data processing
- **🔴 Red**: Commands, Database
- **🟠 Orange**: Loading animation

## 📋 Commands & VNStock Classes Mapping

### 1. `/company <symbol>` Command

#### **VNStock Class: `Company`**

```python
from vnstock import Company
company = Company(symbol=symbol)
```

#### **Methods Used:**

- `company.overview()` - Thông tin tổng quan công ty
- `company.financial_ratio()` - Chỉ số tài chính cơ bản
- `company.balance_sheet()` - Bảng cân đối kế toán

#### **Data Retrieved:**

- **Basic company info**: Tên, địa chỉ, điện thoại, website
- **Financial overview**: Vốn điều lệ, số cổ phiếu, mã số
- **Trading data**: Giá hiện tại, thay đổi, khối lượng
- **Company ratios**: Các chỉ số tài chính cơ bản

#### **Output Format:**

- Company name & basic information
- Financial ratios và overview
- Current trading data
- Formatted with emojis và HTML

---

### 2. `/stock <symbol>` Command

#### **VNStock Class: `Trading`**

```python
from vnstock import Trading
trading = Trading(source='VCI')
```

#### **Methods Used:**

- `trading.price_board([symbol])` - Giá cổ phiếu real-time
- `trading.intraday_data(symbol)` - Dữ liệu trong ngày
- `trading.historical_data(symbol)` - Dữ liệu lịch sử

#### **Data Retrieved:**

- **Current stock price**: Giá hiện tại
- **Price change**: Thay đổi giá và phần trăm
- **Trading volume**: Khối lượng giao dịch
- **High/Low prices**: Giá cao nhất/thấp nhất

#### **Output Format:**

- Current price display với currency formatting
- Price change indicator (tăng/giảm)
- Volume information
- High/Low price data

---

### 3. `/financial <symbol>` Command

#### **VNStock Class: `Finance`**

```python
from vnstock import Finance
finance = Finance(source='vci', symbol=symbol)
```

#### **Methods Used:**

- `finance.ratio()` - Chỉ tiêu định giá (P/E, P/B, ROE, ROA)
- `finance.income_statement()` - Báo cáo kết quả kinh doanh
- `finance.balance_sheet()` - Bảng cân đối kế toán
- `finance.cash_flow()` - Báo cáo lưu chuyển tiền tệ

#### **Data Retrieved:**

- **P/E, P/B, ROE, ROA ratios**: Chỉ tiêu định giá
- **Revenue & profit data**: Doanh thu và lợi nhuận
- **Assets & liabilities**: Tài sản và nợ phải trả
- **Cash flow statements**: Lưu chuyển tiền tệ

#### **Output Format:**

- Financial ratios table
- Income statement summary
- Balance sheet overview
- Cash flow highlights

## 🔄 Detailed Flow Process

### **Step 1: User Input**

```
User sends: /company VNM
/stock VNM
/financial VNM
```

### **Step 2: Command Parser**

- Extract command type (`company`, `stock`, `financial`)
- Extract symbol (`VNM`)
- Validate input format

### **Step 3: Command Router**

- Route to appropriate handler based on command type
- Three branches: Company, Stock, Financial

### **Step 4: Loading Animation**

- Show spinner animation with themed emojis
- Update progress messages
- Provide user feedback

### **Step 5: VNStock API Call**

- **Company Command**: Use `Company` class
- **Stock Command**: Use `Trading` class
- **Financial Command**: Use `Finance` class

### **Step 6: Data Processing**

- Parse raw data from VNStock API
- Extract relevant information
- Handle missing data gracefully
- Format numbers and currencies

### **Step 7: Database Storage**

- Store user interaction logs
- Save stock price history (for stock command)
- Record transaction data

### **Step 8: Response Formatting**

- Apply HTML formatting
- Add emoji icons
- Format currency values
- Structure response layout

### **Step 9: Send Response**

- Send formatted response via Telegram Bot API
- Handle delivery confirmation

## 📊 Data Flow Diagram

### **Company Command Flow:**

```
User → Parser → Router → Company Command → Loading → Company Class → Process Data → Database → Format → Send
```

### **Stock Command Flow:**

```
User → Parser → Router → Stock Command → Loading → Trading Class → Process Data → Database → Format → Send
```

### **Financial Command Flow:**

```
User → Parser → Router → Financial Command → Loading → Finance Class → Process Data → Database → Format → Send
```

## 🛠️ Technical Implementation

### **Command Handler Structure:**

```python
# commands/stock/company.py
async def company_command(update, context):
    symbol = context.args[0].upper()
    loading_msg = await show_loading(update, context)

    try:
        from vnstock import Company
        company = Company(symbol=symbol)

        # Get data using Company class methods
        overview = company.overview()
        financial_ratio = company.financial_ratio()

        # Process and format data
        response = format_company_data(overview, financial_ratio)

        await finish_loading(loading_msg, response)
    except Exception as e:
        await finish_loading_with_error(loading_msg, str(e))
```

### **VNStock Integration:**

```python
# utils/stock_info.py
def get_company_info(symbol):
    company = Company(symbol=symbol)
    return {
        'overview': company.overview(),
        'financial_ratio': company.financial_ratio(),
        'balance_sheet': company.balance_sheet()
    }

def get_stock_price(symbol):
    trading = Trading(source='VCI')
    return trading.price_board([symbol])

def get_financial_data(symbol):
    finance = Finance(source='vci', symbol=symbol)
    return {
        'ratio': finance.ratio(),
        'income': finance.income_statement(),
        'balance': finance.balance_sheet(),
        'cashflow': finance.cash_flow()
    }
```

## 📈 Performance Considerations

### **Response Time Optimization:**

- **Parallel API calls** where possible
- **Caching** frequently requested data
- **Async processing** for non-blocking operations
- **Error handling** with fallback data

### **Data Quality:**

- **Validation** of API responses
- **Fallback values** for missing data
- **Error messages** for invalid symbols
- **Rate limiting** to respect API limits

## 🔧 Customization Options

### **Adding New Commands:**

1. Create new command file in `commands/stock/`
2. Import appropriate VNStock class
3. Implement data processing logic
4. Add to command router
5. Update flow chart

### **Extending VNStock Usage:**

- Add more methods from existing classes
- Import additional VNStock classes
- Combine data from multiple sources
- Create custom data aggregators

## 📋 Command Summary Table

| Command      | VNStock Class | Primary Methods                    | Data Type      | Response Format               |
| ------------ | ------------- | ---------------------------------- | -------------- | ----------------------------- |
| `/company`   | `Company`     | `overview()`, `financial_ratio()`  | Company Info   | Company details with ratios   |
| `/stock`     | `Trading`     | `price_board()`, `intraday_data()` | Price Data     | Current price with change     |
| `/financial` | `Finance`     | `ratio()`, `income_statement()`    | Financial Data | Financial ratios & statements |

## 🎯 Benefits of This Flow Chart

### **Clarity:**

- **Visual representation** of data flow
- **Clear separation** of concerns
- **Easy to understand** command routing
- **Detailed mapping** of VNStock classes

### **Maintainability:**

- **Modular design** for easy updates
- **Clear dependencies** between components
- **Documented data flow** for debugging
- **Scalable architecture** for new features

### **Development:**

- **Quick reference** for developers
- **Onboarding guide** for new team members
- **Troubleshooting guide** for issues
- **Architecture documentation** for stakeholders

---

## 🎉 Kết luận

Flow chart này cung cấp:

- **Cái nhìn tổng quan** về cách bot hoạt động
- **Chi tiết mapping** giữa commands và VNStock classes
- **Hướng dẫn phát triển** cho tính năng mới
- **Documentation** cho maintenance và debugging

**📊 Flow chart này giúp hiểu rõ cách mỗi command sử dụng VNStock classes và xử lý dữ liệu!**
