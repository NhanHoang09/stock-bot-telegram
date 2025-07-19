import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd
from utils.loading import (
    show_animated_loading, 
    update_loading_with_money_animation, 
    finish_loading, 
    finish_loading_with_error
)

def safe_multiply(value, multiplier):
    """Safely multiply values to prevent overflow"""
    if value == 'N/A' or value is None:
        return 'N/A'
    try:
        result = float(value) * multiplier
        if result > 1e18:  # Prevent overflow for very large numbers
            return 'N/A'
        return result
    except (ValueError, TypeError, OverflowError):
        return 'N/A'

async def financial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Chỉ số tài chính"""
    if not context.args:
        await update.message.reply_text("Vui lòng nhập: /financial <symbol>")
        return
    
    symbol = context.args[0].upper()
    
    # Hiển thị loading động
    loading_msg = await show_animated_loading(update, context, f"Đang lấy chỉ số tài chính cho {symbol}...")
    
    try:
        from vnstock import Finance
        
        # Cập nhật loading với animation tiền tệ
        await update_loading_with_money_animation(loading_msg, f"Đang lấy dữ liệu tài chính...", 1)
        
        finance = Finance(source='vci', symbol=symbol)
        
        # Lấy tất cả thông tin tài chính
        financial_data = finance.ratio()
        income_data = finance.income_statement()
        balance_data = finance.balance_sheet()
        cashflow_data = finance.cash_flow()
        
        reply = f"📊 <b>CHỈ SỐ TÀI CHÍNH {symbol}:</b>\n\n"
        
        if not financial_data.empty:
            latest = financial_data.iloc[0]
            
            # === CHỈ TIÊU ĐỊNH GIÁ ===
            reply += "💰 <b>CHỈ TIÊU ĐỊNH GIÁ:</b>\n"
            reply += f"📉 P/E: {latest.get(('Chỉ tiêu định giá', 'P/E'), 'N/A')}\n"
            reply += f"📊 P/B: {latest.get(('Chỉ tiêu định giá', 'P/B'), 'N/A')}\n"
            reply += f"📈 P/S: {latest.get(('Chỉ tiêu định giá', 'P/S'), 'N/A')}\n"
            reply += f"💵 P/Cash Flow: {latest.get(('Chỉ tiêu định giá', 'P/Cash Flow'), 'N/A')}\n"
            reply += f"🏢 EV/EBITDA: {latest.get(('Chỉ tiêu định giá', 'EV/EBITDA'), 'N/A')}\n"
            reply += f"💰 EPS: {format_vnd(latest.get(('Chỉ tiêu định giá', 'EPS (VND)'), 'N/A'))}₫\n"
            reply += f"📈 BVPS: {format_vnd(latest.get(('Chỉ tiêu định giá', 'BVPS (VND)'), 'N/A'))}₫\n"
            
            market_cap = safe_multiply(latest.get(('Chỉ tiêu định giá', 'Market Capital (Bn. VND)'), 'N/A'), 1000000000)
            reply += f"📊 Market Cap: {format_vnd(market_cap)}₫\n"
            
            outstanding_shares = safe_multiply(latest.get(('Chỉ tiêu định giá', 'Outstanding Share (Mil. Shares)'), 'N/A'), 1000000)
            reply += f"📈 Outstanding Shares: {format_vnd(outstanding_shares)} cổ\n\n"
            
            # === CHỈ TIÊU KHẢ NĂNG SINH LỢI ===
            reply += "💹 <b>CHỈ TIÊU KHẢ NĂNG SINH LỢI:</b>\n"
            reply += f"💹 ROE: {latest.get(('Chỉ tiêu khả năng sinh lợi', 'ROE (%)'), 'N/A')}%\n"
            reply += f"💹 ROA: {latest.get(('Chỉ tiêu khả năng sinh lợi', 'ROA (%)'), 'N/A')}%\n"
            reply += f"💹 ROIC: {latest.get(('Chỉ tiêu khả năng sinh lợi', 'ROIC (%)'), 'N/A')}%\n"
            reply += f"💹 Gross Margin: {latest.get(('Chỉ tiêu khả năng sinh lợi', 'Gross Profit Margin (%)'), 'N/A')}%\n"
            reply += f"💹 Net Margin: {latest.get(('Chỉ tiêu khả năng sinh lợi', 'Net Profit Margin (%)'), 'N/A')}%\n"
            reply += f"💹 EBIT Margin: {latest.get(('Chỉ tiêu khả năng sinh lợi', 'EBIT Margin (%)'), 'N/A')}%\n"
            reply += f"💵 Dividend Yield: {latest.get(('Chỉ tiêu khả năng sinh lợi', 'Dividend yield (%)'), 'N/A')}%\n"
            
            ebitda = safe_multiply(latest.get(('Chỉ tiêu khả năng sinh lợi', 'EBITDA (Bn. VND)'), 'N/A'), 1000000000)
            reply += f"💰 EBITDA: {format_vnd(ebitda)}₫\n"
            
            ebit = safe_multiply(latest.get(('Chỉ tiêu khả năng sinh lợi', 'EBIT (Bn. VND)'), 'N/A'), 1000000000)
            reply += f"💰 EBIT: {format_vnd(ebit)}₫\n\n"
            
            # === CHỈ TIÊU THANH KHOẢN ===
            reply += "💰 <b>CHỈ TIÊU THANH KHOẢN:</b>\n"
            reply += f"📊 Current Ratio: {latest.get(('Chỉ tiêu thanh khoản', 'Current Ratio'), 'N/A')}\n"
            reply += f"📊 Quick Ratio: {latest.get(('Chỉ tiêu thanh khoản', 'Quick Ratio'), 'N/A')}\n"
            reply += f"📊 Cash Ratio: {latest.get(('Chỉ tiêu thanh khoản', 'Cash Ratio'), 'N/A')}\n"
            reply += f"📊 Interest Coverage: {latest.get(('Chỉ tiêu thanh khoản', 'Interest Coverage'), 'N/A')}\n"
            reply += f"📊 Financial Leverage: {latest.get(('Chỉ tiêu thanh khoản', 'Financial Leverage'), 'N/A')}\n\n"
            
            # === CHỈ TIÊU CƠ CẤU NGUỒN VỐN ===
            reply += "🏗️ <b>CƠ CẤU NGUỒN VỐN:</b>\n"
            reply += f"📊 Debt/Equity: {latest.get(('Chỉ tiêu cơ cấu nguồn vốn', 'Debt/Equity'), 'N/A')}\n"
            reply += f"📊 (ST+LT borrowings)/Equity: {latest.get(('Chỉ tiêu cơ cấu nguồn vốn', '(ST+LT borrowings)/Equity'), 'N/A')}\n"
            reply += f"📊 Fixed Asset-To-Equity: {latest.get(('Chỉ tiêu cơ cấu nguồn vốn', 'Fixed Asset-To-Equity'), 'N/A')}\n"
            reply += f"📊 Owners' Equity/Charter Capital: {latest.get(('Chỉ tiêu cơ cấu nguồn vốn', 'Owners Equity/Charter Capital'), 'N/A')}\n\n"
            
            # === CHỈ TIÊU HIỆU QUẢ HOẠT ĐỘNG ===
            reply += "⚡ <b>HIỆU QUẢ HOẠT ĐỘNG:</b>\n"
            reply += f"🔄 Asset Turnover: {latest.get(('Chỉ tiêu hiệu quả hoạt động', 'Asset Turnover'), 'N/A')}\n"
            reply += f"🔄 Fixed Asset Turnover: {latest.get(('Chỉ tiêu hiệu quả hoạt động', 'Fixed Asset Turnover'), 'N/A')}\n"
            reply += f"🔄 Inventory Turnover: {latest.get(('Chỉ tiêu hiệu quả hoạt động', 'Inventory Turnover'), 'N/A')}\n"
            reply += f"📅 Days Sales Outstanding: {latest.get(('Chỉ tiêu hiệu quả hoạt động', 'Days Sales Outstanding'), 'N/A')} ngày\n"
            reply += f"📅 Days Inventory Outstanding: {latest.get(('Chỉ tiêu hiệu quả hoạt động', 'Days Inventory Outstanding'), 'N/A')} ngày\n"
            reply += f"📅 Days Payable Outstanding: {latest.get(('Chỉ tiêu hiệu quả hoạt động', 'Days Payable Outstanding'), 'N/A')} ngày\n"
            reply += f"📅 Cash Cycle: {latest.get(('Chỉ tiêu hiệu quả hoạt động', 'Cash Cycle'), 'N/A')} ngày\n\n"
        
        # === BÁO CÁO THU NHẬP ===
        if not income_data.empty:
            latest_income = income_data.iloc[0]
            reply += "📈 <b>BÁO CÁO THU NHẬP (Q1 2025):</b>\n"
            
            revenue = safe_multiply(latest_income.get('Revenue (Bn. VND)', 'N/A'), 1000000000)
            reply += f"📈 Doanh thu: {format_vnd(revenue)}₫\n"
            
            reply += f"📈 Tăng trưởng doanh thu: {latest_income.get('Revenue YoY (%)', 'N/A')}%\n"
            reply += f"💰 Lợi nhuận gộp: {format_vnd(latest_income.get('Gross Profit', 'N/A'))}₫\n"
            reply += f"📊 Lợi nhuận ròng: {format_vnd(latest_income.get('Net Profit For the Year', 'N/A'))}₫\n"
            reply += f"📊 Lợi nhuận thuần: {format_vnd(latest_income.get('Attributable to parent company', 'N/A'))}₫\n"
            reply += f"📊 Tăng trưởng lợi nhuận: {latest_income.get('Attribute to parent company YoY (%)', 'N/A')}%\n"
            reply += f"💵 Thu nhập tài chính: {format_vnd(latest_income.get('Financial Income', 'N/A'))}₫\n"
            reply += f"💸 Chi phí lãi vay: {format_vnd(latest_income.get('Interest Expenses', 'N/A'))}₫\n"
            reply += f"💸 Chi phí tài chính: {format_vnd(latest_income.get('Financial Expenses', 'N/A'))}₫\n\n"
        
        # === BẢNG CÂN ĐỐI KẾ TOÁN ===
        if not balance_data.empty:
            latest_balance = balance_data.iloc[0]
            reply += "🏦 <b>BẢNG CÂN ĐỐI KẾ TOÁN:</b>\n"
            
            total_assets = safe_multiply(latest_balance.get('TOTAL ASSETS (Bn. VND)', 'N/A'), 1000000000)
            reply += f"💰 Tổng tài sản: {format_vnd(total_assets)}₫\n"
            
            current_assets = safe_multiply(latest_balance.get('CURRENT ASSETS (Bn. VND)', 'N/A'), 1000000000)
            reply += f"💰 Tài sản ngắn hạn: {format_vnd(current_assets)}₫\n"
            
            long_term_assets = safe_multiply(latest_balance.get('LONG-TERM ASSETS (Bn. VND)', 'N/A'), 1000000000)
            reply += f"💰 Tài sản dài hạn: {format_vnd(long_term_assets)}₫\n"
            
            cash_equivalents = safe_multiply(latest_balance.get('Cash and cash equivalents (Bn. VND)', 'N/A'), 1000000000)
            reply += f"💰 Tiền và tương đương: {format_vnd(cash_equivalents)}₫\n"
            
            fixed_assets = safe_multiply(latest_balance.get('Fixed assets (Bn. VND)', 'N/A'), 1000000000)
            reply += f"💰 Tài sản cố định: {format_vnd(fixed_assets)}₫\n"
            
            total_liabilities = safe_multiply(latest_balance.get('LIABILITIES (Bn. VND)', 'N/A'), 1000000000)
            reply += f"📊 Tổng nợ phải trả: {format_vnd(total_liabilities)}₫\n"
            
            current_liabilities = safe_multiply(latest_balance.get('Current liabilities (Bn. VND)', 'N/A'), 1000000000)
            reply += f"📊 Nợ ngắn hạn: {format_vnd(current_liabilities)}₫\n"
            
            long_term_liabilities = safe_multiply(latest_balance.get('Long-term liabilities (Bn. VND)', 'N/A'), 1000000000)
            reply += f"📊 Nợ dài hạn: {format_vnd(long_term_liabilities)}₫\n"
            
            owners_equity = safe_multiply(latest_balance.get('OWNERS EQUITY(Bn.VND)', 'N/A'), 1000000000)
            reply += f"💎 Vốn chủ sở hữu: {format_vnd(owners_equity)}₫\n"
            
            capital_reserves = safe_multiply(latest_balance.get('Capital and reserves (Bn. VND)', 'N/A'), 1000000000)
            reply += f"💎 Vốn và quỹ: {format_vnd(capital_reserves)}₫\n"
            
            undistributed_earnings = safe_multiply(latest_balance.get('Undistributed earnings (Bn. VND)', 'N/A'), 1000000000)
            reply += f"💎 Lợi nhuận chưa phân phối: {format_vnd(undistributed_earnings)}₫\n\n"
        
        # === BÁO CÁO LƯU CHUYỂN TIỀN TỆ ===
        if not cashflow_data.empty:
            latest_cashflow = cashflow_data.iloc[0]
            reply += "💸 <b>BÁO CÁO LƯU CHUYỂN TIỀN TỆ:</b>\n"
            reply += f"💰 Lưu chuyển tiền từ HĐKD: {format_vnd(latest_cashflow.get('Net cash inflows/outflows from operating activities', 'N/A'))}₫\n"
            reply += f"💰 Lưu chuyển tiền từ HĐĐT: {format_vnd(latest_cashflow.get('Net Cash Flows from Investing Activities', 'N/A'))}₫\n"
            reply += f"💰 Lưu chuyển tiền từ HĐTC: {format_vnd(latest_cashflow.get('Cash flows from financial activities', 'N/A'))}₫\n"
            reply += f"💰 Tăng/giảm tiền thuần: {format_vnd(latest_cashflow.get('Net increase/decrease in cash and cash equivalents', 'N/A'))}₫\n"
            reply += f"💰 Tiền cuối kỳ: {format_vnd(latest_cashflow.get('Cash and Cash Equivalents at the end of period', 'N/A'))}₫\n"
            reply += f"💵 Cổ tức đã trả: {format_vnd(latest_cashflow.get('Dividends paid', 'N/A'))}₫\n"
            reply += f"💵 Mua tài sản cố định: {format_vnd(latest_cashflow.get('Purchase of fixed assets', 'N/A'))}₫\n"
            reply += f"💵 Vay mượn: {format_vnd(latest_cashflow.get('Proceeds from borrowings', 'N/A'))}₫\n"
            reply += f"💵 Trả nợ vay: {format_vnd(latest_cashflow.get('Repayment of borrowings', 'N/A'))}₫\n"
        
        await finish_loading(loading_msg, reply)
    except Exception as e:
        await finish_loading_with_error(loading_msg, f"Có lỗi xảy ra: {e}")

