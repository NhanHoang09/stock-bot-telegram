from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd

async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Thông tin thị trường"""
    try:
        from vnstock import Trading
        trading = Trading(source='VCI')
        
        # Lấy thông tin VN-Index và HNX-Index
        indices = trading.price_board(['VNINDEX', 'HNXINDEX'])
        
        reply = "📈 <b>Thông tin thị trường:</b>\n\n"
        
        for _, row in indices.iterrows():
            symbol = row[('listing', 'symbol')]
            current_price = row[('match', 'match_price')]
            ref_price = row[('match', 'reference_price')]
            change = current_price - ref_price
            pct_change = (change / ref_price) * 100 if ref_price else 0
            volume = row[('match', 'match_vol')]
            
            emoji = "🟢" if change >= 0 else "🔴"
            name = "VN-Index" if symbol == "VNINDEX" else "HNX-Index"
            
            reply += (
                f"{emoji} <b>{name}</b>\n"
                f"📊 Giá: {format_vnd(current_price)} ({pct_change:+.2f}%)\n"
                f"📈 Thay đổi: {format_vnd(change)}\n"
                f"📊 KL: {format_vnd(volume)} cổ\n\n"
            )
        
        # Thêm thông tin top cổ phiếu tăng/giảm
        try:
            top_gainers = trading.top_mover('gainers', limit=5)
            top_losers = trading.top_mover('losers', limit=5)
            
            reply += "🟢 <b>Top tăng giá:</b>\n"
            for _, row in top_gainers.iterrows():
                symbol = row['symbol']
                change_pct = row['change_pct']
                reply += f"📈 {symbol}: +{change_pct:.2f}%\n"
            
            reply += "\n🔴 <b>Top giảm giá:</b>\n"
            for _, row in top_losers.iterrows():
                symbol = row['symbol']
                change_pct = row['change_pct']
                reply += f"📉 {symbol}: {change_pct:.2f}%\n"
        except:
            pass
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

