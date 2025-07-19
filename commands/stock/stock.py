import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from utils.formatters import format_vnd
from utils.stock_info import get_full_stock_info
from utils.loading import (
    show_animated_loading, 
    update_loading_with_stock_animation, 
    update_loading_with_money_animation,
    finish_loading, 
    finish_loading_with_error
)

# Import database models
try:
    from entities.coin_price.entity import StockPrice
    from entities.index import SessionLocal
except ImportError:
    # Fallback nếu không có database
    StockPrice = None
    SessionLocal = None

async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Vui lòng nhập lệnh đúng: /stock <symbol> hoặc /stock info <symbol>")
        return
    
    if context.args[0].lower() == "info" and len(context.args) > 1:
        symbol = context.args[1].upper()
        
        # Hiển thị loading động
        loading_msg = await show_animated_loading(update, context, f"Đang tìm thông tin chi tiết cho {symbol}...")
        
        try:
            info = await get_full_stock_info(symbol, debug_raw=True, update=update)
            if info:
                await finish_loading(loading_msg, info)
            else:
                await finish_loading_with_error(loading_msg, "Không tìm thấy thông tin công ty cho mã này.")
        except Exception as e:
            await finish_loading_with_error(loading_msg, f"Có lỗi xảy ra: {e}")
        return
    
    symbol = context.args[0].upper()
    
    # Hiển thị loading động
    loading_msg = await show_animated_loading(update, context, f"Đang tìm giá cổ phiếu {symbol}...")
    
    try:
        from vnstock import Trading
        
        # Cập nhật loading với animation cổ phiếu
        await update_loading_with_stock_animation(loading_msg, f"Đang lấy dữ liệu từ sàn giao dịch...", 1)
        
        prices = Trading(source='VCI').price_board([symbol])
        if prices.empty:
            await finish_loading_with_error(loading_msg, f"Không tìm thấy mã chứng khoán {symbol}")
            return
        
        # Cập nhật loading với animation tiền tệ
        await update_loading_with_money_animation(loading_msg, f"Đang lưu dữ liệu...", 2)
        
        price = float(prices.iloc[0][('match', 'match_price')])
        formatted_price = format_vnd(price)
        reply = f"💹 Giá hiện tại của <b>{symbol}</b>: <b>{formatted_price}₫</b> 🇻🇳"
        
        # Lưu vào database nếu có
        if StockPrice and SessionLocal:
            session = SessionLocal()
            try:
                stock_price = StockPrice(symbol=symbol, price=price, timestamp=datetime.utcnow())
                session.add(stock_price)
                session.commit()
            except Exception as e:
                print(f"Database error: {e}")
            finally:
                session.close()
        
        await finish_loading(loading_msg, reply)
        
    except Exception as e:
        await finish_loading_with_error(loading_msg, f"Có lỗi xảy ra: {e}")

