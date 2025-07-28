from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Top cổ phiếu theo tiêu chí"""
    if not context.args:
        await update.message.reply_text("Vui lòng nhập: /top <gainers|losers|volume|value> [limit]")
        return
    
    criteria = context.args[0].lower()
    limit = int(context.args[1]) if len(context.args) > 1 and context.args[1].isdigit() else 10
    
    try:
        from vnstock import Trading
        trading = Trading(source='TCBS')
        
        if criteria in ['gainers', 'losers']:
            data = trading.top_mover(criteria, limit=limit)
            title = "Top tăng giá" if criteria == 'gainers' else "Top giảm giá"
            emoji = "🟢" if criteria == 'gainers' else "🔴"
        elif criteria == 'volume':
            data = trading.top_mover('volume', limit=limit)
            title = "Top khối lượng"
            emoji = "📊"
        elif criteria == 'value':
            data = trading.top_mover('value', limit=limit)
            title = "Top giá trị"
            emoji = "💰"
        else:
            await update.message.reply_text("Tiêu chí không hợp lệ. Dùng: gainers, losers, volume, value")
            return
        
        reply = f"{emoji} <b>{title}:</b>\n\n"
        
        for i, (_, row) in enumerate(data.iterrows(), 1):
            symbol = row['symbol']
            if criteria in ['gainers', 'losers']:
                change_pct = row['change_pct']
                reply += f"{i}. {symbol}: {change_pct:+.2f}%\n"
            elif criteria == 'volume':
                volume = row['volume']
                reply += f"{i}. {symbol}: {format_vnd(volume)} cổ\n"
            elif criteria == 'value':
                value = row['value']
                reply += f"{i}. {symbol}: {format_vnd(value)}₫\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

