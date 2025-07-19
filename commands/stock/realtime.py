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
        trading = Trading(source='VCI')
        prices = trading.price_board(symbols)
        
        if prices.empty:
            await update.message.reply_text("Không tìm thấy dữ liệu cho các mã này.")
            return
        
        reply = "📊 <b>Giá cổ phiếu thời gian thực:</b>\n\n"
        
        for _, row in prices.iterrows():
            symbol = row[('listing', 'symbol')]
            current_price = row[('match', 'match_price')]
            ref_price = row[('listing', 'ref_price')]
            change = current_price - ref_price
            pct_change = (change / ref_price) * 100 if ref_price else 0
            volume = row[('match', 'match_vol')]
            high = row[('match', 'highest')]
            low = row[('match', 'lowest')]
            
            emoji = "🟢" if change >= 0 else "🔴"
            reply += (
                f"{emoji} <b>{symbol}</b>\n"
                f"💰 Giá: {format_vnd(current_price)}₫ ({pct_change:+.2f}%)\n"
                f"📈 Thay đổi: {format_vnd(change)}₫\n"
                f"📊 KL: {format_vnd(volume)} cổ\n"
                f"⬆️ Cao: {format_vnd(high)}₫ | ⬇️ Thấp: {format_vnd(low)}₫\n\n"
            )
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

