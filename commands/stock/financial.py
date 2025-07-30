import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd
from utils.loading import (
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
            reply += f"📉 P/E: {latest.get('price_to_earning', 'N/A')}\n"  # Tỷ lệ P/E - Giá cổ phiếu trên thu nhập mỗi cổ phiếu
            reply += f"📊 P/B: {latest.get('price_to_book', 'N/A')}\n"  # Tỷ lệ P/B - Giá cổ phiếu trên giá trị sổ sách
            reply += f"📈 BVPS: {latest.get('book_value_per_share', 'N/A')}\n"  # Giá trị sổ sách mỗi cổ phiếu
            reply += f"💰 EPS: {latest.get('earning_per_share', 'N/A')}\n"  # Thu nhập mỗi cổ phiếu
            reply += f"💹 ROE: {latest.get('roe', 'N/A')}%\n"  # Tỷ suất sinh lời trên vốn chủ sở hữu
            reply += f"💹 ROA: {latest.get('roa', 'N/A')}%\n"  # Tỷ suất sinh lời trên tài sản
            reply += f"💹 Gross Margin: {latest.get('gross_profit_margin', 'N/A')}%\n"  # Tỷ suất lợi nhuận gộp
            reply += f"💹 Operating Margin: {latest.get('operating_profit_margin', 'N/A')}%\n"  # Tỷ suất lợi nhuận hoạt động
            reply += f"💹 Net Margin: {latest.get('post_tax_margin', 'N/A')}%\n"  # Tỷ suất lợi nhuận ròng
            reply += f"📊 Debt/Equity: {latest.get('debt_on_equity', 'N/A')}\n"  # Tỷ lệ nợ trên vốn chủ sở hữu
            reply += f"📊 Debt/Asset: {latest.get('debt_on_asset', 'N/A')}\n"  # Tỷ lệ nợ trên tài sản
            reply += f"📊 Current Ratio: {latest.get('current_payment', 'N/A')}\n"  # Tỷ lệ thanh toán hiện hành
            reply += f"📊 Quick Ratio: {latest.get('quick_payment', 'N/A')}\n"  # Tỷ lệ thanh toán nhanh
            reply += f"📊 Asset Turnover: {latest.get('revenue_on_asset', 'N/A')}\n"  # Vòng quay tài sản
            reply += f"📊 Days Receivable: {latest.get('days_receivable', 'N/A')}\n"  # Số ngày thu tiền bình quân
            reply += f"📊 Days Inventory: {latest.get('days_inventory', 'N/A')}\n"  # Số ngày tồn kho bình quân
            reply += f"📊 Days Payable: {latest.get('days_payable', 'N/A')}\n"  # Số ngày trả nợ bình quân
            reply += f"📊 EBITDA/Stock: {latest.get('ebitda_on_stock', 'N/A')}\n"  # EBITDA trên mỗi cổ phiếu
            reply += f"📊 EBITDA/Stock Change: {latest.get('ebitda_on_stock_change', 'N/A')}\n"  # Thay đổi EBITDA trên cổ phiếu
            reply += f"📊 Book Value/Share Change: {latest.get('book_value_per_share_change', 'N/A')}\n"  # Thay đổi giá trị sổ sách mỗi cổ phiếu
            # XÓA các dòng sau vì market_cap và outstanding_shares không còn đúng với dữ liệu TCBS
            # reply += f"📊 Market Cap: {format_vnd(market_cap)}₫\n"
            # outstanding_shares = safe_multiply(latest.get(('Chỉ tiêu định giá', 'Outstanding Share (Mil. Shares)'), 'N/A'), 1000000)
            # reply += f"📈 Outstanding Shares: {format_vnd(outstanding_shares)} cổ\n\n"
            # === CHỈ TIÊU KHẢ NĂNG SINH LỢI ===
            reply += "💹 <b>CHỈ TIÊU KHẢ NĂNG SINH LỢI:</b>\n"
            reply += f"💹 ROE: {latest.get('roe', 'N/A')}\n"  # Tỷ suất sinh lời trên vốn chủ sở hữu
            reply += f"💹 ROA: {latest.get('roa', 'N/A')}\n"  # Tỷ suất sinh lời trên tài sản
            reply += f"💹 Gross Margin: {latest.get('gross_profit_margin', 'N/A')}\n"  # Tỷ suất lợi nhuận gộp
            reply += f"💹 Net Margin: {latest.get('post_tax_margin', 'N/A')}\n"  # Tỷ suất lợi nhuận ròng
            reply += f"💹 EBIT Margin: {latest.get('operating_profit_margin', 'N/A')}\n"  # Tỷ suất lợi nhuận trước lãi vay và thuế
            latest_income = None
            if not income_data.empty:
                latest_income = income_data.iloc[0]
            reply += f"💰 EBITDA: {format_vnd(latest_income['ebitda']) if latest_income is not None and 'ebitda' in latest_income else 'N/A'}₫\n"  # Lợi nhuận trước lãi vay, thuế và khấu hao
            reply += f"💰 EBIT: {format_vnd(latest_income['operation_profit']) if latest_income is not None and 'operation_profit' in latest_income else 'N/A'}₫\n"  # Lợi nhuận trước lãi vay và thuế
            # Calculate Dividend Yield from actual data
            try:
                from vnstock import Company
                company = Company()
                company.symbol = symbol
                dividends = company.dividends()
                latest_cash_dividend = dividends[dividends['issue_method'] == 'cash'].iloc[0] if not dividends[dividends['issue_method'] == 'cash'].empty else None
                dividend_yield = f"{latest_cash_dividend['cash_dividend_percentage'] * 100:.2f}%" if latest_cash_dividend is not None else "N/A"
            except Exception:
                dividend_yield = "N/A"
            reply += f"💵 Dividend Yield: {dividend_yield}\n"  # Tỷ suất cổ tức
            reply += "\n"
            # === CHỈ TIÊU TĂNG TRƯỞNG ===
            reply += "📈 <b>CHỈ TIÊU TĂNG TRƯỞNG:</b>\n"
            reply += f"📈 Revenue Growth: {latest_income.get('year_revenue_growth', 'N/A') * 100 if latest_income is not None and 'year_revenue_growth' in latest_income else 'N/A'}%\n"  # Tăng trưởng doanh thu
            reply += f"📈 Operating Profit Growth: {latest_income.get('year_operation_profit_growth', 'N/A') * 100 if latest_income is not None and 'year_operation_profit_growth' in latest_income else 'N/A'}%\n"  # Tăng trưởng lợi nhuận hoạt động
            reply += f"📈 Net Income Growth: {latest_income.get('year_share_holder_income_growth', 'N/A') * 100 if latest_income is not None and 'year_share_holder_income_growth' in latest_income else 'N/A'}%\n"  # Tăng trưởng lợi nhuận ròng
            reply += f"📈 EPS Growth: {latest.get('eps_change', 'N/A') * 100 if latest.get('eps_change') is not None else 'N/A'}%\n"  # Tăng trưởng EPS
            reply += f"📈 Book Value Growth: {latest.get('book_value_per_share_change', 'N/A') * 100 if latest.get('book_value_per_share_change') is not None else 'N/A'}%\n"  # Tăng trưởng giá trị sổ sách
            reply += f"📈 EBITDA Growth: {latest.get('ebitda_on_stock_change', 'N/A') * 100 if latest.get('ebitda_on_stock_change') is not None else 'N/A'}%\n"  # Tăng trưởng EBITDA
            reply += "\n"
            # === CHỈ TIÊU THANH KHOẢN ===
            reply += "💰 <b>CHỈ TIÊU THANH KHOẢN:</b>\n"
            reply += f"📊 Current Ratio: {latest.get('current_payment', 'N/A')}\n"  # Tỷ lệ thanh toán hiện hành
            reply += f"📊 Quick Ratio: {latest.get('quick_payment', 'N/A')}\n"  # Tỷ lệ thanh toán nhanh
            reply += f"📊 Cash Ratio: {latest.get('cash_on_equity', 'N/A')}\n"  # Tỷ lệ tiền mặt trên vốn chủ sở hữu
            reply += f"📊 Interest Coverage: {latest.get('ebit_on_interest', 'N/A')}\n"  # Khả năng trả lãi vay
            reply += f"📊 Financial Leverage: {latest.get('equity_on_liability', 'N/A')}\n"  # Đòn bẩy tài chính
            reply += f"📊 Interest Coverage: {latest.get('ebit_on_interest', 'N/A')}\n"  # Khả năng trả lãi vay (trùng lặp)
            reply += f"📊 Financial Leverage: {latest.get('equity_on_liability', 'N/A')}\n\n"  # Đòn bẩy tài chính (trùng lặp)
            # === CHỈ TIÊU CƠ CẤU NGUỒN VỐN ===
            reply += "🏗️ <b>CƠ CẤU NGUỒN VỐN:</b>\n"
            reply += f"📊 Debt/Equity: {latest.get('debt_on_equity', 'N/A')}\n"  # Tỷ lệ nợ trên vốn chủ sở hữu
            reply += f"📊 Debt/Asset: {latest.get('debt_on_asset', 'N/A')}\n"  # Tỷ lệ nợ trên tài sản
            reply += f"📊 Asset/Equity: {latest.get('asset_on_equity', 'N/A')}\n"  # Tỷ lệ tài sản trên vốn chủ sở hữu
            reply += f"📊 Equity/Liability: {latest.get('equity_on_liability', 'N/A')}\n\n"  # Tỷ lệ vốn chủ sở hữu trên nợ phải trả
            # === CHỈ TIÊU HIỆU QUẢ HOẠT ĐỘNG ===
            reply += "⚡ <b>HIỆU QUẢ HOẠT ĐỘNG:</b>\n"
            reply += f"🔄 Asset Turnover: {latest.get('revenue_on_asset', 'N/A')}\n"  # Vòng quay tài sản
            reply += f"🔄 Revenue/Working Capital: {latest.get('revenue_on_work_capital', 'N/A')}\n"  # Vòng quay vốn lưu động
            reply += f"🔄 Cash Circulation: {latest.get('cash_circulation', 'N/A')}\n"  # Vòng quay tiền mặt
            reply += f"📅 Days Receivable: {latest.get('days_receivable', 'N/A')} ngày\n"  # Số ngày thu tiền bình quân
            reply += f"📅 Days Inventory: {latest.get('days_inventory', 'N/A')} ngày\n"  # Số ngày tồn kho bình quân
            reply += f"📅 Days Payable: {latest.get('days_payable', 'N/A')} ngày\n"  # Số ngày trả nợ bình quân
            reply += f"📅 Capex/Fixed Asset: {latest.get('capex_on_fixed_asset', 'N/A')}\n\n"  # Tỷ lệ đầu tư trên tài sản cố định
        # === BÁO CÁO THU NHẬP ===
        if not income_data.empty:
            latest_income = income_data.iloc[0]
            reply += "📈 <b>BÁO CÁO THU NHẬP:</b>\n"
            reply += f"📈 Doanh thu: {format_vnd(latest_income.get('revenue', 'N/A'))}₫\n"  # Tổng doanh thu
            reply += f"📈 Tăng trưởng doanh thu: {latest_income.get('year_revenue_growth', 'N/A')}%\n"  # Tỷ lệ tăng trưởng doanh thu
            reply += f"💰 Lợi nhuận gộp: {format_vnd(latest_income.get('gross_profit', 'N/A'))}₫\n"  # Lợi nhuận gộp
            reply += f"📊 Lợi nhuận ròng: {format_vnd(latest_income.get('post_tax_profit', 'N/A'))}₫\n"  # Lợi nhuận ròng
            reply += f"📊 Lợi nhuận thuần: {format_vnd(latest_income.get('share_holder_income', 'N/A'))}₫\n"  # Lợi nhuận thuần của cổ đông
            reply += f"📈 Tăng trưởng lợi nhuận: {latest_income.get('year_share_holder_income_growth', 'N/A')}%\n"  # Tỷ lệ tăng trưởng lợi nhuận
            reply += f"💵 EBITDA: {format_vnd(latest_income.get('ebitda', 'N/A'))}₫\n"  # Lợi nhuận trước lãi vay, thuế và khấu hao
            reply += f"💵 Thu nhập tài chính: N/A₫\n"  # Thu nhập từ hoạt động tài chính (không có trong TCBS)
            reply += f"💸 Chi phí lãi vay: {format_vnd(latest_income.get('interest_expense', 'N/A'))}₫\n"  # Chi phí lãi vay
            reply += f"📈 Chi phí tài chính: N/A₫\n\n"  # Chi phí tài chính (không có trong TCBS)
        # === BẢNG CÂN ĐỐI KẾ TOÁN ===
        if not balance_data.empty:
            latest_balance = balance_data.iloc[0]
            reply += "🏦 <b>BẢNG CÂN ĐỐI KẾ TOÁN:</b>\n"
            reply += f"🏦 Tài sản ngắn hạn: {format_vnd(latest_balance.get('short_asset', 'N/A'))}₫\n"  # Tổng tài sản ngắn hạn
            reply += f"🏦 Tiền và tương đương: {format_vnd(latest_balance.get('cash', 'N/A'))}₫\n"  # Tiền mặt và tương đương tiền
            reply += f"🏦 Đầu tư ngắn hạn: {format_vnd(latest_balance.get('short_invest', 'N/A'))}₫\n"  # Đầu tư ngắn hạn
            reply += f"🏦 Tổng tài sản: {format_vnd(latest_balance.get('total_asset', 'N/A'))}₫\n"  # Tổng tài sản
            reply += f"📊 Tổng nợ phải trả: {format_vnd(latest_balance.get('liability', 'N/A'))}₫\n"  # Tổng nợ phải trả
            reply += f"💎 Lợi nhuận chưa phân phối: {format_vnd(latest_balance.get('un_distributed_income', 'N/A'))}₫\n"  # Lợi nhuận chưa phân phối
        # === BÁO CÁO LƯU CHUYỂN TIỀN TỆ ===
        if not cashflow_data.empty:
            latest_cashflow = cashflow_data.iloc[0]
            reply += "💸 <b>BÁO CÁO LƯU CHUYỂN TIỀN TỆ:</b>\n"
            reply += f"💰 Chi phí đầu tư: {format_vnd(latest_cashflow.get('invest_cost', 'N/A'))}₫\n"  # Chi phí đầu tư
            reply += f"💰 Lưu chuyển từ đầu tư: {format_vnd(latest_cashflow.get('from_invest', 'N/A'))}₫\n"  # Dòng tiền từ hoạt động đầu tư
            reply += f"💰 Lưu chuyển từ tài chính: {format_vnd(latest_cashflow.get('from_financial', 'N/A'))}₫\n"  # Dòng tiền từ hoạt động tài chính
            reply += f"💰 Lưu chuyển từ bán hàng: {format_vnd(latest_cashflow.get('from_sale', 'N/A'))}₫\n"  # Dòng tiền từ hoạt động kinh doanh
            reply += f"💰 Dòng tiền tự do: {format_vnd(latest_cashflow.get('free_cash_flow', 'N/A'))}₫\n"  # Dòng tiền tự do
            reply += f"💰 Lưu chuyển tiền từ HĐKD: {format_vnd(latest_cashflow.get('net_cash_from_operating', 'N/A'))}₫\n"  # Dòng tiền thuần từ hoạt động kinh doanh
            reply += f"💰 Lưu chuyển tiền từ HĐĐT: {format_vnd(latest_cashflow.get('net_cash_from_investing', 'N/A'))}₫\n"  # Dòng tiền thuần từ hoạt động đầu tư
            reply += f"💰 Lưu chuyển tiền từ HĐTC: {format_vnd(latest_cashflow.get('net_cash_from_financial', 'N/A'))}₫\n"  # Dòng tiền thuần từ hoạt động tài chính
            reply += f"💰 Tăng/giảm tiền thuần: {format_vnd(latest_cashflow.get('net_increase_decrease_in_cash', 'N/A'))}₫\n"  # Tăng/giảm tiền thuần
            reply += f"💰 Tiền cuối kỳ: {format_vnd(latest_cashflow.get('cash_and_cash_equivalents_at_end_of_period', 'N/A'))}₫\n"  # Tiền và tương đương tiền cuối kỳ
            reply += f"💵 Cổ tức đã trả: {format_vnd(latest_cashflow.get('dividends_paid', 'N/A'))}₫\n"  # Cổ tức đã trả
            reply += f"💵 Mua tài sản cố định: {format_vnd(latest_cashflow.get('purchase_of_fixed_assets', 'N/A'))}₫\n"  # Mua tài sản cố định
            reply += f"💵 Vay mượn: {format_vnd(latest_cashflow.get('proceeds_from_borrowings', 'N/A'))}₫\n"  # Vay mượn
            reply += f"💵 Trả nợ vay: {format_vnd(latest_cashflow.get('repayment_of_borrowings', 'N/A'))}₫\n"  # Trả nợ vay
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

