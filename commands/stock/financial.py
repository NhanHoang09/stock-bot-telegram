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
    
    # Đã loại bỏ hiệu ứng loading động, chỉ giữ lại typing
    loading_msg = None
    try:
        from vnstock import Finance
        finance = Finance(source='tcbs', symbol=symbol)
        financial_data = finance.ratio()
        income_data = finance.income_statement()
        balance_data = finance.balance_sheet()
        cashflow_data = finance.cash_flow()
        reply = f"📊 <b>CHỈ SỐ TÀI CHÍNH {symbol}:</b>\n\n"
        if not financial_data.empty:
            latest = financial_data.iloc[0]
            # === CHỈ TIÊU ĐỊNH GIÁ ===
            reply += "💰 <b>CHỈ TIÊU ĐỊNH GIÁ:</b>\n"
            reply += f"📉 P/E: {latest.get('price_to_earning', 'N/A')}\n"
            reply += f"📊 P/B: {latest.get('price_to_book', 'N/A')}\n"
            reply += f"📈 BVPS: {latest.get('book_value_per_share', 'N/A')}\n"
            reply += f"💰 EPS: {latest.get('earning_per_share', 'N/A')}\n"
            reply += f"💹 ROE: {latest.get('roe', 'N/A')}%\n"
            reply += f"💹 ROA: {latest.get('roa', 'N/A')}%\n"
            reply += f"💹 Gross Margin: {latest.get('gross_profit_margin', 'N/A')}%\n"
            reply += f"💹 Operating Margin: {latest.get('operating_profit_margin', 'N/A')}%\n"
            reply += f"💹 Net Margin: {latest.get('post_tax_margin', 'N/A')}%\n"
            reply += f"📊 Debt/Equity: {latest.get('debt_on_equity', 'N/A')}\n"
            reply += f"📊 Debt/Asset: {latest.get('debt_on_asset', 'N/A')}\n"
            reply += f"📊 Current Ratio: {latest.get('current_payment', 'N/A')}\n"
            reply += f"📊 Quick Ratio: {latest.get('quick_payment', 'N/A')}\n"
            reply += f"📊 Asset Turnover: {latest.get('revenue_on_asset', 'N/A')}\n"
            reply += f"📊 Days Receivable: {latest.get('days_receivable', 'N/A')}\n"
            reply += f"📊 Days Inventory: {latest.get('days_inventory', 'N/A')}\n"
            reply += f"📊 Days Payable: {latest.get('days_payable', 'N/A')}\n"
            reply += f"📊 EBITDA/Stock: {latest.get('ebitda_on_stock', 'N/A')}\n"
            reply += f"📊 EBITDA/Stock Change: {latest.get('ebitda_on_stock_change', 'N/A')}\n"
            reply += f"📊 Book Value/Share Change: {latest.get('book_value_per_share_change', 'N/A')}\n"
            # XÓA các dòng sau vì market_cap và outstanding_shares không còn đúng với dữ liệu TCBS
            # reply += f"📊 Market Cap: {format_vnd(market_cap)}₫\n"
            # outstanding_shares = safe_multiply(latest.get(('Chỉ tiêu định giá', 'Outstanding Share (Mil. Shares)'), 'N/A'), 1000000)
            # reply += f"📈 Outstanding Shares: {format_vnd(outstanding_shares)} cổ\n\n"
            # === CHỈ TIÊU KHẢ NĂNG SINH LỢI ===
            reply += "💹 <b>CHỈ TIÊU KHẢ NĂNG SINH LỢI:</b>\n"
            reply += f"💹 ROE: {latest.get('roe', 'N/A')}\n"
            reply += f"💹 ROA: {latest.get('roa', 'N/A')}\n"
            reply += f"💹 Gross Margin: {latest.get('gross_profit_margin', 'N/A')}\n"
            reply += f"💹 Net Margin: {latest.get('post_tax_margin', 'N/A')}\n"
            reply += f"💹 EBIT Margin: {latest.get('operating_profit_margin', 'N/A')}\n"
            latest_income = None
            if not income_data.empty:
                latest_income = income_data.iloc[0]
            reply += f"💰 EBITDA: {format_vnd(latest_income['ebitda']) if latest_income is not None and 'ebitda' in latest_income else 'N/A'}₫\n"
            reply += f"💰 EBIT: {format_vnd(latest_income['operation_profit']) if latest_income is not None and 'operation_profit' in latest_income else 'N/A'}₫\n"
            reply += f"💵 Dividend Yield: N/A\n"
            ebitda = safe_multiply(latest.get(('Chỉ tiêu khả năng sinh lợi', 'EBITDA (Bn. VND)'), 'N/A'), 1000000000)
            reply += f"💰 EBITDA: {format_vnd(ebitda)}₫\n"
            ebit = safe_multiply(latest.get(('Chỉ tiêu khả năng sinh lợi', 'EBIT (Bn. VND)'), 'N/A'), 1000000000)
            reply += f"💰 EBIT: {format_vnd(ebit)}₫\n\n"
            # === CHỈ TIÊU THANH KHOẢN ===
            reply += "💰 <b>CHỈ TIÊU THANH KHOẢN:</b>\n"
            reply += f"📊 Current Ratio: {latest.get('current_payment', 'N/A')}\n"
            reply += f"📊 Quick Ratio: {latest.get('quick_payment', 'N/A')}\n"
            reply += f"📊 Cash Ratio: {latest.get('cash_on_equity', 'N/A')}\n"
            reply += f"📊 Interest Coverage: {latest.get('ebit_on_interest', 'N/A')}\n"
            reply += f"📊 Financial Leverage: {latest.get('equity_on_liability', 'N/A')}\n"
            reply += f"📊 Interest Coverage: {latest.get('ebit_on_interest', 'N/A')}\n"
            reply += f"📊 Financial Leverage: {latest.get('equity_on_liability', 'N/A')}\n\n"
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
            reply += "📈 <b>BÁO CÁO THU NHẬP:</b>\n"
            reply += f"📈 Doanh thu: {format_vnd(latest_income.get('revenue', 'N/A'))}₫\n"
            reply += f"📈 Tăng trưởng doanh thu: {latest_income.get('year_revenue_growth', 'N/A')}%\n"
            reply += f"💰 Lợi nhuận gộp: {format_vnd(latest_income.get('gross_profit', 'N/A'))}₫\n"
            reply += f"📊 Lợi nhuận ròng: {format_vnd(latest_income.get('net_profit', 'N/A'))}₫\n"
            reply += f"📊 Lợi nhuận thuần: {format_vnd(latest_income.get('share_holder_income', 'N/A'))}₫\n"
            reply += f"📈 Tăng trưởng lợi nhuận: {latest_income.get('year_share_holder_income_growth', 'N/A')}%\n"
            reply += f"💵 EBITDA: {format_vnd(latest_income.get('ebitda', 'N/A'))}₫\n"
            reply += f"💵 Thu nhập tài chính: {format_vnd(latest_income.get('financial_income', 'N/A'))}₫\n"
            reply += f"💸 Chi phí lãi vay: {format_vnd(latest_income.get('interest_expenses', 'N/A'))}₫\n"
            reply += f"💸 Chi phí tài chính: {format_vnd(latest_income.get('financial_expenses', 'N/A'))}₫\n\n"
        # === BẢNG CÂN ĐỐI KẾ TOÁN ===
        if not balance_data.empty:
            latest_balance = balance_data.iloc[0]
            reply += "🏦 <b>BẢNG CÂN ĐỐI KẾ TOÁN:</b>\n"
            reply += f"🏦 Tài sản ngắn hạn: {format_vnd(latest_balance.get('short_asset', 'N/A'))}₫\n"
            reply += f"🏦 Tiền và tương đương: {format_vnd(latest_balance.get('cash', 'N/A'))}₫\n"
            reply += f"🏦 Đầu tư ngắn hạn: {format_vnd(latest_balance.get('short_invest', 'N/A'))}₫\n"
            reply += f"🏦 Tổng tài sản: {format_vnd(latest_balance.get('total_asset', 'N/A'))}₫\n"
            reply += f"📊 Tổng nợ phải trả: {format_vnd(latest_balance.get('liability', 'N/A'))}₫\n"
            reply += f"💎 Lợi nhuận chưa phân phối: {format_vnd(latest_balance.get('un_distributed_income', 'N/A'))}₫\n"
        # === BÁO CÁO LƯU CHUYỂN TIỀN TỆ ===
        if not cashflow_data.empty:
            latest_cashflow = cashflow_data.iloc[0]
            reply += "💸 <b>BÁO CÁO LƯU CHUYỂN TIỀN TỆ:</b>\n"
            reply += f"💰 Chi phí đầu tư: {format_vnd(latest_cashflow.get('invest_cost', 'N/A'))}₫\n"
            reply += f"💰 Lưu chuyển từ đầu tư: {format_vnd(latest_cashflow.get('from_invest', 'N/A'))}₫\n"
            reply += f"💰 Lưu chuyển từ tài chính: {format_vnd(latest_cashflow.get('from_financial', 'N/A'))}₫\n"
            reply += f"💰 Lưu chuyển từ bán hàng: {format_vnd(latest_cashflow.get('from_sale', 'N/A'))}₫\n"
            reply += f"💰 Dòng tiền tự do: {format_vnd(latest_cashflow.get('free_cash_flow', 'N/A'))}₫\n"
            reply += f"💰 Lưu chuyển tiền từ HĐKD: {format_vnd(latest_cashflow.get('net_cash_from_operating', 'N/A'))}₫\n"
            reply += f"💰 Lưu chuyển tiền từ HĐĐT: {format_vnd(latest_cashflow.get('net_cash_from_investing', 'N/A'))}₫\n"
            reply += f"💰 Lưu chuyển tiền từ HĐTC: {format_vnd(latest_cashflow.get('net_cash_from_financial', 'N/A'))}₫\n"
            reply += f"💰 Tăng/giảm tiền thuần: {format_vnd(latest_cashflow.get('net_increase_decrease_in_cash', 'N/A'))}₫\n"
            reply += f"💰 Tiền cuối kỳ: {format_vnd(latest_cashflow.get('cash_and_cash_equivalents_at_end_of_period', 'N/A'))}₫\n"
            reply += f"💵 Cổ tức đã trả: {format_vnd(latest_cashflow.get('dividends_paid', 'N/A'))}₫\n"
            reply += f"💵 Mua tài sản cố định: {format_vnd(latest_cashflow.get('purchase_of_fixed_assets', 'N/A'))}₫\n"
            reply += f"💵 Vay mượn: {format_vnd(latest_cashflow.get('proceeds_from_borrowings', 'N/A'))}₫\n"
            reply += f"💵 Trả nợ vay: {format_vnd(latest_cashflow.get('repayment_of_borrowings', 'N/A'))}₫\n"
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

