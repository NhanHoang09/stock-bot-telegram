from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd

async def filter_pe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lọc cổ phiếu theo P/E"""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Vui lòng nhập: /filter_pe <min_pe> <max_pe> [limit]")
        await update.message.reply_text("Ví dụ: /filter_pe 5 15 20")
        return
    
    try:
        min_pe = float(context.args[0])
        max_pe = float(context.args[1])
        limit = int(context.args[2]) if len(context.args) > 2 else 20
        
        from vnstock import Listing
        listing = Listing()
        all_symbols = listing.all_symbols()
        
        # Lọc cổ phiếu có P/E trong khoảng
        filtered_stocks = []
        
        for _, row in all_symbols.iterrows():
            symbol = row['symbol']
            try:
                from vnstock import Company
                company = Company(symbol=symbol)
                financial_data = company.financial_ratio()
                
                if not financial_data.empty:
                    latest_pe = financial_data.iloc[-1].get('pe')
                    if latest_pe and min_pe <= latest_pe <= max_pe:
                        filtered_stocks.append({
                            'symbol': symbol,
                            'pe': latest_pe,
                            'company_name': row.get('organ_name', 'N/A')
                        })
                        
                        if len(filtered_stocks) >= limit:
                            break
            except:
                continue
        
        if not filtered_stocks:
            await update.message.reply_text(f"Không tìm thấy cổ phiếu nào có P/E từ {min_pe} đến {max_pe}")
            return
        
        # Sắp xếp theo P/E
        filtered_stocks.sort(key=lambda x: x['pe'])
        
        reply = f"📊 <b>Cổ phiếu có P/E từ {min_pe} đến {max_pe}:</b>\n\n"
        
        for i, stock in enumerate(filtered_stocks, 1):
            reply += f"{i}. <b>{stock['symbol']}</b> - P/E: {stock['pe']:.2f}\n"
            reply += f"   {stock['company_name']}\n\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def filter_roe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lọc cổ phiếu theo ROE"""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Vui lòng nhập: /filter_roe <min_roe> <max_roe> [limit]")
        await update.message.reply_text("Ví dụ: /filter_roe 15 30 20")
        return
    
    try:
        min_roe = float(context.args[0])
        max_roe = float(context.args[1])
        limit = int(context.args[2]) if len(context.args) > 2 else 20
        
        from vnstock import Listing
        listing = Listing()
        all_symbols = listing.all_symbols()
        
        filtered_stocks = []
        
        for _, row in all_symbols.iterrows():
            symbol = row['symbol']
            try:
                from vnstock import Company
                company = Company(symbol=symbol)
                financial_data = company.financial_ratio()
                
                if not financial_data.empty:
                    latest_roe = financial_data.iloc[-1].get('roe')
                    if latest_roe and min_roe <= latest_roe <= max_roe:
                        filtered_stocks.append({
                            'symbol': symbol,
                            'roe': latest_roe,
                            'company_name': row.get('organ_name', 'N/A')
                        })
                        
                        if len(filtered_stocks) >= limit:
                            break
            except:
                continue
        
        if not filtered_stocks:
            await update.message.reply_text(f"Không tìm thấy cổ phiếu nào có ROE từ {min_roe}% đến {max_roe}%")
            return
        
        # Sắp xếp theo ROE (giảm dần)
        filtered_stocks.sort(key=lambda x: x['roe'], reverse=True)
        
        reply = f"💹 <b>Cổ phiếu có ROE từ {min_roe}% đến {max_roe}%:</b>\n\n"
        
        for i, stock in enumerate(filtered_stocks, 1):
            reply += f"{i}. <b>{stock['symbol']}</b> - ROE: {stock['roe']:.2f}%\n"
            reply += f"   {stock['company_name']}\n\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def filter_market_cap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lọc cổ phiếu theo vốn hóa thị trường"""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Vui lòng nhập: /filter_market_cap <min_cap> <max_cap> [limit]")
        await update.message.reply_text("Ví dụ: /filter_market_cap 1000 10000 20")
        await update.message.reply_text("Đơn vị: tỷ VNĐ")
        return
    
    try:
        min_cap = float(context.args[0]) * 1e9  # Chuyển từ tỷ sang VNĐ
        max_cap = float(context.args[1]) * 1e9
        limit = int(context.args[2]) if len(context.args) > 2 else 20
        
        from vnstock import Listing
        listing = Listing()
        all_symbols = listing.all_symbols()
        
        filtered_stocks = []
        
        for _, row in all_symbols.iterrows():
            symbol = row['symbol']
            try:
                from vnstock import Company
                company = Company(symbol=symbol)
                financial_data = company.financial_ratio()
                
                if not financial_data.empty:
                    latest_market_cap = financial_data.iloc[-1].get('market_cap')
                    if latest_market_cap and min_cap <= latest_market_cap <= max_cap:
                        filtered_stocks.append({
                            'symbol': symbol,
                            'market_cap': latest_market_cap,
                            'company_name': row.get('organ_name', 'N/A')
                        })
                        
                        if len(filtered_stocks) >= limit:
                            break
            except:
                continue
        
        if not filtered_stocks:
            await update.message.reply_text(f"Không tìm thấy cổ phiếu nào có vốn hóa từ {context.args[0]} đến {context.args[1]} tỷ VNĐ")
            return
        
        # Sắp xếp theo vốn hóa (giảm dần)
        filtered_stocks.sort(key=lambda x: x['market_cap'], reverse=True)
        
        reply = f"💰 <b>Cổ phiếu có vốn hóa từ {context.args[0]} đến {context.args[1]} tỷ VNĐ:</b>\n\n"
        
        for i, stock in enumerate(filtered_stocks, 1):
            market_cap_bil = stock['market_cap'] / 1e9
            reply += f"{i}. <b>{stock['symbol']}</b> - Vốn hóa: {market_cap_bil:.1f} tỷ VNĐ\n"
            reply += f"   {stock['company_name']}\n\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def filter_volume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lọc cổ phiếu theo khối lượng giao dịch"""
    if not context.args:
        await update.message.reply_text("Vui lòng nhập: /filter_volume <min_volume> [limit]")
        await update.message.reply_text("Ví dụ: /filter_volume 1000000 20")
        await update.message.reply_text("Đơn vị: cổ phiếu")
        return
    
    try:
        min_volume = int(context.args[0])
        limit = int(context.args[1]) if len(context.args) > 1 else 20
        
        from vnstock import Trading
        trading = Trading(source='TCBS')
        
        # Lấy tất cả cổ phiếu có khối lượng > min_volume
        all_prices = trading.price_board()
        
        filtered_stocks = []
        
        for _, row in all_prices.iterrows():
            symbol = row[('listing', 'symbol')]
            volume = row[('match', 'match_vol')]
            
            if volume and volume >= min_volume:
                current_price = row[('match', 'match_price')]
                ref_price = row[('listing', 'ref_price')]
                change = current_price - ref_price
                pct_change = (change / ref_price) * 100 if ref_price else 0
                
                filtered_stocks.append({
                    'symbol': symbol,
                    'volume': volume,
                    'price': current_price,
                    'change_pct': pct_change
                })
                
                if len(filtered_stocks) >= limit:
                    break
        
        if not filtered_stocks:
            await update.message.reply_text(f"Không tìm thấy cổ phiếu nào có khối lượng >= {format_vnd(min_volume)} cổ")
            return
        
        # Sắp xếp theo khối lượng (giảm dần)
        filtered_stocks.sort(key=lambda x: x['volume'], reverse=True)
        
        reply = f"📊 <b>Cổ phiếu có khối lượng >= {format_vnd(min_volume)} cổ:</b>\n\n"
        
        for i, stock in enumerate(filtered_stocks, 1):
            emoji = "🟢" if stock['change_pct'] >= 0 else "🔴"
            reply += f"{i}. {emoji} <b>{stock['symbol']}</b>\n"
            reply += f"   KL: {format_vnd(stock['volume'])} cổ | Giá: {format_vnd(stock['price'])}₫ ({stock['change_pct']:+.2f}%)\n\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def filter_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lọc cổ phiếu theo giá"""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Vui lòng nhập: /filter_price <min_price> <max_price> [limit]")
        await update.message.reply_text("Ví dụ: /filter_price 10000 50000 20")
        return
    
    try:
        min_price = float(context.args[0])
        max_price = float(context.args[1])
        limit = int(context.args[2]) if len(context.args) > 2 else 20
        
        from vnstock import Trading
        trading = Trading(source='TCBS')
        all_prices = trading.price_board()
        
        filtered_stocks = []
        
        for _, row in all_prices.iterrows():
            symbol = row[('listing', 'symbol')]
            current_price = row[('match', 'match_price')]
            
            if current_price and min_price <= current_price <= max_price:
                ref_price = row[('listing', 'ref_price')]
                change = current_price - ref_price
                pct_change = (change / ref_price) * 100 if ref_price else 0
                volume = row[('match', 'match_vol')]
                
                filtered_stocks.append({
                    'symbol': symbol,
                    'price': current_price,
                    'change_pct': pct_change,
                    'volume': volume
                })
                
                if len(filtered_stocks) >= limit:
                    break
        
        if not filtered_stocks:
            await update.message.reply_text(f"Không tìm thấy cổ phiếu nào có giá từ {format_vnd(min_price)} đến {format_vnd(max_price)}₫")
            return
        
        # Sắp xếp theo giá (tăng dần)
        filtered_stocks.sort(key=lambda x: x['price'])
        
        reply = f"💰 <b>Cổ phiếu có giá từ {format_vnd(min_price)} đến {format_vnd(max_price)}₫:</b>\n\n"
        
        for i, stock in enumerate(filtered_stocks, 1):
            emoji = "🟢" if stock['change_pct'] >= 0 else "🔴"
            reply += f"{i}. {emoji} <b>{stock['symbol']}</b>\n"
            reply += f"   Giá: {format_vnd(stock['price'])}₫ ({stock['change_pct']:+.2f}%) | KL: {format_vnd(stock['volume'])} cổ\n\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def filter_sector(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lọc cổ phiếu theo ngành"""
    if not context.args:
        await update.message.reply_text("Vui lòng nhập: /filter_sector <tên_ngành> [limit]")
        await update.message.reply_text("Ví dụ: /filter_sector tài chính 20")
        await update.message.reply_text("Ví dụ: /filter_sector công nghệ 15")
        return
    
    try:
        sector_name = ' '.join(context.args[:-1]).upper() if len(context.args) > 1 else context.args[0].upper()
        limit = int(context.args[-1]) if len(context.args) > 1 and context.args[-1].isdigit() else 20
        
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
        
        # Lấy thông tin giá cho các cổ phiếu trong ngành
        from vnstock import Trading
        trading = Trading(source='TCBS')
        
        sector_symbols = sector_stocks['symbol'].tolist()
        prices = trading.price_board(sector_symbols)
        
        filtered_stocks = []
        
        for _, row in prices.iterrows():
            symbol = row[('listing', 'symbol')]
            current_price = row[('match', 'match_price')]
            ref_price = row[('listing', 'ref_price')]
            change = current_price - ref_price
            pct_change = (change / ref_price) * 100 if ref_price else 0
            volume = row[('match', 'match_vol')]
            
            # Lấy tên công ty
            company_info = sector_stocks[sector_stocks['symbol'] == symbol]
            company_name = company_info.iloc[0]['organ_name'] if not company_info.empty else symbol
            
            filtered_stocks.append({
                'symbol': symbol,
                'company_name': company_name,
                'price': current_price,
                'change_pct': pct_change,
                'volume': volume
            })
            
            if len(filtered_stocks) >= limit:
                break
        
        # Sắp xếp theo % thay đổi (giảm dần)
        filtered_stocks.sort(key=lambda x: x['change_pct'], reverse=True)
        
        reply = f"🏭 <b>Cổ phiếu ngành {sector_name} (Top {len(filtered_stocks)}):</b>\n\n"
        
        for i, stock in enumerate(filtered_stocks, 1):
            emoji = "🟢" if stock['change_pct'] >= 0 else "🔴"
            reply += f"{i}. {emoji} <b>{stock['symbol']}</b> ({stock['change_pct']:+.2f}%)\n"
            reply += f"   Giá: {format_vnd(stock['price'])}₫ | KL: {format_vnd(stock['volume'])} cổ\n"
            reply += f"   {stock['company_name']}\n\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def screener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bộ lọc cổ phiếu tổng hợp"""
    try:
        from vnstock import Trading, Listing
        trading = Trading(source='TCBS')
        listing = Listing()
        
        reply = "🔍 <b>BỘ LỌC CỔ PHIẾU TỔNG HỢP:</b>\n\n"
        
        # Lấy top cổ phiếu theo các tiêu chí
        try:
            # Top tăng giá
            top_gainers = trading.top_mover('gainers', limit=5)
            reply += "🟢 <b>Top tăng giá:</b>\n"
            for i, (_, row) in enumerate(top_gainers.iterrows(), 1):
                symbol = row['symbol']
                change_pct = row['change_pct']
                reply += f"   {i}. {symbol}: +{change_pct:.2f}%\n"
            reply += "\n"
        except:
            pass
        
        try:
            # Top giảm giá
            top_losers = trading.top_mover('losers', limit=5)
            reply += "🔴 <b>Top giảm giá:</b>\n"
            for i, (_, row) in enumerate(top_losers.iterrows(), 1):
                symbol = row['symbol']
                change_pct = row['change_pct']
                reply += f"   {i}. {symbol}: {change_pct:.2f}%\n"
            reply += "\n"
        except:
            pass
        
        try:
            # Top khối lượng
            top_volume = trading.top_mover('volume', limit=5)
            reply += "📊 <b>Top khối lượng:</b>\n"
            for i, (_, row) in enumerate(top_volume.iterrows(), 1):
                symbol = row['symbol']
                volume = row['volume']
                reply += f"   {i}. {symbol}: {format_vnd(volume)} cổ\n"
            reply += "\n"
        except:
            pass
        
        try:
            # Top giá trị
            top_value = trading.top_mover('value', limit=5)
            reply += "💰 <b>Top giá trị:</b>\n"
            for i, (_, row) in enumerate(top_value.iterrows(), 1):
                symbol = row['symbol']
                value = row['value']
                reply += f"   {i}. {symbol}: {format_vnd(value)}₫\n"
            reply += "\n"
        except:
            pass
        
        reply += "💡 <b>Lưu ý:</b>\n"
        reply += "• Dữ liệu được cập nhật theo thời gian thực\n"
        reply += "• Sử dụng các lệnh filter để lọc chi tiết hơn\n"
        reply += "• Kết hợp nhiều tiêu chí để ra quyết định\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}") 