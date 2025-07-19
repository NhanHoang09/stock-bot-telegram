from telegram import Update
from telegram.ext import ContextTypes
import matplotlib.pyplot as plt
import os
from utils.formatters import format_vnd

async def funds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Danh sách quỹ đầu tư (ETF & Quỹ mở)"""
    try:
        from vnstock import Listing
        listing = Listing()
        
        reply = "💰 <b>QUỸ ĐẦU TƯ VIỆT NAM:</b>\n\n"
        
        # Lấy danh sách ETF
        try:
            etf_list = listing.etf()
            if not etf_list.empty:
                reply += "📊 <b>ETF (Quỹ hoán đổi danh mục):</b>\n"
                for i, (_, row) in enumerate(etf_list.head(10).iterrows(), 1):
                    symbol = row.get('symbol', 'N/A')
                    name = row.get('organ_name', 'N/A')
                    reply += f"{i}. <b>{symbol}</b> - {name}\n"
                
                if len(etf_list) > 10:
                    reply += f"... và {len(etf_list) - 10} ETF khác\n"
                reply += "\n"
        except:
            reply += "📊 Không có dữ liệu ETF\n\n"
        
        # Thêm thông tin về các loại quỹ
        reply += "🏦 <b>Phân loại quỹ đầu tư:</b>\n"
        reply += "• <b>ETF:</b> Quỹ hoán đổi danh mục - giao dịch như cổ phiếu\n"
        reply += "• <b>Quỹ mở:</b> Quỹ đầu tư chứng khoán - mua/bán theo NAV\n"
        reply += "• <b>Quỹ đóng:</b> Quỹ đầu tư đóng - không mua/bán thường xuyên\n\n"
        
        reply += "💡 <b>ETF phổ biến:</b>\n"
        reply += "• FUEVFVND - ETF VNM\n"
        reply += "• E1VFVN30 - ETF VN30\n"
        reply += "• FUESSVFL - ETF SSI\n"
        reply += "• VFMVN30 - ETF VNM VN30\n"
        reply += "• VFMVFS - ETF VNM VNFinSelect\n\n"
        
        reply += "📈 <b>Lưu ý đầu tư:</b>\n"
        reply += "• ETF có tính thanh khoản cao hơn quỹ mở\n"
        reply += "• Quỹ mở có NAV cập nhật hàng ngày\n"
        reply += "• Nên xem xét phí quản lý và hiệu suất lịch sử\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def fund_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Chi tiết quỹ đầu tư"""
    if not context.args:
        await update.message.reply_text("Vui lòng nhập: /fund_detail <mã_quỹ>")
        await update.message.reply_text("Ví dụ: /fund_detail FUEVFVND")
        await update.message.reply_text("Ví dụ: /fund_detail E1VFVN30")
        return
    
    try:
        fund_symbol = context.args[0].upper()
        from vnstock import Trading, Listing
        trading = Trading(source='VCI')
        listing = Listing()
        
        # Lấy thông tin giá quỹ
        fund_price = trading.price_board([fund_symbol])
        
        reply = f"💰 <b>CHI TIẾT QUỸ {fund_symbol}:</b>\n\n"
        
        if not fund_price.empty:
            row = fund_price.iloc[0]
            current_price = row[('match', 'match_price')]
            ref_price = row[('listing', 'ref_price')]
            change = current_price - ref_price
            pct_change = (change / ref_price) * 100 if ref_price else 0
            volume = row[('match', 'match_vol')]
            high = row[('match', 'highest')]
            low = row[('match', 'lowest')]
            
            emoji = "🟢" if change >= 0 else "🔴"
            
            reply += f"{emoji} <b>Thông tin giá:</b>\n"
            reply += f"• Giá hiện tại: {format_vnd(current_price)}₫ ({pct_change:+.2f}%)\n"
            reply += f"• Thay đổi: {format_vnd(change)}₫\n"
            reply += f"• Khối lượng: {format_vnd(volume)} đơn vị\n"
            reply += f"• Cao nhất: {format_vnd(high)}₫\n"
            reply += f"• Thấp nhất: {format_vnd(low)}₫\n\n"
        
        # Lấy thông tin từ danh sách ETF
        try:
            etf_list = listing.etf()
            fund_info = etf_list[etf_list['symbol'].str.upper() == fund_symbol]
            
            if not fund_info.empty:
                info = fund_info.iloc[0]
                reply += "📋 <b>Thông tin cơ bản:</b>\n"
                reply += f"• Tên quỹ: {info.get('organ_name', 'N/A')}\n"
                reply += f"• Mã quỹ: {info.get('symbol', 'N/A')}\n"
                if 'exchange' in info:
                    reply += f"• Sàn giao dịch: {info.get('exchange', 'N/A')}\n"
                if 'type' in info:
                    reply += f"• Loại quỹ: {info.get('type', 'N/A')}\n"
                reply += "\n"
        except:
            pass
        
        # Thông tin về các quỹ phổ biến
        fund_descriptions = {
            'FUEVFVND': {
                'name': 'ETF VNM',
                'description': 'Quỹ ETF theo dõi chỉ số VN-Index',
                'strategy': 'Đầu tư vào các cổ phiếu trong VN-Index',
                'risk': 'Rủi ro trung bình'
            },
            'E1VFVN30': {
                'name': 'ETF VN30',
                'description': 'Quỹ ETF theo dõi chỉ số VN30',
                'strategy': 'Đầu tư vào 30 cổ phiếu lớn nhất HOSE',
                'risk': 'Rủi ro thấp đến trung bình'
            },
            'FUESSVFL': {
                'name': 'ETF SSI',
                'description': 'Quỹ ETF của SSI',
                'strategy': 'Đầu tư theo chiến lược của SSI',
                'risk': 'Rủi ro trung bình'
            },
            'VFMVN30': {
                'name': 'ETF VNM VN30',
                'description': 'Quỹ ETF VNM theo dõi VN30',
                'strategy': 'Đầu tư vào 30 cổ phiếu blue-chip',
                'risk': 'Rủi ro thấp đến trung bình'
            }
        }
        
        if fund_symbol in fund_descriptions:
            fund_info = fund_descriptions[fund_symbol]
            reply += "📊 <b>Thông tin chi tiết:</b>\n"
            reply += f"• Tên: {fund_info['name']}\n"
            reply += f"• Mô tả: {fund_info['description']}\n"
            reply += f"• Chiến lược: {fund_info['strategy']}\n"
            reply += f"• Mức độ rủi ro: {fund_info['risk']}\n\n"
        
        reply += "💡 <b>Lưu ý:</b>\n"
        reply += "• ETF giao dịch như cổ phiếu trên sàn\n"
        reply += "• Giá ETF có thể khác biệt với NAV\n"
        reply += "• Nên xem xét spread và khối lượng giao dịch\n"
        reply += "• Theo dõi tracking error so với benchmark\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def fund_performance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hiệu suất quỹ đầu tư"""
    if not context.args:
        await update.message.reply_text("Vui lòng nhập: /fund_performance <mã_quỹ> [số_ngày]")
        await update.message.reply_text("Ví dụ: /fund_performance FUEVFVND")
        await update.message.reply_text("Ví dụ: /fund_performance E1VFVN30 30")
        return
    
    try:
        fund_symbol = context.args[0].upper()
        days = int(context.args[1]) if len(context.args) > 1 else 30
        
        from vnstock import Vnstock
        stock = Vnstock().stock(symbol=fund_symbol, source='VCI')
        
        # Tính ngày bắt đầu
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        # Lấy lịch sử
        df = stock.quote.history(start=start_str, end=end_str, interval='1D')
        
        if df.empty:
            await update.message.reply_text(f"Không có dữ liệu hiệu suất cho quỹ {fund_symbol}")
            return
        
        # Tính toán hiệu suất
        current_price = df['close'].iloc[-1]
        start_price = df['close'].iloc[0]
        total_return = ((current_price - start_price) / start_price) * 100
        max_price = df['close'].max()
        min_price = df['close'].min()
        volatility = df['close'].pct_change().std() * 100
        
        # Tạo biểu đồ
        plt.figure(figsize=(12, 6))
        plt.plot(df['time'], df['close'], label=f'Quỹ {fund_symbol}', color='green', marker='o', markersize=3, linewidth=2)
        plt.title(f'Hiệu suất quỹ {fund_symbol} ({start_str} - {end_str})')
        plt.xlabel('Ngày')
        plt.ylabel('Giá quỹ (VNĐ)')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        
        chart_path = f'/tmp/{fund_symbol}_fund_chart.png'
        plt.savefig(chart_path)
        plt.close()
        
        # Gửi biểu đồ
        await update.message.reply_photo(photo=open(chart_path, 'rb'))
        
        # Gửi file CSV
        csv_path = f"/tmp/{fund_symbol}_fund_performance.csv"
        df.to_csv(csv_path)
        await update.message.reply_document(document=open(csv_path, 'rb'))
        
        # Thống kê hiệu suất
        reply = f"📊 <b>HIỆU SUẤT QUỸ {fund_symbol} ({days} ngày):</b>\n\n"
        reply += f"💰 <b>Thống kê cơ bản:</b>\n"
        reply += f"• Giá hiện tại: {format_vnd(current_price)}₫\n"
        reply += f"• Giá đầu kỳ: {format_vnd(start_price)}₫\n"
        reply += f"• Tổng lợi nhuận: {total_return:+.2f}%\n"
        reply += f"• Giá cao nhất: {format_vnd(max_price)}₫\n"
        reply += f"• Giá thấp nhất: {format_vnd(min_price)}₫\n"
        reply += f"• Độ biến động: {volatility:.2f}%\n\n"
        
        # Đánh giá hiệu suất
        if total_return > 5:
            performance_rating = "🟢 Tốt"
        elif total_return > 0:
            performance_rating = "🟡 Trung bình"
        else:
            performance_rating = "🔴 Kém"
        
        reply += f"📈 <b>Đánh giá hiệu suất:</b>\n"
        reply += f"• Xếp hạng: {performance_rating}\n"
        
        if volatility < 2:
            risk_level = "Thấp"
        elif volatility < 5:
            risk_level = "Trung bình"
        else:
            risk_level = "Cao"
        
        reply += f"• Mức độ rủi ro: {risk_level}\n"
        reply += f"• Độ biến động: {volatility:.2f}%\n\n"
        
        reply += "💡 <b>Lưu ý:</b>\n"
        reply += "• Hiệu suất quá khứ không đảm bảo tương lai\n"
        reply += "• Nên xem xét cùng với benchmark\n"
        reply += "• Theo dõi tracking error và phí quản lý\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
        
        # Xóa file tạm
        os.remove(csv_path)
        os.remove(chart_path)
        
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def fund_compare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """So sánh các quỹ đầu tư"""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Vui lòng nhập: /fund_compare <quỹ1> <quỹ2> [quỹ3...]")
        await update.message.reply_text("Ví dụ: /fund_compare FUEVFVND E1VFVN30")
        return
    
    try:
        fund_symbols = [fund.upper() for fund in context.args]
        from vnstock import Trading
        trading = Trading(source='VCI')
        
        # Lấy dữ liệu các quỹ
        fund_data = trading.price_board(fund_symbols)
        
        if fund_data.empty:
            await update.message.reply_text("Không tìm thấy dữ liệu cho các quỹ này")
            return
        
        reply = f"📊 <b>SO SÁNH QUỸ ĐẦU TƯ:</b>\n\n"
        
        # So sánh từng quỹ
        for _, row in fund_data.iterrows():
            symbol = row[('listing', 'symbol')]
            current_price = row[('match', 'match_price')]
            ref_price = row[('listing', 'ref_price')]
            change = current_price - ref_price
            pct_change = (change / ref_price) * 100 if ref_price else 0
            volume = row[('match', 'match_vol')]
            
            emoji = "🟢" if change >= 0 else "🔴"
            
            reply += f"{emoji} <b>{symbol}</b>\n"
            reply += f"   📊 Giá: {format_vnd(current_price)}₫ ({pct_change:+.2f}%)\n"
            reply += f"   📈 Thay đổi: {format_vnd(change)}₫\n"
            reply += f"   📊 KL: {format_vnd(volume)} đơn vị\n\n"
        
        # Phân tích xu hướng
        changes = []
        for _, row in fund_data.iterrows():
            current_price = row[('match', 'match_price')]
            ref_price = row[('listing', 'ref_price')]
            pct_change = ((current_price - ref_price) / ref_price) * 100 if ref_price else 0
            changes.append(pct_change)
        
        if len(changes) > 1:
            best_performer = max(changes)
            worst_performer = min(changes)
            
            reply += "📈 <b>Phân tích xu hướng:</b>\n"
            reply += f"• Quỹ tăng mạnh nhất: {best_performer:+.2f}%\n"
            reply += f"• Quỹ tăng ít nhất: {worst_performer:+.2f}%\n"
            
            if all(change >= 0 for change in changes):
                reply += "• 🟢 Tất cả quỹ đều tăng\n"
            elif all(change <= 0 for change in changes):
                reply += "• 🔴 Tất cả quỹ đều giảm\n"
            else:
                reply += "• 🟡 Xu hướng hỗn hợp\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def fund_sector(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quỹ đầu tư theo ngành"""
    try:
        from vnstock import Listing
        listing = Listing()
        
        reply = "🏭 <b>QUỸ ĐẦU TƯ THEO NGÀNH:</b>\n\n"
        
        # Lấy danh sách ETF
        try:
            etf_list = listing.etf()
            if not etf_list.empty:
                # Phân loại theo ngành (dựa trên tên)
                sector_funds = {
                    'Tài chính': [],
                    'Công nghệ': [],
                    'Tiêu dùng': [],
                    'Vật liệu': [],
                    'Khác': []
                }
                
                for _, row in etf_list.iterrows():
                    symbol = row.get('symbol', '')
                    name = row.get('organ_name', '')
                    
                    if any(keyword in name.upper() for keyword in ['TÀI CHÍNH', 'NGÂN HÀNG', 'BẢO HIỂM']):
                        sector_funds['Tài chính'].append((symbol, name))
                    elif any(keyword in name.upper() for keyword in ['CÔNG NGHỆ', 'TECH', 'SOFTWARE']):
                        sector_funds['Công nghệ'].append((symbol, name))
                    elif any(keyword in name.upper() for keyword in ['TIÊU DÙNG', 'THỰC PHẨM', 'BÁN LẺ']):
                        sector_funds['Tiêu dùng'].append((symbol, name))
                    elif any(keyword in name.upper() for keyword in ['VẬT LIỆU', 'XÂY DỰNG', 'THÉP']):
                        sector_funds['Vật liệu'].append((symbol, name))
                    else:
                        sector_funds['Khác'].append((symbol, name))
                
                # Hiển thị theo ngành
                for sector, funds in sector_funds.items():
                    if funds:
                        reply += f"🏭 <b>{sector}:</b>\n"
                        for symbol, name in funds[:5]:  # Giới hạn 5 quỹ mỗi ngành
                            reply += f"• <b>{symbol}</b> - {name}\n"
                        if len(funds) > 5:
                            reply += f"  ... và {len(funds) - 5} quỹ khác\n"
                        reply += "\n"
            else:
                reply += "📊 Không có dữ liệu ETF\n\n"
        except:
            reply += "📊 Không có dữ liệu ETF\n\n"
        
        reply += "💡 <b>Lưu ý:</b>\n"
        reply += "• Phân loại dựa trên tên quỹ\n"
        reply += "• Có thể có quỹ đa ngành\n"
        reply += "• Nên xem xét chiến lược đầu tư thực tế\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def fund_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xếp hạng quỹ đầu tư"""
    try:
        from vnstock import Listing, Trading
        listing = Listing()
        trading = Trading(source='VCI')
        
        reply = "🏆 <b>XẾP HẠNG QUỸ ĐẦU TƯ:</b>\n\n"
        
        # Lấy danh sách ETF và giá
        try:
            etf_list = listing.etf()
            if not etf_list.empty:
                # Lấy giá cho các ETF
                symbols = etf_list['symbol'].tolist()[:20]  # Giới hạn 20 ETF
                fund_prices = trading.price_board(symbols)
                
                if not fund_prices.empty:
                    # Tính % thay đổi
                    fund_performance = []
                    for _, row in fund_prices.iterrows():
                        symbol = row[('listing', 'symbol')]
                        current_price = row[('match', 'match_price')]
                        ref_price = row[('listing', 'ref_price')]
                        pct_change = ((current_price - ref_price) / ref_price) * 100 if ref_price else 0
                        
                        # Lấy tên quỹ
                        fund_info = etf_list[etf_list['symbol'] == symbol]
                        name = fund_info.iloc[0]['organ_name'] if not fund_info.empty else symbol
                        
                        fund_performance.append({
                            'symbol': symbol,
                            'name': name,
                            'pct_change': pct_change,
                            'price': current_price
                        })
                    
                    # Sắp xếp theo % thay đổi (giảm dần)
                    fund_performance.sort(key=lambda x: x['pct_change'], reverse=True)
                    
                    reply += "📈 <b>Top 10 quỹ tăng giá:</b>\n"
                    for i, fund in enumerate(fund_performance[:10], 1):
                        emoji = "🟢" if fund['pct_change'] >= 0 else "🔴"
                        reply += f"{i}. {emoji} <b>{fund['symbol']}</b> ({fund['pct_change']:+.2f}%)\n"
                        reply += f"   {fund['name']}\n\n"
                    
                    reply += "📉 <b>Top 5 quỹ giảm giá:</b>\n"
                    for i, fund in enumerate(fund_performance[-5:], 1):
                        emoji = "🔴"
                        reply += f"{i}. {emoji} <b>{fund['symbol']}</b> ({fund['pct_change']:+.2f}%)\n"
                        reply += f"   {fund['name']}\n\n"
                else:
                    reply += "📊 Không có dữ liệu giá quỹ\n\n"
            else:
                reply += "📊 Không có dữ liệu ETF\n\n"
        except:
            reply += "📊 Không có dữ liệu quỹ\n\n"
        
        reply += "💡 <b>Lưu ý:</b>\n"
        reply += "• Xếp hạng dựa trên % thay đổi giá\n"
        reply += "• Chỉ tính các ETF có dữ liệu\n"
        reply += "• Hiệu suất quá khứ không đảm bảo tương lai\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}") 