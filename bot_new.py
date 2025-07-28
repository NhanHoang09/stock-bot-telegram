import os
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
import pandas as pd
import pandas_ta as pta
# from vnstock import stock_historical_data  # Bản vnstock hiện tại không hỗ trợ hàm này, hãy dùng class Vnstock nếu cần lấy dữ liệu lịch sử

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TG_TOKEN')

# Import commands from modules
from commands.basic.start import start
from commands.basic.help import help, help_callback
from commands.stock.stock import stock
from commands.stock.etf import etf
from commands.stock.history import history
from commands.stock.realtime import realtime
from commands.stock.financial import financial
# from commands.stock.company import company  # Removed: merged into /stock info
from commands.market.market import market
from commands.market.top import top
from commands.market.sector import sector
from commands.market.index import index, index_detail, index_history, index_compare, index_sector
from commands.funds.funds import funds, fund_detail, fund_performance, fund_compare, fund_sector, fund_ranking
from commands.news.news import news, news_stock, market_news, events, calendar, announcements
from commands.filter.filter import filter_pe, filter_roe, filter_market_cap, filter_volume, filter_price, filter_sector, screener
from commands.analysis.commodities import gold, metals, commodities
from commands.analysis.technical_analysis import get_technical_summary, ta_technical

def main():
    """Khởi tạo và chạy bot"""
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Basic commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    
    # Help callback handler
    app.add_handler(CallbackQueryHandler(help_callback, pattern="^help_"))
    
    # Stock commands
    app.add_handler(CommandHandler("stock", stock))
    app.add_handler(CommandHandler("etf", etf))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("realtime", realtime))
    app.add_handler(CommandHandler("financial", financial))
    
    # Market commands
    app.add_handler(CommandHandler("market", market))
    app.add_handler(CommandHandler("top", top))
    app.add_handler(CommandHandler("sector", sector))
    
    # Index commands
    app.add_handler(CommandHandler("index", index))
    app.add_handler(CommandHandler("index_detail", index_detail))
    app.add_handler(CommandHandler("index_history", index_history))
    app.add_handler(CommandHandler("index_compare", index_compare))
    app.add_handler(CommandHandler("index_sector", index_sector))
    
    # Fund commands
    app.add_handler(CommandHandler("funds", funds))
    app.add_handler(CommandHandler("fund_detail", fund_detail))
    app.add_handler(CommandHandler("fund_performance", fund_performance))
    app.add_handler(CommandHandler("fund_compare", fund_compare))
    app.add_handler(CommandHandler("fund_sector", fund_sector))
    app.add_handler(CommandHandler("fund_ranking", fund_ranking))
    
    # News commands
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("news_stock", news_stock))
    app.add_handler(CommandHandler("market_news", market_news))
    app.add_handler(CommandHandler("events", events))
    app.add_handler(CommandHandler("calendar", calendar))
    app.add_handler(CommandHandler("announcements", announcements))
    
    # Filter commands
    app.add_handler(CommandHandler("filter_pe", filter_pe))
    app.add_handler(CommandHandler("filter_roe", filter_roe))
    app.add_handler(CommandHandler("filter_market_cap", filter_market_cap))
    app.add_handler(CommandHandler("filter_volume", filter_volume))
    app.add_handler(CommandHandler("filter_price", filter_price))
    app.add_handler(CommandHandler("filter_sector", filter_sector))
    app.add_handler(CommandHandler("screener", screener))
    
    # Commodities commands
    app.add_handler(CommandHandler("gold", gold))
    app.add_handler(CommandHandler("metals", metals))
    app.add_handler(CommandHandler("commodities", commodities))
    # Technical analysis command
    app.add_handler(CommandHandler("ta_technical", ta_technical))
    
    print("🤖 Bot đang khởi động...")
    print("📊 Stock Bot với 38 commands đã sẵn sàng!")
    print("🔗 Liên hệ: @nhanhoang09")
    
    app.run_polling()

if __name__ == "__main__":
    main() 