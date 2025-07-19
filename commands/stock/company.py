import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd
from utils.loading import (
    show_animated_loading, 
    update_loading_with_company_animation, 
    update_loading_with_money_animation,
    update_loading_with_stock_animation,
    finish_loading, 
    finish_loading_with_error
)

async def company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Thông tin doanh nghiệp chi tiết"""
    if not context.args:
        await update.message.reply_text("Vui lòng nhập: /company <symbol>")
        return
    
    symbol = context.args[0].upper()
    
    # Hiển thị loading động
    loading_msg = await show_animated_loading(update, context, f"Đang tìm thông tin công ty {symbol}...")
    
    try:
        from vnstock import Company, Listing, Trading
        
        # Cập nhật loading với animation công ty
        await update_loading_with_company_animation(loading_msg, f"Đang lấy thông tin cơ bản...", 1)
        
        reply = f"🏢 <b>Thông tin doanh nghiệp {symbol}:</b>\n\n"
        
        # === THÔNG TIN CƠ BẢN ===
        try:
            # Sử dụng Listing để lấy thông tin cơ bản
            listing = Listing()
            all_symbols = listing.all_symbols()
            symbol_info = all_symbols[all_symbols['symbol'].str.upper() == symbol]
            
            if not symbol_info.empty:
                info = symbol_info.iloc[0]
                reply += "📋 <b>Thông tin cơ bản:</b>\n"
                
                # Tên công ty
                company_name = info.get('organ_name', 'N/A')
                if company_name != 'N/A' and company_name:
                    reply += f"🏢 Tên: {company_name}\n"
                
                # Sàn giao dịch
                exchange = info.get('exchange', 'N/A')
                if exchange != 'N/A' and exchange:
                    reply += f"🏛️ Sàn: {exchange}\n"
                
                # Loại chứng khoán
                security_type = info.get('type', 'N/A')
                if security_type != 'N/A' and security_type:
                    reply += f"🏷️ Loại: {security_type}\n"
                
                # Ngành nghề
                industry = info.get('industry', 'N/A')
                if industry != 'N/A' and industry:
                    reply += f"💼 Ngành: {industry}\n"
                
                # Website
                website = info.get('website', 'N/A')
                if website != 'N/A' and website:
                    reply += f"🌐 Website: {website}\n"
                
                reply += "\n"
            else:
                reply += "📋 <b>Thông tin cơ bản:</b>\n"
                reply += "❌ Không tìm thấy thông tin cơ bản\n\n"
                
        except Exception as e:
            reply += "📋 <b>Thông tin cơ bản:</b>\n"
            reply += f"❌ Lỗi khi lấy thông tin cơ bản: {str(e)}\n\n"
        
        # Cập nhật loading với animation công ty
        await update_loading_with_company_animation(loading_msg, f"Đang lấy thông tin tổng quan...", 2)
        
        # === THÔNG TIN CHI TIẾT ===
        try:
            company = Company(symbol=symbol)
            
            # Thông tin tổng quan
            try:
                overview = company.overview()
                if not overview.empty:
                    reply += "📊 <b>Thông tin tổng quan:</b>\n"
                    
                    # Vốn điều lệ
                    charter_capital = overview.get('charter_capital', [None])[0]
                    if charter_capital:
                        reply += f"💰 Vốn điều lệ: {format_vnd(charter_capital)}₫\n"
                    
                    # Số lượng cổ phiếu
                    shares_outstanding = overview.get('financial_ratio_issue_share', [None])[0]
                    if shares_outstanding:
                        reply += f"📊 Số cổ phiếu: {format_vnd(shares_outstanding)} cổ phiếu\n"
                    
                    # ID công ty
                    company_id = overview.get('id', [None])[0]
                    if company_id:
                        reply += f"🆔 Mã số: {company_id}\n"
                    
                    reply += "\n"
            except Exception as e:
                reply += "📊 <b>Thông tin tổng quan:</b>\n"
                reply += f"❌ Lỗi khi lấy thông tin tổng quan: {str(e)}\n\n"
            
            # Cập nhật loading với animation tiền tệ
            await update_loading_with_money_animation(loading_msg, f"Đang lấy chỉ số tài chính...", 3)
            
            # Thông tin tài chính cơ bản (sử dụng Finance class)
            try:
                from vnstock import Finance
                finance = Finance(source='vci', symbol=symbol)
                financial_data = finance.ratio()
                
                if not financial_data.empty:
                    latest = financial_data.iloc[0]
                    reply += "💰 <b>Chỉ số tài chính cơ bản:</b>\n"
                    
                    # P/E
                    pe = latest.get(('Chỉ tiêu định giá', 'P/E'), None)
                    if pe and pe != 'N/A':
                        reply += f"📊 P/E: {pe:.2f}\n"
                    
                    # P/B
                    pb = latest.get(('Chỉ tiêu định giá', 'P/B'), None)
                    if pb and pb != 'N/A':
                        reply += f"📊 P/B: {pb:.2f}\n"
                    
                    # ROE
                    roe = latest.get(('Chỉ tiêu sinh lời', 'ROE (%)'), None)
                    if roe and roe != 'N/A':
                        reply += f"📊 ROE: {roe:.2f}%\n"
                    
                    # ROA
                    roa = latest.get(('Chỉ tiêu sinh lời', 'ROA (%)'), None)
                    if roa and roa != 'N/A':
                        reply += f"📊 ROA: {roa:.2f}%\n"
                    
                    # EPS
                    eps = latest.get(('Chỉ tiêu định giá', 'EPS (VND)'), None)
                    if eps and eps != 'N/A':
                        reply += f"📊 EPS: {format_vnd(eps)}₫\n"
                    
                    # BVPS
                    bvps = latest.get(('Chỉ tiêu định giá', 'BVPS (VND)'), None)
                    if bvps and bvps != 'N/A':
                        reply += f"📊 BVPS: {format_vnd(bvps)}₫\n"
                    
                    # Market Cap
                    market_cap = latest.get(('Chỉ tiêu định giá', 'Market Capital (Bn. VND)'), None)
                    if market_cap and market_cap != 'N/A':
                        market_cap_vnd = market_cap * 1000000000  # Convert from Bn to VND
                        reply += f"📊 Market Cap: {format_vnd(market_cap_vnd)}₫\n"
                    
                    reply += "\n"
                else:
                    reply += "💰 <b>Chỉ số tài chính cơ bản:</b>\n"
                    reply += "❌ Không có dữ liệu tài chính\n\n"
            except Exception as e:
                reply += "💰 <b>Chỉ số tài chính cơ bản:</b>\n"
                reply += f"❌ Lỗi khi lấy thông tin tài chính: {str(e)}\n\n"
                
        except Exception as e:
            reply += f"❌ Lỗi khi lấy thông tin chi tiết: {str(e)}\n\n"
        
        # Cập nhật loading với animation cổ phiếu
        await update_loading_with_stock_animation(loading_msg, f"Đang lấy thông tin giao dịch...", 4)
        
        # === THÔNG TIN GIAO DỊCH ===
        try:
            trading = Trading(source='VCI')
            price_data = trading.price_board([symbol])
            
            if not price_data.empty:
                current_data = price_data.iloc[0]
                reply += "📈 <b>Thông tin giao dịch hiện tại:</b>\n"
                
                # Giá hiện tại
                current_price = current_data.get(('match', 'match_price'), None)
                if current_price:
                    reply += f"💰 Giá hiện tại: {format_vnd(current_price)}₫\n"
                
                # Giá tham chiếu
                ref_price = current_data.get(('match', 'reference_price'), None)
                if ref_price:
                    reply += f"📊 Giá tham chiếu: {format_vnd(ref_price)}₫\n"
                
                # Thay đổi
                if current_price and ref_price:
                    change = current_price - ref_price
                    pct_change = (change / ref_price) * 100
                    reply += f"📊 Thay đổi: {format_vnd(change)} ({pct_change:+.2f}%)\n"
                
                # Khối lượng
                volume = current_data.get(('match', 'match_vol'), None)
                if volume:
                    reply += f"📊 Khối lượng: {format_vnd(volume)} cổ phiếu\n"
                
                # Giá cao nhất
                high = current_data.get(('match', 'highest'), None)
                if high:
                    reply += f"📈 Cao nhất: {format_vnd(high)}₫\n"
                
                # Giá thấp nhất
                low = current_data.get(('match', 'lowest'), None)
                if low:
                    reply += f"📉 Thấp nhất: {format_vnd(low)}₫\n"
                
                reply += "\n"
        except Exception as e:
            reply += "📈 <b>Thông tin giao dịch hiện tại:</b>\n"
            reply += f"❌ Lỗi khi lấy thông tin giao dịch: {str(e)}\n\n"
        
        await finish_loading(loading_msg, reply)
        
    except Exception as e:
        await finish_loading_with_error(loading_msg, f"Có lỗi xảy ra: {str(e)}")

