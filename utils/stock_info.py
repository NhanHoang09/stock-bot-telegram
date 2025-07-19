from utils.formatters import format_vnd

def get_company_info(symbol):
    """Lấy thông tin cơ bản của công ty"""
    try:
        from vnstock import Company
        company = Company(symbol=symbol)
        info = company.overview()
        
        if info.empty:
            return None
        
        return info.iloc[0]
    except:
        return None

async def get_full_stock_info(symbol, debug_raw=False, update=None):
    """Lấy thông tin đầy đủ của cổ phiếu"""
    try:
        from vnstock import Trading, Company
        trading = Trading(source='VCI')
        company = Company(symbol=symbol)
        
        # Lấy thông tin giá
        price_data = trading.price_board([symbol])
        
        if price_data.empty:
            return None, None
        
        price_info = price_data.iloc[0]
        
        # Lấy thông tin công ty
        company_info = company.overview()
        
        if company_info.empty:
            company_info = None
        else:
            company_info = company_info.iloc[0]
        
        # Tạo thông tin hiển thị (phiên bản ngắn gọn)
        if price_info is not None and company_info is not None:
            current_price = price_info.get(('match', 'match_price'), 'N/A')
            ref_price = price_info.get(('match', 'reference_price'), 'N/A')
            change = current_price - ref_price if current_price != 'N/A' and ref_price != 'N/A' else 0
            pct_change = (change / ref_price * 100) if ref_price != 'N/A' and ref_price != 0 else 0
            volume = price_info.get(('match', 'match_vol'), 'N/A')
            high = price_info.get(('match', 'highest'), 'N/A')
            low = price_info.get(('match', 'lowest'), 'N/A')
            open_price = price_info.get(('match', 'open_price'), 'N/A')
            total_volume = price_info.get(('match', 'accumulated_volume'), 'N/A')
            
            emoji = "🟢" if change >= 0 else "🔴"
            
            reply = f"📊 <b>THÔNG TIN {symbol}:</b>\n\n"
            
            # === THÔNG TIN GIÁ CHÍNH ===
            reply += f"{emoji} <b>📈 GIÁ:</b>\n"
            reply += f"💰 Hiện tại: {format_vnd(current_price)}₫\n"
            reply += f"📈 Thay đổi: {format_vnd(change)} ({pct_change:+.2f}%)\n"
            reply += f"🚪 Mở cửa: {format_vnd(open_price)}₫\n"
            reply += f"📈 Cao nhất: {format_vnd(high)}₫\n"
            reply += f"📉 Thấp nhất: {format_vnd(low)}₫\n"
            reply += f"📊 KL hiện tại: {format_vnd(volume)} cổ\n"
            reply += f"📊 KL tổng: {format_vnd(total_volume)} cổ\n\n"
            
            # === THÔNG TIN CÔNG TY ===
            reply += "🏢 <b>📋 CÔNG TY:</b>\n"
            reply += f"🆔 Mã số: {company_info.get('id', 'N/A')}\n"
            reply += f"📊 Cổ phiếu: {format_vnd(company_info.get('issue_share', 'N/A'))} cổ\n"
            reply += f"💰 Vốn điều lệ: {format_vnd(company_info.get('charter_capital', 'N/A'))}₫\n"
            reply += f"🏭 Ngành: {company_info.get('icb_name2', 'N/A')}\n"
            reply += f"🏭 Phân ngành: {company_info.get('icb_name3', 'N/A')}\n\n"
            
            # === THÔNG TIN GIAO DỊCH ===
            reply += "💼 <b>💼 GIAO DỊCH:</b>\n"
            reply += f"🏢 Sàn: {price_info.get(('listing', 'exchange'), 'N/A')}\n"
            reply += f"📊 Loại: {price_info.get(('listing', 'stock_type'), 'N/A')}\n"
            reply += f"📈 Trạng thái: {price_info.get(('listing', 'trading_status'), 'N/A')}\n"
            reply += f"📅 Ngày giao dịch: {price_info.get(('listing', 'trading_date'), 'N/A')}\n\n"
            
            # === GIÁ TRẦN/SÀN ===
            reply += "📊 <b>📊 GIÁ TRẦN/SÀN:</b>\n"
            reply += f"📈 Trần: {format_vnd(price_info.get(('listing', 'ceiling'), 'N/A'))}₫\n"
            reply += f"📉 Sàn: {format_vnd(price_info.get(('listing', 'floor'), 'N/A'))}₫\n\n"
            
            # === THÔNG TIN NƯỚC NGOÀI ===
            foreign_buy = price_info.get(('match', 'foreign_buy_volume'), 'N/A')
            foreign_sell = price_info.get(('match', 'foreign_sell_volume'), 'N/A')
            if foreign_buy != 'N/A' or foreign_sell != 'N/A':
                reply += "🌍 <b>🌍 NƯỚC NGOÀI:</b>\n"
                reply += f"📊 Mua: {format_vnd(foreign_buy)} cổ\n"
                reply += f"📊 Bán: {format_vnd(foreign_sell)} cổ\n\n"
            
            # === GIÁ KHỚP LỆNH ===
            reply += "💱 <b>💱 GIÁ KHỚP LỆNH:</b>\n"
            bid1 = price_info.get(('bid_ask', 'bid_1_price'), 'N/A')
            ask1 = price_info.get(('bid_ask', 'ask_1_price'), 'N/A')
            if bid1 != 'N/A' and ask1 != 'N/A':
                reply += f"📊 Mua: {format_vnd(bid1)}₫\n"
                reply += f"📊 Bán: {format_vnd(ask1)}₫\n\n"
            
            # === MÔ TẢ NGẮN GỌN ===
            company_profile = company_info.get('company_profile', '')
            if company_profile:
                reply += "📝 <b>📝 MÔ TẢ:</b>\n"
                # Giới hạn độ dài mô tả
                if len(company_profile) > 300:
                    reply += f"{company_profile[:300]}...\n\n"
                else:
                    reply += f"{company_profile}\n\n"
            
            return reply
        else:
            return None
        
    except Exception as e:
        if debug_raw and update:
            await update.message.reply_text(f"Debug error: {e}")
        return None 