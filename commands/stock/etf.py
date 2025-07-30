from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd
from utils.stock_info import get_full_stock_info
from utils.common import get_development_message

async def get_etf_data_from_vnstock(symbol):
    """Lấy dữ liệu ETF thực từ vnstock"""
    try:
        from vnstock import Trading, Company, Listing
        import pandas as pd
        
        # Lấy dữ liệu giá
        trading = Trading(source='TCBS')
        price_data = trading.price_board([symbol])
        
        if price_data.empty:
            return None
        
        price_info = price_data.iloc[0]
        
        # Tạo dữ liệu ETF từ vnstock
        etf_data = {
            'symbol': symbol,
            'price': float(price_info['Giá']) if price_info['Giá'] is not None else 0,
            'price_change_1d': price_info.get('% thay đổi giá 3D', 0),
            'price_change_1m': price_info.get('% thay đổi giá 1M', 0),
            'price_change_3m': price_info.get('% thay đổi giá 3M', 0),
            'price_change_1y': price_info.get('% thay đổi giá 1Y', 0),
            'volume': price_info.get('KLGD ròng(CM)', 0),
            'high_1y': price_info.get('Đỉnh 1Y', 0) if price_info.get('Đỉnh 1Y') is not None else 0,
            'low_1y': price_info.get('Đáy 1Y', 0) if price_info.get('Đáy 1Y') is not None else 0
        }
        
        # Xác định loại ETF dựa trên symbol và dữ liệu
        etf_data['etf_type'] = 'Unknown'
        etf_data['issuer'] = 'Unknown'
        etf_data['index'] = 'Unknown'
        
        # Phân loại ETF dựa trên symbol pattern
        if symbol.startswith('FUEV'):
            if 'VND' in symbol:
                etf_data['etf_type'] = 'Fubon FTSE Vietnam ETF'
                etf_data['issuer'] = 'Fubon'
                etf_data['index'] = 'FTSE Vietnam'
            elif 'SVFL' in symbol:
                etf_data['etf_type'] = 'Fubon FTSE Vietnam 30 ETF'
                etf_data['issuer'] = 'Fubon'
                etf_data['index'] = 'FTSE Vietnam 30'
            elif 'SV50' in symbol:
                etf_data['etf_type'] = 'Fubon FTSE Vietnam 50 ETF'
                etf_data['issuer'] = 'Fubon'
                etf_data['index'] = 'FTSE Vietnam 50'
            elif 'VNV30' in symbol:
                etf_data['etf_type'] = 'Fubon FTSE Vietnam 30 ETF'
                etf_data['issuer'] = 'Fubon'
                etf_data['index'] = 'VN30'
            elif 'VFMID' in symbol:
                etf_data['etf_type'] = 'Fubon FTSE Vietnam Mid Cap ETF'
                etf_data['issuer'] = 'Fubon'
                etf_data['index'] = 'FTSE Vietnam Mid Cap'
            elif 'VN100' in symbol:
                etf_data['etf_type'] = 'VinaCapital VN100 ETF'
                etf_data['issuer'] = 'VinaCapital'
                etf_data['index'] = 'VN100'
            elif 'SVND' in symbol:
                etf_data['etf_type'] = 'Fubon FTSE Vietnam ETF'
                etf_data['issuer'] = 'Fubon'
                etf_data['index'] = 'FTSE Vietnam'
            else:
                # ETF Fubon khác
                etf_data['etf_type'] = 'Fubon ETF'
                etf_data['issuer'] = 'Fubon'
                etf_data['index'] = 'Unknown'
        elif symbol.startswith('VN'):
            if symbol == 'VNM':
                etf_data['etf_type'] = 'VanEck Vectors Vietnam ETF'
                etf_data['issuer'] = 'VanEck'
                etf_data['index'] = 'Vietnam Market'
            elif '30' in symbol:
                etf_data['etf_type'] = 'VN30 ETF'
                etf_data['issuer'] = 'SSI'
                etf_data['index'] = 'VN30'
            elif 'MID' in symbol:
                etf_data['etf_type'] = 'VN Mid Cap ETF'
                etf_data['issuer'] = 'SSI'
                etf_data['index'] = 'VN Mid Cap'
            elif 'SML' in symbol:
                etf_data['etf_type'] = 'VN Small Cap ETF'
                etf_data['issuer'] = 'SSI'
                etf_data['index'] = 'VN Small Cap'
            elif 'DIAMOND' in symbol:
                etf_data['etf_type'] = 'VNDiamond ETF'
                etf_data['issuer'] = 'SSI'
                etf_data['index'] = 'VNDiamond'
            else:
                # ETF theo ngành
                sector_map = {
                    'FIN': 'Tài chính', 'REAL': 'Bất động sản', 'MATERIAL': 'Vật liệu',
                    'ENERGY': 'Năng lượng', 'HEALTH': 'Y tế', 'TECH': 'Công nghệ',
                    'COMM': 'Tiêu dùng', 'INDUSTRIAL': 'Công nghiệp', 'UTILITY': 'Tiện ích', 'TELECOM': 'Viễn thông'
                }
                for sector, name in sector_map.items():
                    if sector in symbol:
                        etf_data['etf_type'] = f'VN {name} ETF'
                        etf_data['issuer'] = 'SSI'
                        etf_data['index'] = f'VN {name}'
                        break
        else:
            # ETF khác không theo pattern
            etf_data['etf_type'] = 'ETF'
            etf_data['issuer'] = 'Unknown'
            etf_data['index'] = 'Unknown'
        
        return etf_data
        
    except Exception as e:
        print(f"Error getting ETF data from vnstock: {e}")
        return None

async def etf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ETF command handler"""
    if not context.args:
        # Tính năng đang phát triển
        reply = get_development_message("/etf", "hiển thị danh sách ETF")
        
        await update.message.reply_text(reply, parse_mode='HTML')
        
        # # Hiển thị danh sách ETF - CODE CŨ (ĐÃ COMMENT)
        # try:
        #     # Danh sách ETF phổ biến để kiểm tra
        #     etf_symbols = ['FUEVFVND', 'FUESSVFL', 'FUEVNV30', 'FUESSVND', 'FUEVFMID', 'FUEVN100', 'FUESSV50', 'VNM', 'VNM30', 'VNMID', 'VNSML', 'VNDIAMOND']
        #     
        #     reply = "📈 <b>Danh sách ETF có sẵn trên vnstock:</b>\n\n"
        #     available_etfs = []
        #     
        #     for symbol in etf_symbols:
        #         try:
        #             etf_data = await get_etf_data_from_vnstock(symbol)
        #             if etf_data and etf_data.get('price'):
        #                 available_etfs.append({
        #                     'symbol': symbol,
        #                     'type': etf_data.get('etf_type', 'ETF'),
        #                     'issuer': etf_data.get('issuer', 'Unknown'),
        #                     'index': etf_data.get('index', 'Unknown'),
        #                     'price': etf_data.get('price', 0)
        #                 })
        #         except Exception as e:
        #             continue
        #     
        #     if available_etfs:
        #         for etf in available_etfs:
        #             reply += f"🔹 <b>{etf['symbol']}</b> - {etf['type']}\n"
        #             reply += f"   🏢 {etf['issuer']} | 📈 {etf['index']}\n"
        #             reply += f"   💰 Giá: {etf['price']:,.0f}₫\n\n"
        #         else:
        #             reply += "❌ Không thể lấy danh sách ETF tự động từ dữ liệu hiện tại.\n"
        #             reply += "Vui lòng dùng /etf <symbol> hoặc /etf info <symbol> để tra cứu."
        #         
        #         await update.message.reply_text(reply, parse_mode='HTML')
        # except Exception as e:
        #     await update.message.reply_text(f"❌ Có lỗi xảy ra: {str(e)}")
        return

    symbol = context.args[0].upper()
     
    if len(context.args) > 1 and context.args[1].lower() == 'info':
        # Tính năng đang phát triển
        reply = get_development_message(f"/etf info {symbol}", "thông tin chi tiết ETF")
         
        await update.message.reply_text(reply, parse_mode='HTML')
        
        # # Hiển thị thông tin chi tiết ETF - CODE CŨ (ĐÃ COMMENT)
        # try:
        #     await show_animated_loading(update, context, f"🔍 Đang lấy thông tin ETF {symbol}...")
        #     
        #     etf_data = await get_etf_data_from_vnstock(symbol)
        #     
        #     if not etf_data:
        #         await finish_loading(loading_msg, f"❌ Không tìm thấy thông tin ETF {symbol}")
        #         return
        #     
        #     reply = f"📊 <b>Thông tin ETF: {symbol}</b>\n\n"
        #     
        #     # Thông tin cơ bản
        #     reply += f"💹 <b>Giá hiện tại:</b> {etf_data.get('price', 0):,.0f}₫\n"
        #     reply += f"📝 <b>Tên:</b> {etf_data.get('etf_type', 'Unknown')}\n"
        #     reply += f"🏢 <b>Đơn vị quản lý:</b> {etf_data.get('issuer', 'Unknown')}\n"
        #     reply += f"📈 <b>Chỉ số tham chiếu:</b> {etf_data.get('index', 'Unknown')}\n\n"
        #     
        #     # Thay đổi giá
        #     price_change = etf_data.get('price_change', {})
        #     if price_change:
        #         reply += "📈 <b>Thay đổi giá:</b>\n"
        #         for period, change in price_change.items():
        #             if change is not None:
        #         reply += f"   • {period}: {change:+.1f}%\n"
        #         reply += "\n"
        #     
        #     # Thông tin giao dịch
        #     reply += "📊 <b>Thông tin giao dịch:</b>\n"
        #     reply += f"   • Khối lượng: {etf_data.get('volume', 0):,.0f} cổ phiếu\n"
        #     reply += f"   • Đỉnh 1Y: {etf_data.get('high_1y', 0):,.0f}₫\n"
        #     reply += f"   • Đáy 1Y: {etf_data.get('low_1y', 0):,.0f}₫\n\n"
        #     
        #     reply += "💡 <b>Nguồn dữ liệu:</b> vnstock API (TCBS source)"
        #     
        #     await finish_loading(loading_msg, reply)
        # except Exception as e:
        #     await finish_loading(loading_msg, f"❌ Có lỗi xảy ra: {str(e)}")
        return
    
    # Kiểm tra giá ETF - chỉ chức năng này hoạt động
    try:
        from vnstock import Trading
        prices = Trading(source='TCBS').price_board([symbol])
        if prices.empty:
            await update.message.reply_text(f"❌ Không tìm thấy mã ETF {symbol}")
            return
        
        # Sử dụng cột 'Giá' thay vì tuple key
        price_value = prices.iloc[0]['Giá']
        if price_value is None:
            await update.message.reply_text(f"❌ Không có dữ liệu giá cho mã ETF {symbol}")
            return
        
        price = float(price_value)
        formatted_price = format_vnd(price)
        reply = f"💹 <b>Giá hiện tại của {symbol}:</b> <b>{formatted_price}₫</b> 🇻🇳"
        
        await update.message.reply_text(reply, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"❌ Có lỗi xảy ra: {str(e)}")
    return

