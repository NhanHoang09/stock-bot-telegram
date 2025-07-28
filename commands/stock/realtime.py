from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd

async def realtime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Giá cổ phiếu thời gian thực"""
    if not context.args:
        await update.message.reply_text("Vui lòng nhập: /realtime <symbol1> <symbol2> ...")
        return
    
    symbols = [s.upper() for s in context.args]
    try:
        from vnstock import Trading
        trading = Trading(source='TCBS')
        prices = trading.price_board(symbols)
        
        if prices.empty:
            await update.message.reply_text("Không tìm thấy dữ liệu cho các mã này.")
            return
        
        reply = "📊 <b>Realtime stock prices:</b>\n\n"
        
        for _, row in prices.iterrows():
            # Mã cổ phiếu
            symbol = row.get('Mã CP', 'N/A')
            # Giá hiện tại
            current_price = row.get('Giá', 'N/A')
            # Giá tham chiếu hoặc thay đổi phiên (cần xác nhận lại ý nghĩa cột này)
            ref_price = row.get('Phiên +/- ', 0)
            try:
                # Chênh lệch giá so với ref_price
                change = float(current_price) - float(ref_price)
            except Exception:
                change = 0
            try:
                # Phần trăm thay đổi giá
                pct_change = (change / float(ref_price)) * 100 if ref_price else 0
            except Exception:
                pct_change = 0
            # Khối lượng giao dịch ròng (có thể là khối lượng mua bán ròng)
            volume = row.get('KLGD ròng(CM)', 'N/A')
            # Giá cao nhất 1 năm
            high = row.get('Đỉnh 1Y', 'N/A')
            # Giá thấp nhất 1 năm
            low = row.get('Đáy 1Y', 'N/A')
            
            emoji = "🟢" if change >= 0 else "🔴"
            reply += (
                f"{emoji} <b>{symbol}</b>\n"
                f"💰 Price: {format_vnd(current_price)}₫ ({pct_change:+.2f}%)\n"  # Giá hiện tại và phần trăm thay đổi
                f"📈 Change: {format_vnd(change)}₫\n"  # Chênh lệch giá so với ref_price
                f"📊 Volume: {format_vnd(volume)}\n"  # Khối lượng giao dịch ròng
                f"⬆️ High: {format_vnd(high)}₫ | ⬇️ Low: {format_vnd(low)}₫\n\n"  # Giá cao nhất/thấp nhất 1 năm
            )
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

