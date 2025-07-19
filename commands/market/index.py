from telegram import Update
from telegram.ext import ContextTypes
import matplotlib.pyplot as plt
import os
from utils.formatters import format_vnd

async def index(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Chỉ số thị trường trong nước"""
    try:
        from vnstock import Trading
        trading = Trading(source='VCI')
        
        # Lấy thông tin các chỉ số chính
        indices = ['VNINDEX', 'HNXINDEX', 'UPCOMINDEX']
        index_data = trading.price_board(indices)
        
        reply = "📈 <b>CHỈ SỐ THỊ TRƯỜNG VIỆT NAM:</b>\n\n"
        
        if not index_data.empty:
            for _, row in index_data.iterrows():
                symbol = row[('listing', 'symbol')]
                current_price = row[('match', 'match_price')]
                ref_price = row[('match', 'reference_price')]
                change = current_price - ref_price
                pct_change = (change / ref_price) * 100 if ref_price else 0
                volume = row[('match', 'match_vol')]
                
                emoji = "🟢" if change >= 0 else "🔴"
                
                # Tên chỉ số
                if symbol == "VNINDEX":
                    name = "VN-Index"
                    description = "Chỉ số chứng khoán TP.HCM"
                elif symbol == "HNXINDEX":
                    name = "HNX-Index"
                    description = "Chỉ số chứng khoán Hà Nội"
                elif symbol == "UPCOMINDEX":
                    name = "UPCOM-Index"
                    description = "Chỉ số chứng khoán UPCOM"
                else:
                    name = symbol
                    description = "Chỉ số thị trường"
                
                reply += f"{emoji} <b>{name}</b>\n"
                reply += f"   📊 Giá: {format_vnd(current_price)} ({pct_change:+.2f}%)\n"
                reply += f"   📈 Thay đổi: {format_vnd(change)}\n"
                reply += f"   📊 KL: {format_vnd(volume)} cổ\n"
                reply += f"   📋 {description}\n\n"
        else:
            reply += "📊 Không có dữ liệu chỉ số\n"
        
        # Thêm thông tin về các chỉ số ngành
        reply += "🏭 <b>Chỉ số ngành chính:</b>\n"
        reply += "• VN30 - Top 30 cổ phiếu lớn nhất HOSE\n"
        reply += "• VNMID - Chỉ số cổ phiếu vừa\n"
        reply += "• VNSML - Chỉ số cổ phiếu nhỏ\n"
        reply += "• VNALL - Chỉ số toàn thị trường\n"
        reply += "• VNMATERIAL - Chỉ số ngành vật liệu\n"
        reply += "• VNFINANCIAL - Chỉ số ngành tài chính\n"
        reply += "• VNUTILITY - Chỉ số ngành tiện ích\n"
        reply += "• VNHEALTHCARE - Chỉ số ngành y tế\n"
        reply += "• VNINDUSTRIAL - Chỉ số ngành công nghiệp\n"
        reply += "• VNCONSUMER - Chỉ số ngành tiêu dùng\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def index_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Chi tiết chỉ số thị trường"""
    if not context.args:
        await update.message.reply_text("Vui lòng nhập: /index_detail <tên_chỉ_số>")
        await update.message.reply_text("Ví dụ: /index_detail VNINDEX")
        await update.message.reply_text("Ví dụ: /index_detail VN30")
        return
    
    try:
        index_name = context.args[0].upper()
        from vnstock import Trading
        trading = Trading(source='VCI')
        
        # Lấy dữ liệu chỉ số
        index_data = trading.price_board([index_name])
        
        if index_data.empty:
            await update.message.reply_text(f"Không tìm thấy dữ liệu cho chỉ số {index_name}")
            return
        
        row = index_data.iloc[0]
        current_price = row[('match', 'match_price')]
        ref_price = row[('match', 'reference_price')]
        change = current_price - ref_price
        pct_change = (change / ref_price) * 100 if ref_price else 0
        volume = row[('match', 'match_vol')]
        high = row[('match', 'highest')]
        low = row[('match', 'lowest')]
        
        emoji = "🟢" if change >= 0 else "🔴"
        
        # Tên và mô tả chỉ số
        index_info = {
            'VNINDEX': ('VN-Index', 'Chỉ số chứng khoán TP.HCM', 'Chỉ số đại diện cho toàn bộ thị trường chứng khoán TP.HCM'),
            'HNXINDEX': ('HNX-Index', 'Chỉ số chứng khoán Hà Nội', 'Chỉ số đại diện cho thị trường chứng khoán Hà Nội'),
            'UPCOMINDEX': ('UPCOM-Index', 'Chỉ số chứng khoán UPCOM', 'Chỉ số đại diện cho thị trường UPCOM'),
            'VN30': ('VN30', 'Chỉ số VN30', 'Chỉ số của 30 cổ phiếu có giá trị vốn hóa lớn nhất HOSE'),
            'VNMID': ('VNMID', 'Chỉ số VNMID', 'Chỉ số cổ phiếu vừa'),
            'VNSML': ('VNSML', 'Chỉ số VNSML', 'Chỉ số cổ phiếu nhỏ'),
            'VNFINANCIAL': ('VNFINANCIAL', 'Chỉ số tài chính', 'Chỉ số ngành tài chính - ngân hàng'),
            'VNMATERIAL': ('VNMATERIAL', 'Chỉ số vật liệu', 'Chỉ số ngành vật liệu - xây dựng'),
            'VNUTILITY': ('VNUTILITY', 'Chỉ số tiện ích', 'Chỉ số ngành tiện ích công cộng'),
            'VNHEALTHCARE': ('VNHEALTHCARE', 'Chỉ số y tế', 'Chỉ số ngành y tế - dược phẩm'),
            'VNINDUSTRIAL': ('VNINDUSTRIAL', 'Chỉ số công nghiệp', 'Chỉ số ngành công nghiệp'),
            'VNCONSUMER': ('VNCONSUMER', 'Chỉ số tiêu dùng', 'Chỉ số ngành tiêu dùng')
        }
        
        name, short_desc, full_desc = index_info.get(index_name, (index_name, 'Chỉ số thị trường', 'Chỉ số đại diện cho thị trường'))
        
        reply = f"📊 <b>CHI TIẾT CHỈ SỐ {name}:</b>\n\n"
        reply += f"📋 <b>Thông tin cơ bản:</b>\n"
        reply += f"• Tên: {name}\n"
        reply += f"• Mô tả: {short_desc}\n"
        reply += f"• Chi tiết: {full_desc}\n\n"
        
        reply += f"{emoji} <b>Dữ liệu hiện tại:</b>\n"
        reply += f"• Giá: {format_vnd(current_price)} ({pct_change:+.2f}%)\n"
        reply += f"• Thay đổi: {format_vnd(change)}\n"
        reply += f"• Khối lượng: {format_vnd(volume)} cổ\n"
        reply += f"• Cao nhất: {format_vnd(high)}\n"
        reply += f"• Thấp nhất: {format_vnd(low)}\n\n"
        
        # Thêm thông tin về thành phần (nếu có)
        if index_name in ['VN30', 'VNMID', 'VNSML']:
            reply += "📋 <b>Thành phần chính:</b>\n"
            if index_name == 'VN30':
                reply += "• VNM, VIC, VHM, HPG, TCB, BID, MBB, GAS, VPB, FPT\n"
                reply += "• VRE, VNM, VIC, VHM, HPG, TCB, BID, MBB, GAS, VPB\n"
                reply += "• FPT, VRE, VNM, VIC, VHM, HPG, TCB, BID, MBB, GAS\n"
            elif index_name == 'VNMID':
                reply += "• Các cổ phiếu có vốn hóa vừa\n"
            elif index_name == 'VNSML':
                reply += "• Các cổ phiếu có vốn hóa nhỏ\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def index_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lịch sử chỉ số thị trường"""
    if not context.args:
        await update.message.reply_text("Vui lòng nhập: /index_history <tên_chỉ_số> <số_ngày>")
        await update.message.reply_text("Ví dụ: /index_history VNINDEX 30")
        return
    
    try:
        index_name = context.args[0].upper()
        days = int(context.args[1]) if len(context.args) > 1 else 30
        
        from vnstock import Vnstock
        stock = Vnstock().stock(symbol=index_name, source='VCI')
        
        # Tính ngày bắt đầu
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        # Lấy lịch sử
        df = stock.quote.history(start=start_str, end=end_str, interval='1D')
        
        if df.empty:
            await update.message.reply_text(f"Không có dữ liệu lịch sử cho chỉ số {index_name}")
            return
        
        # Tạo biểu đồ
        plt.figure(figsize=(12, 6))
        plt.plot(df['time'], df['close'], label=f'Chỉ số {index_name}', color='blue', marker='o', markersize=3, linewidth=2)
        plt.title(f'Lịch sử chỉ số {index_name} ({start_str} - {end_str})')
        plt.xlabel('Ngày')
        plt.ylabel('Giá trị chỉ số')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        
        chart_path = f'/tmp/{index_name}_index_chart.png'
        plt.savefig(chart_path)
        plt.close()
        
        # Gửi biểu đồ
        await update.message.reply_photo(photo=open(chart_path, 'rb'))
        
        # Gửi file CSV
        csv_path = f"/tmp/{index_name}_index_history.csv"
        df.to_csv(csv_path)
        await update.message.reply_document(document=open(csv_path, 'rb'))
        
        # Thống kê cơ bản
        current_value = df['close'].iloc[-1]
        start_value = df['close'].iloc[0]
        total_change = current_value - start_value
        total_pct_change = (total_change / start_value) * 100
        max_value = df['close'].max()
        min_value = df['close'].min()
        
        reply = f"📊 <b>Thống kê chỉ số {index_name} ({days} ngày):</b>\n\n"
        reply += f"• Giá hiện tại: {format_vnd(current_value)}\n"
        reply += f"• Giá đầu kỳ: {format_vnd(start_value)}\n"
        reply += f"• Thay đổi: {format_vnd(total_change)} ({total_pct_change:+.2f}%)\n"
        reply += f"• Cao nhất: {format_vnd(max_value)}\n"
        reply += f"• Thấp nhất: {format_vnd(min_value)}\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
        
        # Xóa file tạm
        os.remove(csv_path)
        os.remove(chart_path)
        
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def index_compare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """So sánh các chỉ số thị trường"""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Vui lòng nhập: /index_compare <chỉ_số1> <chỉ_số2> [chỉ_số3...]")
        await update.message.reply_text("Ví dụ: /index_compare VNINDEX HNXINDEX")
        await update.message.reply_text("Ví dụ: /index_compare VN30 VNMID VNSML")
        return
    
    try:
        indices = [idx.upper() for idx in context.args]
        from vnstock import Trading
        trading = Trading(source='VCI')
        
        # Lấy dữ liệu các chỉ số
        index_data = trading.price_board(indices)
        
        if index_data.empty:
            await update.message.reply_text("Không tìm thấy dữ liệu cho các chỉ số này")
            return
        
        reply = f"📊 <b>SO SÁNH CHỈ SỐ THỊ TRƯỜNG:</b>\n\n"
        
        # Tên chỉ số
        index_names = {
            'VNINDEX': 'VN-Index',
            'HNXINDEX': 'HNX-Index', 
            'UPCOMINDEX': 'UPCOM-Index',
            'VN30': 'VN30',
            'VNMID': 'VNMID',
            'VNSML': 'VNSML',
            'VNFINANCIAL': 'VNFINANCIAL',
            'VNMATERIAL': 'VNMATERIAL',
            'VNUTILITY': 'VNUTILITY',
            'VNHEALTHCARE': 'VNHEALTHCARE',
            'VNINDUSTRIAL': 'VNINDUSTRIAL',
            'VNCONSUMER': 'VNCONSUMER'
        }
        
        # So sánh từng chỉ số
        for _, row in index_data.iterrows():
            symbol = row[('listing', 'symbol')]
            current_price = row[('match', 'match_price')]
            ref_price = row[('listing', 'ref_price')]
            change = current_price - ref_price
            pct_change = (change / ref_price) * 100 if ref_price else 0
            volume = row[('match', 'match_vol')]
            
            emoji = "🟢" if change >= 0 else "🔴"
            name = index_names.get(symbol, symbol)
            
            reply += f"{emoji} <b>{name}</b>\n"
            reply += f"   📊 Giá: {format_vnd(current_price)} ({pct_change:+.2f}%)\n"
            reply += f"   📈 Thay đổi: {format_vnd(change)}\n"
            reply += f"   📊 KL: {format_vnd(volume)} cổ\n\n"
        
        # Phân tích xu hướng
        changes = []
        for _, row in index_data.iterrows():
            current_price = row[('match', 'match_price')]
            ref_price = row[('listing', 'ref_price')]
            pct_change = ((current_price - ref_price) / ref_price) * 100 if ref_price else 0
            changes.append(pct_change)
        
        if len(changes) > 1:
            best_performer = max(changes)
            worst_performer = min(changes)
            
            reply += "📈 <b>Phân tích xu hướng:</b>\n"
            reply += f"• Chỉ số tăng mạnh nhất: {best_performer:+.2f}%\n"
            reply += f"• Chỉ số tăng ít nhất: {worst_performer:+.2f}%\n"
            
            if all(change >= 0 for change in changes):
                reply += "• 🟢 Tất cả chỉ số đều tăng\n"
            elif all(change <= 0 for change in changes):
                reply += "• 🔴 Tất cả chỉ số đều giảm\n"
            else:
                reply += "• 🟡 Xu hướng hỗn hợp\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def index_sector(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Chỉ số ngành và phân tích sector"""
    try:
        from vnstock import Trading
        trading = Trading(source='VCI')
        
        # Các chỉ số ngành chính
        sector_indices = [
            'VNFINANCIAL', 'VNMATERIAL', 'VNUTILITY', 
            'VNHEALTHCARE', 'VNINDUSTRIAL', 'VNCONSUMER'
        ]
        
        sector_data = trading.price_board(sector_indices)
        
        reply = "🏭 <b>CHỈ SỐ NGÀNH THỊ TRƯỜNG:</b>\n\n"
        
        if not sector_data.empty:
            # Sắp xếp theo % thay đổi
            sector_performance = []
            for _, row in sector_data.iterrows():
                symbol = row[('listing', 'symbol')]
                current_price = row[('match', 'match_price')]
                ref_price = row[('listing', 'ref_price')]
                pct_change = ((current_price - ref_price) / ref_price) * 100 if ref_price else 0
                
                sector_names = {
                    'VNFINANCIAL': '🏦 Tài chính - Ngân hàng',
                    'VNMATERIAL': '🏗️ Vật liệu - Xây dựng',
                    'VNUTILITY': '⚡ Tiện ích công cộng',
                    'VNHEALTHCARE': '🏥 Y tế - Dược phẩm',
                    'VNINDUSTRIAL': '🏭 Công nghiệp',
                    'VNCONSUMER': '🛒 Tiêu dùng'
                }
                
                sector_performance.append({
                    'symbol': symbol,
                    'name': sector_names.get(symbol, symbol),
                    'price': current_price,
                    'pct_change': pct_change
                })
            
            # Sắp xếp theo % thay đổi (giảm dần)
            sector_performance.sort(key=lambda x: x['pct_change'], reverse=True)
            
            for i, sector in enumerate(sector_performance, 1):
                emoji = "🟢" if sector['pct_change'] >= 0 else "🔴"
                reply += f"{i}. {emoji} <b>{sector['name']}</b>\n"
                reply += f"   📊 Giá: {format_vnd(sector['price'])} ({sector['pct_change']:+.2f}%)\n\n"
        else:
            reply += "📊 Không có dữ liệu chỉ số ngành\n"
        
        # Thông tin thêm về các ngành
        reply += "📈 <b>Thông tin ngành:</b>\n"
        reply += "• <b>Tài chính:</b> Ngân hàng, bảo hiểm, chứng khoán\n"
        reply += "• <b>Vật liệu:</b> Thép, xi măng, xây dựng\n"
        reply += "• <b>Tiện ích:</b> Điện, nước, gas\n"
        reply += "• <b>Y tế:</b> Dược phẩm, thiết bị y tế\n"
        reply += "• <b>Công nghiệp:</b> Sản xuất, chế tạo\n"
        reply += "• <b>Tiêu dùng:</b> Thực phẩm, đồ uống, bán lẻ\n\n"
        
        reply += "💡 <b>Lưu ý:</b>\n"
        reply += "• Chỉ số ngành phản ánh xu hướng của từng lĩnh vực\n"
        reply += "• Có thể dùng để phân tích rotation giữa các ngành\n"
        reply += "• Theo dõi để nắm bắt cơ hội đầu tư theo sector\n"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}") 