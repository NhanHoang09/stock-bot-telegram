import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd
from utils.loading import show_animated_loading, finish_loading

async def compare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """So sánh 2 mã chứng khoán"""
    if len(context.args) < 2:
        await update.message.reply_text("Vui lòng nhập: /compare <symbol1> <symbol2>")
        return
    
    symbol1 = context.args[0].upper()
    symbol2 = context.args[1].upper()
    
    # Hiển thị loading
    loading_msg = await show_animated_loading(update, context, f"Đang so sánh {symbol1} vs {symbol2}...")
    
    try:
        from vnstock import Trading, Finance, Company
        
        # Lấy dữ liệu cho cả 2 mã
        trading = Trading(source='TCBS')
        price_data = trading.price_board([symbol1, symbol2])
        
        # Tách dữ liệu cho từng mã
        price1 = price_data[price_data['Mã CP'] == symbol1].iloc[0] if not price_data[price_data['Mã CP'] == symbol1].empty else None
        price2 = price_data[price_data['Mã CP'] == symbol2].iloc[0] if not price_data[price_data['Mã CP'] == symbol2].empty else None
        
        # Lấy dữ liệu tài chính
        finance1 = Finance(source='tcbs', symbol=symbol1)
        finance2 = Finance(source='tcbs', symbol=symbol2)
        
        financial_data1 = finance1.ratio()
        financial_data2 = finance2.ratio()
        
        income_data1 = finance1.income_statement()
        income_data2 = finance2.income_statement()
        
        # Lấy thông tin công ty
        company1 = Company()
        company1.symbol = symbol1
        company2 = Company()
        company2.symbol = symbol2
        
        dividends1 = company1.dividends()
        dividends2 = company2.dividends()
        
        reply = f"⚖️ <b>SO SÁNH: {symbol1} vs {symbol2}</b>\n\n"
        
        # === SO SÁNH GIÁ ===
        reply += "💰 <b>SO SÁNH GIÁ:</b>\n"
        if price1 is not None and price2 is not None:
            price1_val = price1.get('Giá', 0)
            price2_val = price2.get('Giá', 0)
            
            reply += f"📊 {symbol1}: {format_vnd(price1_val)}₫\n"
            reply += f"📊 {symbol2}: {format_vnd(price2_val)}₫\n"
            
            # Tính % chênh lệch
            if price1_val > 0 and price2_val > 0:
                diff_pct = ((price1_val - price2_val) / price2_val) * 100
                if diff_pct > 0:
                    reply += f"📈 {symbol1} cao hơn {symbol2}: +{diff_pct:.1f}%\n"
                else:
                    reply += f"📉 {symbol1} thấp hơn {symbol2}: {diff_pct:.1f}%\n"
        
        reply += "\n"
        
        # === SO SÁNH ĐỊNH GIÁ ===
        reply += "📊 <b>SO SÁNH ĐỊNH GIÁ:</b>\n"
        if (financial_data1 is not None and hasattr(financial_data1, 'empty') and not financial_data1.empty and 
            financial_data2 is not None and hasattr(financial_data2, 'empty') and not financial_data2.empty):
            fin1 = financial_data1.iloc[0]
            fin2 = financial_data2.iloc[0]
            
            # P/E
            pe1 = fin1.get('price_to_earning', 0)
            pe2 = fin2.get('price_to_earning', 0)
            reply += f"📊 P/E: {symbol1}={pe1:.2f} | {symbol2}={pe2:.2f}\n"
            
            # P/B
            pb1 = fin1.get('price_to_book', 0)
            pb2 = fin2.get('price_to_book', 0)
            reply += f"📊 P/B: {symbol1}={pb1:.2f} | {symbol2}={pb2:.2f}\n"
            
            # ROE
            roe1 = fin1.get('roe', 0) * 100
            roe2 = fin2.get('roe', 0) * 100
            reply += f"📊 ROE: {symbol1}={roe1:.1f}% | {symbol2}={roe2:.1f}%\n"
            
            # EPS
            eps1 = fin1.get('earning_per_share', 0)
            eps2 = fin2.get('earning_per_share', 0)
            reply += f"📊 EPS: {symbol1}={format_vnd(eps1)}₫ | {symbol2}={format_vnd(eps2)}₫\n"
        
        reply += "\n"
        
        # === SO SÁNH TĂNG TRƯỞNG ===
        reply += "📈 <b>SO SÁNH TĂNG TRƯỞNG:</b>\n"
        if (income_data1 is not None and hasattr(income_data1, 'empty') and not income_data1.empty and 
            income_data2 is not None and hasattr(income_data2, 'empty') and not income_data2.empty):
            inc1 = income_data1.iloc[0]
            inc2 = income_data2.iloc[0]
            
            # Tăng trưởng doanh thu
            rev_growth1 = inc1.get('year_revenue_growth', 0) * 100
            rev_growth2 = inc2.get('year_revenue_growth', 0) * 100
            reply += f"📈 Revenue Growth: {symbol1}={rev_growth1:.1f}% | {symbol2}={rev_growth2:.1f}%\n"
            
            # Tăng trưởng lợi nhuận
            profit_growth1 = inc1.get('year_share_holder_income_growth', 0) * 100
            profit_growth2 = inc2.get('year_share_holder_income_growth', 0) * 100
            reply += f"📈 Profit Growth: {symbol1}={profit_growth1:.1f}% | {symbol2}={profit_growth2:.1f}%\n"
            
            # EBITDA
            ebitda1 = inc1.get('ebitda', 0)
            ebitda2 = inc2.get('ebitda', 0)
            reply += f"📈 EBITDA: {symbol1}={format_vnd(ebitda1)}₫ | {symbol2}={format_vnd(ebitda2)}₫\n"
        
        reply += "\n"
        
        # === SO SÁNH RỦI RO ===
        reply += "⚠️ <b>SO SÁNH RỦI RO:</b>\n"
        if (financial_data1 is not None and hasattr(financial_data1, 'empty') and not financial_data1.empty and 
            financial_data2 is not None and hasattr(financial_data2, 'empty') and not financial_data2.empty):
            # Debt/Equity
            debt_equity1 = fin1.get('debt_on_equity', 0)
            debt_equity2 = fin2.get('debt_on_equity', 0)
            reply += f"📊 Debt/Equity: {symbol1}={debt_equity1:.2f} | {symbol2}={debt_equity2:.2f}\n"
            
            # Current Ratio
            current1 = fin1.get('current_payment', 0)
            current2 = fin2.get('current_payment', 0)
            reply += f"📊 Current Ratio: {symbol1}={current1:.2f} | {symbol2}={current2:.2f}\n"
            
            # Interest Coverage
            interest1 = fin1.get('ebit_on_interest', 0)
            interest2 = fin2.get('ebit_on_interest', 0)
            reply += f"📊 Interest Coverage: {symbol1}={interest1:.1f}x | {symbol2}={interest2:.1f}x\n"
        
        reply += "\n"
        
        # === SO SÁNH CỔ TỨC ===
        reply += "💵 <b>SO SÁNH CỔ TỨC:</b>\n"
        try:
            latest_cash1 = dividends1[dividends1['issue_method'] == 'cash'].iloc[0] if not dividends1[dividends1['issue_method'] == 'cash'].empty else None
            latest_cash2 = dividends2[dividends2['issue_method'] == 'cash'].iloc[0] if not dividends2[dividends2['issue_method'] == 'cash'].empty else None
            
            if latest_cash1 is not None and latest_cash2 is not None:
                div1 = latest_cash1['cash_dividend_percentage'] * 100
                div2 = latest_cash2['cash_dividend_percentage'] * 100
                reply += f"💵 Dividend Yield: {symbol1}={div1:.2f}% | {symbol2}={div2:.2f}%\n"
            else:
                reply += f"💵 Dividend Yield: {symbol1}=N/A | {symbol2}=N/A\n"
        except Exception:
            reply += f"💵 Dividend Yield: {symbol1}=N/A | {symbol2}=N/A\n"
        
        reply += "\n"
        
        # === KHUYẾN NGHỊ SO SÁNH ===
        reply += "🎯 <b>KHUYẾN NGHỊ SO SÁNH:</b>\n"
        
        if (financial_data1 is not None and hasattr(financial_data1, 'empty') and not financial_data1.empty and 
            financial_data2 is not None and hasattr(financial_data2, 'empty') and not financial_data2.empty):
            # Tính điểm cho từng mã
            score1 = 0
            score2 = 0
            
            # Điểm định giá (P/E thấp hơn = tốt hơn)
            if pe1 < pe2: score1 += 1
            else: score2 += 1
            
            # Điểm ROE (ROE cao hơn = tốt hơn)
            if roe1 > roe2: score1 += 1
            else: score2 += 1
            
            # Điểm tăng trưởng
            if rev_growth1 > rev_growth2: score1 += 1
            else: score2 += 1
            
            if profit_growth1 > profit_growth2: score1 += 1
            else: score2 += 1
            
            # Điểm rủi ro (debt thấp hơn = tốt hơn)
            if debt_equity1 < debt_equity2: score1 += 1
            else: score2 += 1
            
            # Kết luận
            if score1 > score2:
                winner = symbol1
                winner_score = score1
                loser_score = score2
            elif score2 > score1:
                winner = symbol2
                winner_score = score2
                loser_score = score1
            else:
                winner = "Hòa"
                winner_score = score1
                loser_score = score2
            
            reply += f"🏆 Winner: {winner}\n"
            reply += f"📊 Score: {symbol1}={score1} | {symbol2}={score2}\n"
            
            # Lý do
            reasons = []
            if pe1 < pe2: reasons.append(f"{symbol1} có P/E thấp hơn")
            if roe1 > roe2: reasons.append(f"{symbol1} có ROE cao hơn")
            if rev_growth1 > rev_growth2: reasons.append(f"{symbol1} tăng trưởng doanh thu tốt hơn")
            if debt_equity1 < debt_equity2: reasons.append(f"{symbol1} ít rủi ro nợ hơn")
            
            if reasons:
                reply += f"📋 Reasons: {', '.join(reasons[:2])}\n"
        
        await finish_loading(loading_msg, reply, parse_mode='HTML')
        
    except Exception as e:
        await finish_loading(loading_msg, f"Có lỗi xảy ra: {e}")