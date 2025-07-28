from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hiển thị menu help chính"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Cổ phiếu & ETF", callback_data="help_stock"),
            InlineKeyboardButton("📈 Thị trường", callback_data="help_market")
        ],
        [
            InlineKeyboardButton("💰 Quỹ đầu tư", callback_data="help_funds"),
            InlineKeyboardButton("📰 Tin tức", callback_data="help_news")
        ],
        [
            InlineKeyboardButton("🔍 Bộ lọc", callback_data="help_filter"),
            InlineKeyboardButton("🥇 Hàng hóa", callback_data="help_commodities")
        ],
        [
            InlineKeyboardButton("📋 Tất cả commands", callback_data="help_all")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    help_text = """
🤖 <b>STOCK BOT - USER GUIDE</b>

Welcome to Stock Bot! 🎉

📋 <b>BASIC COMMANDS:</b>
• <code>/start</code> - Start the bot
• <code>/help</code> - This help menu
• <code>/ta_technical</code> - Technical analysis indicators (see below)

💡 <b>Select a category below for details:</b>

📊 <b>Stocks & ETF</b> - Stock prices, info, charts
📈 <b>Market</b> - Indices, top stocks, sectors
💰 <b>Funds</b> - ETF, open funds, performance
📰 <b>News</b> - News, events, announcements
🔍 <b>Filter</b> - Stock screening
🥇 <b>Commodities</b> - Gold, metals, raw materials

<b>Technical Analysis:</b>
• <code>/ta_technical &lt;symbol&gt; [start_date] [end_date]</code>
  Returns key technical indicators (RSI, MACD, EMA, etc.) for the given stock symbol and date range.
  Example: <code>/ta_technical VNM 2023-01-01 2023-12-31</code>

🔗 <b>CONTACT:</b> @nhanhoang09
"""
    
    await update.message.reply_text(help_text, parse_mode='HTML', reply_markup=reply_markup)

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý callback cho help menu"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "help_stock":
        await show_stock_help(query)
    elif query.data == "help_market":
        await show_market_help(query)
    elif query.data == "help_funds":
        await show_funds_help(query)
    elif query.data == "help_news":
        await show_news_help(query)
    elif query.data == "help_filter":
        await show_filter_help(query)
    elif query.data == "help_commodities":
        await show_commodities_help(query)
    elif query.data == "help_all":
        await show_all_help(query)
    elif query.data == "help_back":
        await show_main_help(query)

async def show_main_help(query):
    """Hiển thị menu help chính cho callback"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Cổ phiếu & ETF", callback_data="help_stock"),
            InlineKeyboardButton("📈 Thị trường", callback_data="help_market")
        ],
        [
            InlineKeyboardButton("💰 Quỹ đầu tư", callback_data="help_funds"),
            InlineKeyboardButton("📰 Tin tức", callback_data="help_news")
        ],
        [
            InlineKeyboardButton("🔍 Bộ lọc", callback_data="help_filter"),
            InlineKeyboardButton("🥇 Hàng hóa", callback_data="help_commodities")
        ],
        [
            InlineKeyboardButton("📋 Tất cả commands", callback_data="help_all")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    help_text = """
🤖 <b>STOCK BOT - USER GUIDE</b>

Welcome to Stock Bot! 🎉

📋 <b>BASIC COMMANDS:</b>
• <code>/start</code> - Start the bot
• <code>/help</code> - This help menu
• <code>/ta_technical</code> - Technical analysis indicators (see below)

💡 <b>Select a category below for details:</b>

📊 <b>Stocks & ETF</b> - Stock prices, info, charts
📈 <b>Market</b> - Indices, top stocks, sectors
💰 <b>Funds</b> - ETF, open funds, performance
📰 <b>News</b> - News, events, announcements
🔍 <b>Filter</b> - Stock screening
🥇 <b>Commodities</b> - Gold, metals, raw materials

<b>Technical Analysis:</b>
• <code>/ta_technical &lt;symbol&gt; [start_date] [end_date]</code>
  Returns key technical indicators (RSI, MACD, EMA, etc.) for the given stock symbol and date range.
  Example: <code>/ta_technical VNM 2023-01-01 2023-12-31</code>

🔗 <b>CONTACT:</b> @nhanhoang09
"""
    
    await query.edit_message_text(help_text, parse_mode='HTML', reply_markup=reply_markup)

async def show_stock_help(query):
    """Hiển thị help cho cổ phiếu và ETF"""
    keyboard = [
        [InlineKeyboardButton("⬅️ Quay lại", callback_data="help_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
📊 <b>STOCKS & ETF</b>

🔹 <b>/stock &lt;symbol&gt;</b>
   Get current stock price
   Example: <code>/stock VNM</code>

🔹 <b>/stock info &lt;symbol&gt;</b>
   Full company info, financials, real-time trading, overview
   Example: <code>/stock info VNM</code>
   
   <b>Returned info includes:</b>
   • Basic info: Name, exchange, type, industry, website
   • Overview: Charter capital, shares, year, shareholders, employees, rating, short name, industry code
   • Financials: P/E, P/B, ROE, ROA, EPS, BVPS, Market Cap (if available)
   • Realtime trading: Price, volume, 1Y high/low

🔹 <b>/realtime &lt;symbol1&gt; &lt;symbol2&gt; ...</b>
   Real-time prices for multiple stocks
   Example: <code>/realtime VNM FPT VIC</code>

🔹 <b>/history &lt;symbol&gt; &lt;years&gt; [time_range]</b>
   Price history with chart and statistics
   
   <b>Usage:</b>
   • <code>/history VNM 2</code> - Last 2 years
   • <code>/history VNM 2 2021-2023</code> - From 2021-2023
   • <code>/history VNM 2 2021-01-01-2023-12-31</code> - Specific dates
   
   <b>Result:</b> Chart + Year/month stats + CSV

🔹 <b>/financial &lt;symbol&gt;</b>
   Financial ratios (P/E, ROE...)
   Example: <code>/financial VNM</code>

📊 <b>ETF:</b>

🔹 <b>/etf</b> - List ETF
🔹 <b>/etf &lt;symbol&gt;</b> - ETF price
🔹 <b>/etf info &lt;symbol&gt;</b> - ETF info
"""
    
    await query.edit_message_text(text, parse_mode='HTML', reply_markup=reply_markup)

async def show_market_help(query):
    """Hiển thị help cho thị trường"""
    keyboard = [
        [InlineKeyboardButton("⬅️ Quay lại", callback_data="help_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
📈 <b>THỊ TRƯỜNG & CHỈ SỐ</b>

🔹 <b>/market</b>
   VN-Index, HNX-Index và top cổ phiếu

🔹 <b>/top &lt;criteria&gt; [limit]</b>
   Top cổ phiếu theo tiêu chí:
   • <code>gainers</code> - Top tăng giá
   • <code>losers</code> - Top giảm giá
   • <code>volume</code> - Top khối lượng
   • <code>value</code> - Top giá trị giao dịch
   
   Ví dụ: <code>/top gainers 10</code>

🔹 <b>/sector &lt;tên_ngành&gt;</b>
   Tìm cổ phiếu theo ngành
   Ví dụ: <code>/sector ngân hàng</code>

🔹 <b>/index</b> - Chỉ số thị trường
🔹 <b>/index_detail &lt;tên_chỉ_số&gt;</b> - Chi tiết chỉ số
🔹 <b>/index_history &lt;tên_chỉ_số&gt; &lt;số_ngày&gt;</b> - Lịch sử chỉ số
🔹 <b>/index_compare &lt;chỉ_số1&gt; &lt;chỉ_số2&gt;</b> - So sánh chỉ số
🔹 <b>/index_sector</b> - Chỉ số ngành
"""
    
    await query.edit_message_text(text, parse_mode='HTML', reply_markup=reply_markup)

async def show_funds_help(query):
    """Hiển thị help cho quỹ đầu tư"""
    keyboard = [
        [InlineKeyboardButton("⬅️ Quay lại", callback_data="help_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
💰 <b>QUỸ ĐẦU TƯ (ETF & QUỸ MỞ)</b>

🔹 <b>/funds</b>
   Danh sách quỹ đầu tư

🔹 <b>/fund_detail &lt;mã_quỹ&gt;</b>
   Chi tiết quỹ đầu tư
   Ví dụ: <code>/fund_detail FUEVFVND</code>

🔹 <b>/fund_performance &lt;mã_quỹ&gt; [số_ngày]</b>
   Hiệu suất quỹ với biểu đồ
   Ví dụ: <code>/fund_performance FUEVFVND</code>

🔹 <b>/fund_compare &lt;quỹ1&gt; &lt;quỹ2&gt;</b>
   So sánh các quỹ đầu tư
   Ví dụ: <code>/fund_compare FUEVFVND E1VFVN30</code>

🔹 <b>/fund_sector</b>
   Quỹ đầu tư theo ngành

🔹 <b>/fund_ranking [số_ngày] [limit]</b>
   Xếp hạng quỹ theo hiệu suất
   Ví dụ: <code>/fund_ranking 30 10</code>
"""
    
    await query.edit_message_text(text, parse_mode='HTML', reply_markup=reply_markup)

async def show_news_help(query):
    """Hiển thị help cho tin tức"""
    keyboard = [
        [InlineKeyboardButton("⬅️ Quay lại", callback_data="help_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
📰 <b>TIN TỨC & SỰ KIỆN</b>

🔹 <b>/news</b>
   Tin tức thị trường mới nhất

🔹 <b>/news_stock &lt;mã_cổ_phiếu&gt;</b>
   Tin tức về cổ phiếu cụ thể
   Ví dụ: <code>/news_stock VNM</code>

🔹 <b>/market_news</b>
   Tin tức thị trường tổng hợp

🔹 <b>/events</b>
   Sự kiện thị trường chứng khoán

🔹 <b>/calendar [số_ngày]</b>
   Lịch sự kiện thị trường
   Ví dụ: <code>/calendar 7</code>

🔹 <b>/announcements &lt;mã_cổ_phiếu&gt; [limit]</b>
   Công bố thông tin doanh nghiệp
   Ví dụ: <code>/announcements VNM</code>
"""
    
    await query.edit_message_text(text, parse_mode='HTML', reply_markup=reply_markup)

async def show_filter_help(query):
    """Hiển thị help cho bộ lọc"""
    keyboard = [
        [InlineKeyboardButton("⬅️ Quay lại", callback_data="help_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
🔍 <b>BỘ LỌC CỔ PHIẾU</b>

🔹 <b>/filter_pe &lt;min_pe&gt; &lt;max_pe&gt; [limit]</b>
   Lọc theo P/E
   Ví dụ: <code>/filter_pe 5 15 20</code>

🔹 <b>/filter_roe &lt;min_roe&gt; &lt;max_roe&gt; [limit]</b>
   Lọc theo ROE (%)
   Ví dụ: <code>/filter_roe 15 30 20</code>

🔹 <b>/filter_market_cap &lt;min_cap&gt; &lt;max_cap&gt; [limit]</b>
   Lọc theo vốn hóa (tỷ VNĐ)
   Ví dụ: <code>/filter_market_cap 1000 10000 20</code>

🔹 <b>/filter_volume &lt;min_volume&gt; [limit]</b>
   Lọc theo khối lượng (cổ)
   Ví dụ: <code>/filter_volume 1000000 20</code>

🔹 <b>/filter_price &lt;min_price&gt; &lt;max_price&gt; [limit]</b>
   Lọc theo giá (VNĐ)
   Ví dụ: <code>/filter_price 10000 50000 20</code>

🔹 <b>/screener [tiêu_chí:giá_trị...] [limit]</b>
   Bộ lọc tổng hợp nhiều tiêu chí
   Ví dụ: <code>/screener pe_max:15 roe_min:20 20</code>
"""
    
    await query.edit_message_text(text, parse_mode='HTML', reply_markup=reply_markup)

async def show_commodities_help(query):
    """Hiển thị help cho hàng hóa"""
    keyboard = [
        [InlineKeyboardButton("⬅️ Quay lại", callback_data="help_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
🥇 <b>KIM LOẠI QUÝ & HÀNG HÓA</b>

🔹 <b>/gold</b>
   Thông tin giá vàng trong nước và thế giới

🔹 <b>/metals</b>
   Kim loại quý và nguyên liệu (thép, kim loại)

🔹 <b>/commodities</b>
   Hàng hóa và nguyên liệu cơ bản

💡 <b>Lưu ý:</b>
• Giá vàng và hàng hóa có thể có độ trễ
• Dữ liệu được cập nhật theo thời gian thực
• Chỉ mang tính chất tham khảo
"""
    
    await query.edit_message_text(text, parse_mode='HTML', reply_markup=reply_markup)

async def show_all_help(query):
    """Hiển thị tất cả commands (chia nhỏ)"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Cổ phiếu & ETF", callback_data="help_stock"),
            InlineKeyboardButton("📈 Thị trường", callback_data="help_market")
        ],
        [
            InlineKeyboardButton("💰 Quỹ đầu tư", callback_data="help_funds"),
            InlineKeyboardButton("📰 Tin tức", callback_data="help_news")
        ],
        [
            InlineKeyboardButton("🔍 Bộ lọc", callback_data="help_filter"),
            InlineKeyboardButton("🥇 Hàng hóa", callback_data="help_commodities")
        ],
        [InlineKeyboardButton("⬅️ Quay lại", callback_data="help_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
📋 <b>ALL COMMANDS</b>

💡 <b>Select a category below for details:</b>

📊 <b>Stocks & ETF</b> - Stock prices, info, charts
📈 <b>Market</b> - Indices, top stocks, sectors
💰 <b>Funds</b> - ETF, open funds, performance
📰 <b>News</b> - News, events, announcements
🔍 <b>Filter</b> - Stock screening
🥇 <b>Commodities</b> - Gold, metals, raw materials

<b>Technical Analysis:</b>
• <code>/ta_technical &lt;symbol&gt; [start_date] [end_date]</code>
  Returns key technical indicators (RSI, MACD, EMA, etc.) for the given stock symbol and date range.
  Example: <code>/ta_technical VNM 2023-01-01 2023-12-31</code>

🔗 <b>CONTACT:</b> @nhanhoang09
"""
    
    await query.edit_message_text(text, parse_mode='HTML', reply_markup=reply_markup) 