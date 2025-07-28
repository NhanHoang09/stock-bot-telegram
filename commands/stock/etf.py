from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd
from utils.stock_info import get_full_stock_info

async def etf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args and context.args[0].lower() == "info" and len(context.args) > 1:
        symbol = context.args[1].upper()
        info = await get_full_stock_info(symbol, debug_raw=True, update=update)
        if info:
            await update.message.reply_text(info, parse_mode='HTML')
        else:
            await update.message.reply_text("Không tìm thấy thông tin công ty cho mã này.")
        return
    
    # Nếu có tham số, tra cứu giá ETF
    if context.args:
        symbol = context.args[0].upper()
        try:
            from vnstock import Trading
            prices = Trading(source='TCBS').price_board([symbol])
            if prices.empty:
                await update.message.reply_text(f"Không tìm thấy mã ETF {symbol}")
                return
            price = float(prices.iloc[0][('match', 'match_price')])
            formatted_price = format_vnd(price)
            reply = f"💹 Giá hiện tại của <b>{symbol}</b>: <b>{formatted_price}₫</b> 🇻🇳"
            await update.message.reply_text(reply, parse_mode='HTML')
        except Exception as e:
            await update.message.reply_text(f"Có lỗi xảy ra: {e}")
        return
    
    # Nếu không có tham số, thử lấy danh sách ETF từ vnstock
    try:
        from vnstock import Listing
        listing = Listing()
        if hasattr(listing, 'etf') and callable(getattr(listing, 'etf')):
            df = listing.etf()
            if df.empty:
                await update.message.reply_text("Không tìm thấy quỹ ETF nào trên thị trường.")
                return
            etf_list = [f"🔹 <b>{row['symbol']}</b>: {row['organ_name']}" for _, row in df.iterrows()]
            reply = "📈 <b>Danh sách các quỹ ETF trên thị trường:</b>\n" + "\n".join(etf_list)
            await update.message.reply_text(reply, parse_mode='HTML')
        else:
            await update.message.reply_text("Không thể lấy danh sách ETF tự động từ dữ liệu hiện tại. Vui lòng dùng /etf <symbol> hoặc /etf info <symbol> để tra cứu.")
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

