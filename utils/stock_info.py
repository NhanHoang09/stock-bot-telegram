import pandas as pd
from utils.formatters import format_vnd

async def get_full_stock_info(symbol, debug_raw=False, update=None):
    try:
        from vnstock import Trading, Company, Listing
        # Lấy thông tin giá hiện tại
        trading = Trading(source='TCBS')
        price_data = trading.price_board([symbol])
        price_info = price_data.iloc[0] if not price_data.empty else None
        # Lấy thông tin công ty tổng quan
        company = Company(symbol=symbol)
        overview = company.overview()
        overview_info = overview.iloc[0] if not overview.empty else None
        # Lấy thông tin cơ bản từ Listing
        listing = Listing()
        all_symbols = listing.all_symbols()
        symbol_info = all_symbols[all_symbols['ticker'].str.upper() == symbol]
        symbol_info = symbol_info.iloc[0] if not symbol_info.empty else None
        # Lấy thông tin tài chính (nếu có)
        try:
            from vnstock import Finance
            finance = Finance(source='vci', symbol=symbol)
            financial_data = finance.ratio()
            latest_fin = financial_data.iloc[0] if not financial_data.empty else None
        except Exception:
            latest_fin = None
        # === Compose reply ===
        reply = f"<b>📊 STOCK INFO: {symbol}</b>\n\n"
        # --- Basic Info ---
        reply += "<b>🏢 Basic Info:</b>\n"
        if symbol_info is not None:
            company_name = symbol_info.get('organ_name', 'N/A')
            # Only 'ticker' and 'organ_name' are available from Listing().all_symbols()
            if company_name: reply += f"🏢 Name: {company_name}\n"
            reply += f"🏛️ Ticker: {symbol}\n"
        else:
            reply += "N/A\n"
        reply += "\n"
        # --- Overview ---
        reply += "<b>📊 Overview:</b>\n"
        if overview_info is not None:
            charter_capital = overview_info.get('charter_capital', 'N/A')
            outstanding_share = overview_info.get('outstanding_share', 'N/A')
            established_year = overview_info.get('established_year', 'N/A')
            no_shareholders = overview_info.get('no_shareholders', 'N/A')
            no_employees = overview_info.get('no_employees', 'N/A')
            stock_rating = overview_info.get('stock_rating', 'N/A')
            short_name = overview_info.get('short_name', 'N/A')
            industry_id = overview_info.get('industry_id', 'N/A')
            industry_id_v2 = overview_info.get('industry_id_v2', 'N/A')
            if charter_capital: reply += f"💰 Charter capital: {format_vnd(charter_capital)}₫\n"
            if outstanding_share: reply += f"📊 Outstanding shares: {outstanding_share}\n"
            if established_year: reply += f"🏢 Established year: {established_year}\n"
            if no_shareholders: reply += f"👥 Shareholders: {no_shareholders}\n"
            if no_employees: reply += f"👨‍💼 Employees: {no_employees}\n"
            if stock_rating: reply += f"⭐ Stock rating (TCBS): {stock_rating}/5\n"
            if short_name: reply += f"🏷️ Short name: {short_name}\n"
            if industry_id: reply += f"🏷️ Industry ID: {industry_id}\n"
            if industry_id_v2: reply += f"🏷️ Industry ID v2: {industry_id_v2}\n"
        else:
            reply += "N/A\n"
        reply += "\n"
        # --- Financial ---
        reply += "<b>💰 Financial:</b>\n"
        if latest_fin is not None:
            pe = latest_fin.get(('Chỉ tiêu định giá', 'P/E'), None)
            pb = latest_fin.get(('Chỉ tiêu định giá', 'P/B'), None)
            roe = latest_fin.get(('Chỉ tiêu sinh lời', 'ROE (%)'), None)
            eps = latest_fin.get(('Chỉ tiêu định giá', 'EPS (VND)'), None)
            market_cap = latest_fin.get(('Chỉ tiêu định giá', 'Market Capital (Bn. VND)'), None)
            if pe: reply += f"📊 P/E: {pe:.2f}\n"
            if pb: reply += f"📊 P/B: {pb:.2f}\n"
            if roe: reply += f"📊 ROE: {roe:.2f}%\n"
            if eps: reply += f"📊 EPS: {format_vnd(eps)}₫\n"
            if market_cap: reply += f"📊 Market Cap: {format_vnd(market_cap * 1_000_000_000)}₫\n"
            reply += "\n<i>See /financial &lt;symbol&gt; for full financial details.</i>\n"
        else:
            reply += "N/A\n"
        reply += "\n"
        # --- Realtime Trading ---
        reply += "<b>📈 Realtime Trading:</b>\n"
        if price_info is not None:
            current_price = price_info.get('Giá', 'N/A')
            volume = price_info.get('KLGD ròng(CM)', 'N/A')
            high = price_info.get('Đỉnh 1Y', 'N/A')
            low = price_info.get('Đáy 1Y', 'N/A')
            reply += f"💰 Price: {format_vnd(current_price)}₫\n"
            reply += f"📊 Volume: {format_vnd(volume)}\n"
            reply += f"⬆️ High 1Y: {format_vnd(high)}₫ | ⬇️ Low 1Y: {format_vnd(low)}₫\n"
        else:
            reply += "N/A\n"
        return reply
    except Exception as e:
        if debug_raw and update:
            await update.message.reply_text(f"Debug error: {e}")
        return None 