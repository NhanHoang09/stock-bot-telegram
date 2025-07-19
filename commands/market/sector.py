from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd

async def sector(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cổ phiếu theo ngành"""
    if not context.args:
        await update.message.reply_text("Vui lòng nhập: /sector <tên_ngành>")
        return
    
    sector_name = ' '.join(context.args).upper()
    try:
        from vnstock import Listing
        listing = Listing()
        all_symbols = listing.all_symbols()
        
        # Lọc theo ngành
        sector_stocks = all_symbols[
            all_symbols['industry'].str.upper().str.contains(sector_name, na=False)
        ]
        
        if sector_stocks.empty:
            await update.message.reply_text(f"Không tìm thấy cổ phiếu nào trong ngành '{sector_name}'")
            return
        
        reply = f"🏭 <b>Cổ phiếu ngành {sector_name}:</b>\n\n"
        
        for _, row in sector_stocks.head(20).iterrows():
            symbol = row['symbol']
            company_name = row['organ_name']
            exchange = row.get('exchange', 'N/A')
            reply += f"🔹 <b>{symbol}</b> ({exchange})\n"
            reply += f"   {company_name}\n\n"
        
        if len(sector_stocks) > 20:
            reply += f"... và {len(sector_stocks) - 20} cổ phiếu khác"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

