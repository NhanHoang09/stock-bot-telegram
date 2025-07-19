from telegram import Update
from telegram.ext import ContextTypes
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from utils.formatters import format_vnd

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "📊 <b>CÁCH SỬ DỤNG LỆNH HISTORY:</b>\n\n"
            "1️⃣ <b>Xem theo số năm gần nhất:</b>\n"
            "   /history <symbol> <years>\n"
            "   Ví dụ: /history VNM 2\n\n"
            "2️⃣ <b>Xem theo khoảng thời gian cụ thể:</b>\n"
            "   /history <symbol> <years> <start_year>-<end_year>\n"
            "   Ví dụ: /history VNM 2 2021-2023\n\n"
            "3️⃣ <b>Xem theo ngày cụ thể:</b>\n"
            "   /history <symbol> <years> <start_date>-<end_date>\n"
            "   Ví dụ: /history VNM 2 2021-01-01-2023-12-31\n\n"
            "📝 <b>Lưu ý:</b>\n"
            "• <years> chỉ dùng để tính mặc định nếu không có ngày cụ thể\n"
            "• Định dạng ngày: YYYY-MM-DD\n"
            "• Định dạng năm: YYYY-YYYY",
            parse_mode='HTML'
        )
        return
    
    symbol = context.args[0].upper()
    years = int(context.args[1]) if len(context.args) > 1 and context.args[1].isdigit() else 1

    # Mặc định: lấy <years> năm gần nhất
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * years)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    # Xử lý tham số thời gian cụ thể
    if len(context.args) > 2:
        time_range = context.args[2]
        
        # Kiểm tra định dạng năm (YYYY-YYYY)
        if '-' in time_range and len(time_range.split('-')) == 2:
            start_year, end_year = time_range.split('-')
            try:
                start_year = int(start_year)
                end_year = int(end_year)
                start_str = f"{start_year}-01-01"
                end_str = f"{end_year}-12-31"
            except ValueError:
                await update.message.reply_text("❌ Sai định dạng năm. Ví dụ đúng: 2021-2023")
                return
        
        # Kiểm tra định dạng ngày cụ thể (YYYY-MM-DD-YYYY-MM-DD)
        elif time_range.count('-') == 5:
            try:
                parts = time_range.split('-')
                start_str = f"{parts[0]}-{parts[1]}-{parts[2]}"
                end_str = f"{parts[3]}-{parts[4]}-{parts[5]}"
                
                # Validate ngày
                datetime.strptime(start_str, '%Y-%m-%d')
                datetime.strptime(end_str, '%Y-%m-%d')
            except ValueError:
                await update.message.reply_text("❌ Sai định dạng ngày. Ví dụ đúng: 2021-01-01-2023-12-31")
                return

    try:
        from vnstock import Vnstock
        stock = Vnstock().stock(symbol=symbol, source='VCI')
        df = stock.quote.history(start=start_str, end=end_str, interval='1D')
        if df.empty:
            await update.message.reply_text(f"❌ Không có dữ liệu lịch sử cho mã {symbol} trong khoảng thời gian {start_str} - {end_str}.")
            return
        
        # === PHÂN TÍCH DỮ LIỆU ===
        current_price = df['close'].iloc[-1]
        start_price = df['close'].iloc[0]
        total_change = current_price - start_price
        total_change_pct = (total_change / start_price) * 100
        
        # Thống kê cơ bản
        max_price = df['close'].max()
        min_price = df['close'].min()
        avg_price = df['close'].mean()
        std_price = df['close'].std()
        
        # Tìm ngày cao nhất và thấp nhất
        max_date = df.loc[df['close'].idxmax(), 'time']
        min_date = df.loc[df['close'].idxmin(), 'time']
        
        # Tính toán biến động
        daily_returns = df['close'].pct_change().dropna()
        volatility = daily_returns.std() * 100  # Độ biến động hàng ngày
        
        # Tạo bảng thống kê
        stats_text = f"📊 <b>PHÂN TÍCH LỊCH SỬ {symbol}:</b>\n"
        stats_text += f"📅 <b>Thời gian: {start_str} → {end_str}</b>\n\n"
        
        # === THÔNG TIN TỔNG QUAN ===
        stats_text += "📈 <b>THÔNG TIN TỔNG QUAN:</b>\n"
        stats_text += f"📊 Số ngày giao dịch: {len(df)} ngày\n"
        stats_text += f"💰 Giá bắt đầu: {format_vnd(start_price)}₫\n"
        stats_text += f"💰 Giá kết thúc: {format_vnd(current_price)}₫\n"
        stats_text += f"📈 Thay đổi tổng: {format_vnd(total_change)} ({total_change_pct:+.2f}%)\n\n"
        
        # === THỐNG KÊ GIÁ ===
        stats_text += "📊 <b>THỐNG KÊ GIÁ:</b>\n"
        stats_text += f"📈 Giá cao nhất: {format_vnd(max_price)}₫ ({max_date.strftime('%Y-%m-%d')})\n"
        stats_text += f"📉 Giá thấp nhất: {format_vnd(min_price)}₫ ({min_date.strftime('%Y-%m-%d')})\n"
        stats_text += f"📊 Giá trung bình: {format_vnd(avg_price)}₫\n"
        stats_text += f"📊 Độ lệch chuẩn: {format_vnd(std_price)}₫\n"
        stats_text += f"📊 Độ biến động: {volatility:.2f}%\n\n"
        
        # === PHÂN TÍCH THEO NĂM ===
        df['year'] = pd.to_datetime(df['time']).dt.year
        yearly_stats = df.groupby('year').agg({
            'close': ['mean', 'min', 'max', 'std']
        }).round(2)
        
        stats_text += "📅 <b>THỐNG KÊ THEO NĂM:</b>\n"
        for year, data in yearly_stats.iterrows():
            avg = data[('close', 'mean')]
            min_val = data[('close', 'min')]
            max_val = data[('close', 'max')]
            stats_text += f"📊 {year}: TB={format_vnd(avg)}₫, Min={format_vnd(min_val)}₫, Max={format_vnd(max_val)}₫\n"
        stats_text += "\n"
        
        # === PHÂN TÍCH THEO THÁNG ===
        df['month'] = pd.to_datetime(df['time']).dt.to_period('M')
        monthly_stats = df.groupby('month').agg({
            'close': ['mean', 'min', 'max', 'std']
        }).round(2)
        
        stats_text += "📅 <b>THỐNG KÊ THEO THÁNG (6 THÁNG GẦN NHẤT):</b>\n"
        for month, data in monthly_stats.tail(6).iterrows():
            month_str = str(month)
            avg = data[('close', 'mean')]
            min_val = data[('close', 'min')]
            max_val = data[('close', 'max')]
            stats_text += f"📊 {month_str}: TB={format_vnd(avg)}₫, Min={format_vnd(min_val)}₫, Max={format_vnd(max_val)}₫\n"
        stats_text += "\n"
        
        # === PHÂN TÍCH XU HƯỚNG ===
        # Tính xu hướng 30 ngày gần nhất
        recent_30 = df.tail(30)
        if len(recent_30) >= 30:
            trend_30 = (recent_30['close'].iloc[-1] - recent_30['close'].iloc[0]) / recent_30['close'].iloc[0] * 100
            
            # Tính xu hướng 7 ngày gần nhất
            recent_7 = df.tail(7)
            trend_7 = (recent_7['close'].iloc[-1] - recent_7['close'].iloc[0]) / recent_7['close'].iloc[0] * 100
            
            stats_text += "📈 <b>XU HƯỚNG GẦN ĐÂY:</b>\n"
            stats_text += f"📊 30 ngày qua: {trend_30:+.2f}%\n"
            stats_text += f"📊 7 ngày qua: {trend_7:+.2f}%\n\n"
        
        # === BẢNG GIÁ GẦN ĐÂY ===
        stats_text += "📋 <b>GIÁ GẦN ĐÂY (10 NGÀY):</b>\n"
        recent_10 = df.tail(10)
        for _, row in recent_10.iterrows():
            date_str = row['time'].strftime('%m-%d')
            price = row['close']
            change = price - start_price
            change_pct = (change / start_price) * 100
            stats_text += f"📅 {date_str}: {format_vnd(price)}₫ ({change_pct:+.2f}%)\n"
        
        # Gửi bảng thống kê trước
        await update.message.reply_text(stats_text, parse_mode='HTML')
        
        # === VẼ BIỂU ĐỒ CẢI THIỆN ===
        # Tạo subplot cho giá và volume
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})
        
        # Biểu đồ giá
        ax1.plot(df['time'], df['close'], label='Giá đóng cửa', color='blue', linewidth=2)
        ax1.scatter(df['time'], df['close'], color='red', s=20, alpha=0.6)
        
        # Thêm đường trung bình
        ax1.axhline(y=avg_price, color='orange', linestyle='--', alpha=0.7, label=f'Trung bình: {format_vnd(avg_price)}₫')
        
        # Đánh dấu điểm cao nhất và thấp nhất
        ax1.scatter(max_date, max_price, color='green', s=100, marker='^', label=f'Cao nhất: {format_vnd(max_price)}₫')
        ax1.scatter(min_date, min_price, color='red', s=100, marker='v', label=f'Thấp nhất: {format_vnd(min_price)}₫')
        
        ax1.set_title(f'Lịch sử giá {symbol} ({start_str} - {end_str})', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Giá (VND)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.tick_params(axis='x', rotation=45)
        
        # Biểu đồ volume (nếu có)
        if 'volume' in df.columns:
            ax2.bar(df['time'], df['volume'], alpha=0.6, color='gray')
            ax2.set_ylabel('Khối lượng', fontsize=12)
            ax2.set_xlabel('Ngày', fontsize=12)
            ax2.grid(True, alpha=0.3)
            ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        chart_path = f'/tmp/{symbol}_chart.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        # Gửi biểu đồ
        await update.message.reply_photo(photo=open(chart_path, 'rb'))
        
        # Gửi file CSV
        csv_path = f"/tmp/{symbol}_history.csv"
        df.to_csv(csv_path, index=False)
        await update.message.reply_document(document=open(csv_path, 'rb'))
        
        # Dọn dẹp file
        os.remove(csv_path)
        os.remove(chart_path)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi: {e}")

