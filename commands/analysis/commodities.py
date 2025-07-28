from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd

async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Giá vàng trong nước và thế giới"""
    try:
        from vnstock import Trading
        trading = Trading(source='TCBS')
        
        # Lấy giá vàng từ các mã vàng phổ biến
        gold_symbols = ['SJC', 'PNJ', 'BVH']  # Các mã liên quan đến vàng
        gold_data = trading.price_board(gold_symbols)
        
        reply = "🥇 <b>THÔNG TIN VÀNG:</b>\n\n"
        
        # Thông tin vàng trong nước
        reply += "🇻🇳 <b>Vàng trong nước:</b>\n"
        
        # Thử lấy thông tin từ các nguồn khác nhau
        try:
            # Lấy thông tin từ Trading API
            all_prices = trading.price_board()
            gold_related = all_prices[
                all_prices[('listing', 'symbol')].str.contains('GOLD|VANG|SJC', case=False, na=False)
            ]
            
            if not gold_related.empty:
                for _, row in gold_related.head(5).iterrows():
                    symbol = row[('listing', 'symbol')]
                    price = row[('match', 'match_price')]
                    change = row[('match', 'match_price')] - row[('listing', 'ref_price')]
                    pct_change = (change / row[('listing', 'ref_price')]) * 100 if row[('listing', 'ref_price')] else 0
                    
                    emoji = "🟢" if change >= 0 else "🔴"
                    reply += f"{emoji} <b>{symbol}</b>: {format_vnd(price)}₫ ({pct_change:+.2f}%)\n"
            else:
                reply += "📊 Không có dữ liệu vàng trong nước\n"
        except:
            reply += "📊 Không có dữ liệu vàng trong nước\n"
        
        reply += "\n🌍 <b>Lưu ý:</b>\n"
        reply += "• Giá vàng thế giới thường được cập nhật qua các nguồn quốc tế\n"
        reply += "• Giá vàng trong nước có thể khác biệt do thuế và phí\n"
        reply += "• Nên tham khảo các trang chuyên về vàng để có thông tin chính xác\n\n"
        
        reply += "💡 <b>Mã cổ phiếu liên quan vàng:</b>\n"
        reply += "• SJC - Công ty Vàng bạc Đá quý Sài Gòn\n"
        reply += "• PNJ - Công ty Cổ phần Vàng bạc Đá quý Phú Nhuận\n"
        reply += "• BVH - Tập đoàn Bảo Việt\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def metals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kim loại quý và nguyên liệu"""
    try:
        from vnstock import Trading
        trading = Trading(source='TCBS')
        
        # Lấy thông tin các công ty khai thác kim loại
        metal_symbols = ['HPG', 'HSG', 'TVN', 'TLH', 'KSB']  # Thép, kim loại
        metal_data = trading.price_board(metal_symbols)
        
        reply = "🔧 <b>KIM LOẠI & NGUYÊN LIỆU:</b>\n\n"
        
        if not metal_data.empty:
            reply += "🏭 <b>Công ty thép & kim loại:</b>\n"
            
            for _, row in metal_data.iterrows():
                symbol = row[('listing', 'symbol')]
                price = row[('match', 'match_price')]
                ref_price = row[('listing', 'ref_price')]
                change = price - ref_price
                pct_change = (change / ref_price) * 100 if ref_price else 0
                volume = row[('match', 'match_vol')]
                
                emoji = "🟢" if change >= 0 else "🔴"
                reply += f"{emoji} <b>{symbol}</b>\n"
                reply += f"   💰 Giá: {format_vnd(price)}₫ ({pct_change:+.2f}%)\n"
                reply += f"   📊 KL: {format_vnd(volume)} cổ\n\n"
        else:
            reply += "📊 Không có dữ liệu kim loại\n"
        
        reply += "📈 <b>Thông tin thị trường:</b>\n"
        reply += "• Giá thép và kim loại phụ thuộc vào nhu cầu xây dựng\n"
        reply += "• Giá nguyên liệu thô ảnh hưởng đến chi phí sản xuất\n"
        reply += "• Xuất khẩu thép là ngành quan trọng của Việt Nam\n\n"
        
        reply += "💡 <b>Mã cổ phiếu chính:</b>\n"
        reply += "• HPG - Hòa Phát (Thép)\n"
        reply += "• HSG - Tôn Hoa Sen (Thép)\n"
        reply += "• TVN - Thép Việt Nhật\n"
        reply += "• TLH - Tập đoàn Thép Thái Long\n"
        reply += "• KSB - KSB (Thép)\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def commodities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hàng hóa và nguyên liệu cơ bản"""
    try:
        from vnstock import Trading
        trading = Trading(source='TCBS')
        
        # Lấy thông tin các công ty nông nghiệp, thực phẩm
        commodity_symbols = ['VNM', 'FPT', 'VIC', 'HPG', 'GAS']  # Đa dạng hàng hóa
        commodity_data = trading.price_board(commodity_symbols)
        
        reply = "📦 <b>HÀNG HÓA & NGUYÊN LIỆU:</b>\n\n"
        
        if not commodity_data.empty:
            reply += "🏢 <b>Giá cổ phiếu hàng hóa:</b>\n"
            
            for _, row in commodity_data.iterrows():
                symbol = row[('listing', 'symbol')]
                price = row[('match', 'match_price')]
                ref_price = row[('listing', 'ref_price')]
                change = price - ref_price
                pct_change = (change / ref_price) * 100 if ref_price else 0
                volume = row[('match', 'match_vol')]
                
                emoji = "🟢" if change >= 0 else "🔴"
                
                # Phân loại theo ngành
                if symbol in ['VNM']:
                    category = "🥛 Thực phẩm"
                elif symbol in ['FPT']:
                    category = "💻 Công nghệ"
                elif symbol in ['VIC']:
                    category = "🏗️ Bất động sản"
                elif symbol in ['HPG']:
                    category = "🔧 Thép"
                elif symbol in ['GAS']:
                    category = "⛽ Năng lượng"
                else:
                    category = "📊 Khác"
                
                reply += f"{emoji} <b>{symbol}</b> {category}\n"
                reply += f"   💰 Giá: {format_vnd(price)}₫ ({pct_change:+.2f}%)\n"
                reply += f"   📊 KL: {format_vnd(volume)} cổ\n\n"
        else:
            reply += "📊 Không có dữ liệu hàng hóa\n"
        
        reply += "🌾 <b>Phân loại hàng hóa:</b>\n"
        reply += "• <b>Nông nghiệp:</b> VNM, HAG, HNG\n"
        reply += "• <b>Thực phẩm:</b> VNM, MSN, KDC\n"
        reply += "• <b>Năng lượng:</b> GAS, PVD, PVS\n"
        reply += "• <b>Vật liệu:</b> HPG, HSG, TVN\n"
        reply += "• <b>Hóa chất:</b> DCM, DPM, LIX\n\n"
        
        reply += "📈 <b>Yếu tố ảnh hưởng:</b>\n"
        reply += "• Giá nguyên liệu thô quốc tế\n"
        reply += "• Tỷ giá USD/VND\n"
        reply += "• Nhu cầu tiêu thụ trong nước\n"
        reply += "• Chính sách xuất nhập khẩu\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

