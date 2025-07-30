import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd
from utils.loading import show_animated_loading, finish_loading
import pandas as pd
from datetime import datetime, timedelta

async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Phân tích tổng hợp chứng khoán"""
    if not context.args:
        await update.message.reply_text("Vui lòng nhập: /analysis <symbol> [start_date] [end_date]\nVí dụ: /analysis VNM 2023-01-01 2024-12-31")
        return
    
    symbol = context.args[0].upper()
    
    # Xử lý thời gian từ message hoặc mặc định 1 năm
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Nếu có thêm tham số thời gian
    if len(context.args) >= 2:
        try:
            start_date = datetime.strptime(context.args[1], '%Y-%m-%d')
        except ValueError:
            await update.message.reply_text("Định dạng ngày không đúng. Sử dụng: YYYY-MM-DD")
            return
    
    if len(context.args) >= 3:
        try:
            end_date = datetime.strptime(context.args[2], '%Y-%m-%d')
        except ValueError:
            await update.message.reply_text("Định dạng ngày không đúng. Sử dụng: YYYY-MM-DD")
            return
    
    # Format dates cho API
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    # Hiển thị loading
    loading_msg = await show_animated_loading(update, context, f"Đang phân tích tổng hợp {symbol} từ {start_str} đến {end_str}...")
    
    try:
        from vnstock import Trading, Finance, Company
        from vnstock import Vnstock
        
        # Lấy dữ liệu từ nhiều nguồn
        trading = Trading(source='TCBS')
        price_data = trading.price_board([symbol])
        price_info = price_data.iloc[0] if price_data is not None and hasattr(price_data, 'empty') and not price_data.empty else None
        
        finance = Finance(source='tcbs', symbol=symbol)
        financial_data = finance.ratio()
        income_data = finance.income_statement()
        
        company = Company()
        company.symbol = symbol
        dividends = company.dividends()
        
        # Lấy dữ liệu lịch sử cho phân tích kỹ thuật
        try:
            stock = Vnstock().stock(symbol=symbol, source='TCBS')
            hist_data = stock.quote.history(symbol=symbol, start=start_str, end=end_str)
        except Exception:
            hist_data = None
        
        reply = f"🔍 <b>PHÂN TÍCH TỔNG HỢP: {symbol}</b>\n\n"
        
        # === PHÂN TÍCH ĐỊNH GIÁ ===
        reply += "💰 <b>PHÂN TÍCH ĐỊNH GIÁ:</b>\n"
        if financial_data is not None and hasattr(financial_data, 'empty') and not financial_data.empty:
            latest = financial_data.iloc[0]
            current_price = price_info.get('Giá', 0) if price_info is not None else 0
            
            # Tính các chỉ số định giá
            pe = latest.get('price_to_earning', 0)
            pb = latest.get('price_to_book', 0)
            roe = latest.get('roe', 0)
            eps = latest.get('earning_per_share', 0)
            
            # Đánh giá P/E
            pe_rating = "🟢 Thấp" if pe < 15 else "🟡 Trung bình" if pe < 25 else "🔴 Cao"
            reply += f"📊 P/E: {pe:.2f} {pe_rating}\n"
            
            # Đánh giá P/B
            pb_rating = "🟢 Thấp" if pb < 1.5 else "🟡 Trung bình" if pb < 3 else "🔴 Cao"
            reply += f"📊 P/B: {pb:.2f} {pb_rating}\n"
            
            # Đánh giá ROE
            roe_rating = "🟢 Tốt" if roe > 0.15 else "🟡 Trung bình" if roe > 0.10 else "🔴 Thấp"
            reply += f"📊 ROE: {roe*100:.1f}% {roe_rating}\n"
            
            # PEG Ratio (P/E Growth)
            eps_growth = latest.get('eps_change', 0)
            peg = pe / (eps_growth * 100) if eps_growth is not None and eps_growth != 0 else "N/A"
            peg_rating = "🟢 Tốt" if isinstance(peg, (int, float)) and peg < 1 else "🟡 Trung bình" if isinstance(peg, (int, float)) and peg < 1.5 else "🔴 Cao"
            reply += f"📊 PEG: {peg:.2f} {peg_rating}\n" if isinstance(peg, (int, float)) else f"📊 PEG: {peg} {peg_rating}\n"
        
        reply += "\n"
        
        # === PHÂN TÍCH TĂNG TRƯỞNG ===
        reply += "📈 <b>PHÂN TÍCH TĂNG TRƯỞNG:</b>\n"
        if income_data is not None and hasattr(income_data, 'empty') and not income_data.empty:
            latest_income = income_data.iloc[0]
            
            revenue_growth = latest_income.get('year_revenue_growth', 0) * 100
            profit_growth = latest_income.get('year_share_holder_income_growth', 0) * 100
            
            # Đánh giá tăng trưởng doanh thu
            revenue_rating = "🟢 Tốt" if revenue_growth > 10 else "🟡 Trung bình" if revenue_growth > 5 else "🔴 Thấp"
            reply += f"📈 Revenue Growth: {revenue_growth:.1f}% {revenue_rating}\n"
            
            # Đánh giá tăng trưởng lợi nhuận
            profit_rating = "🟢 Tốt" if profit_growth > 15 else "🟡 Trung bình" if profit_growth > 8 else "🔴 Thấp"
            reply += f"📈 Profit Growth: {profit_growth:.1f}% {profit_rating}\n"
            
            # Chất lượng tăng trưởng
            quality = "🟢 Tốt" if profit_growth > revenue_growth else "🟡 Trung bình" if profit_growth > revenue_growth * 0.8 else "🔴 Kém"
            reply += f"📈 Growth Quality: {quality}\n"
        
        reply += "\n"
        
        # === PHÂN TÍCH RỦI RO ===
        reply += "⚠️ <b>PHÂN TÍCH RỦI RO:</b>\n"
        if financial_data is not None and hasattr(financial_data, 'empty') and not financial_data.empty:
            debt_equity = latest.get('debt_on_equity', 0)
            current_ratio = latest.get('current_payment', 0)
            interest_coverage = latest.get('ebit_on_interest', 0)
            
            # Đánh giá rủi ro nợ
            debt_rating = "🟢 Thấp" if debt_equity < 0.5 else "🟡 Trung bình" if debt_equity < 1 else "🔴 Cao"
            reply += f"📊 Debt Risk: {debt_equity:.2f} {debt_rating}\n"
            
            # Đánh giá thanh khoản
            liquidity_rating = "🟢 Tốt" if current_ratio > 2 else "🟡 Trung bình" if current_ratio > 1.5 else "🔴 Thấp"
            reply += f"📊 Liquidity: {current_ratio:.2f} {liquidity_rating}\n"
            
            # Đánh giá khả năng trả lãi
            interest_rating = "🟢 Tốt" if interest_coverage > 3 else "🟡 Trung bình" if interest_coverage > 1.5 else "🔴 Thấp"
            reply += f"📊 Interest Coverage: {interest_coverage:.1f}x {interest_rating}\n"
        
        reply += "\n"
        
        # === PHÂN TÍCH KỸ THUẬT CƠ BẢN ===
        reply += "📊 <b>PHÂN TÍCH KỸ THUẬT:</b>\n"
        if (price_info is not None and isinstance(price_info, pd.Series) and 
            hist_data is not None and hasattr(hist_data, 'empty') and not hist_data.empty):
            current_price = price_info.get('Giá', 0)
            high_1y = price_info.get('Đỉnh 1Y', 0)
            low_1y = price_info.get('Đáy 1Y', 0)
            
            # Tính % từ đỉnh và đáy
            from_high = ((current_price - high_1y) / high_1y) * 100 if high_1y is not None and high_1y != 0 else 0
            from_low = ((current_price - low_1y) / low_1y) * 100 if low_1y is not None and low_1y != 0 else 0
            
            # Đánh giá vị trí giá
            if from_high > -10:
                price_position = "🟢 Gần đỉnh"
            elif from_low < 20:
                price_position = "🔴 Gần đáy"
            else:
                price_position = "🟡 Trung bình"
            
            reply += f"📈 Price Position: {price_position}\n"
            reply += f"📈 From 1Y High: {from_high:.1f}%\n"
            reply += f"📈 From 1Y Low: {from_low:.1f}%\n"
            
            # Tính biến động
            if hasattr(hist_data, '__len__') and len(hist_data) > 20:
                recent_prices = hist_data['close'].tail(20)
                volatility = (recent_prices.max() - recent_prices.min()) / recent_prices.mean() * 100
                vol_rating = "🟢 Thấp" if volatility < 10 else "🟡 Trung bình" if volatility < 20 else "🔴 Cao"
                reply += f"📊 Volatility (20D): {volatility:.1f}% {vol_rating}\n"
        
        reply += "\n"
        
        # === KHUYẾN NGHỊ TỔNG HỢP ===
        reply += "🎯 <b>KHUYẾN NGHỊ:</b>\n"
        
        # Tính điểm tổng hợp
        score = 0
        reasons = []
        
        if financial_data is not None and hasattr(financial_data, 'empty') and not financial_data.empty:
            latest = financial_data.iloc[0]
            pe = latest.get('price_to_earning', 0)
            pb = latest.get('price_to_book', 0)
            roe = latest.get('roe', 0)
            
            # Điểm định giá
            if pe < 15: score += 2; reasons.append("P/E thấp")
            elif pe < 25: score += 1
            else: score -= 1; reasons.append("P/E cao")
            
            if pb < 1.5: score += 2; reasons.append("P/B thấp")
            elif pb < 3: score += 1
            else: score -= 1; reasons.append("P/B cao")
            
            if roe > 0.15: score += 2; reasons.append("ROE cao")
            elif roe > 0.10: score += 1
            else: score -= 1; reasons.append("ROE thấp")
        
        if income_data is not None and hasattr(income_data, 'empty') and not income_data.empty:
            latest_income = income_data.iloc[0]
            revenue_growth = latest_income.get('year_revenue_growth', 0) * 100
            profit_growth = latest_income.get('year_share_holder_income_growth', 0) * 100
            
            # Điểm tăng trưởng
            if revenue_growth > 10: score += 2; reasons.append("Tăng trưởng tốt")
            elif revenue_growth > 5: score += 1
            else: score -= 1; reasons.append("Tăng trưởng chậm")
            
            if profit_growth > revenue_growth: score += 1; reasons.append("Chất lượng tăng trưởng tốt")
            else: score -= 1; reasons.append("Chất lượng tăng trưởng kém")
        
        # Đánh giá tổng thể
        if score >= 6:
            recommendation = "🟢 MUA"
            confidence = "Cao"
        elif score >= 3:
            recommendation = "🟡 GIỮ"
            confidence = "Trung bình"
        else:
            recommendation = "🔴 BÁN"
            confidence = "Thấp"
        
        reply += f"📊 Recommendation: {recommendation}\n"
        reply += f"📊 Confidence: {confidence}\n"
        reply += f"📊 Score: {score}/10\n"
        reply += f"📊 Reasons: {', '.join(reasons[:3])}\n"
        
        await finish_loading(loading_msg, reply, parse_mode='HTML')
        
    except Exception as e:
        await finish_loading(loading_msg, f"Có lỗi xảy ra: {e}")