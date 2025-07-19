from telegram import Update
from telegram.ext import ContextTypes
import sqlite3
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Khởi tạo bot và lưu thông tin người dùng"""
    user = update.effective_user
    
    # Tạo database nếu chưa có
    if not os.path.exists('users.db'):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    # Lưu thông tin người dùng
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
    ''', (user.id, user.username, user.first_name, user.last_name))
    conn.commit()
    conn.close()
    
    welcome_message = f"""
🤖 <b>CHÀO MỪNG ĐẾN VỚI STOCK BOT!</b>

👋 Xin chào {user.first_name}!

📊 <b>Bot cung cấp:</b>
• Giá cổ phiếu thời gian thực
• Thông tin tài chính doanh nghiệp
• Biểu đồ và lịch sử giá
• Tin tức thị trường
• Bộ lọc cổ phiếu
• Quỹ đầu tư (ETF)
• Chỉ số thị trường
• Và nhiều tính năng khác...

💡 <b>Bắt đầu:</b>
• Gõ <code>/help</code> để xem tất cả lệnh
• Gõ <code>/stock VNM</code> để xem giá cổ phiếu
• Gõ <code>/market</code> để xem thị trường

🔗 <b>Liên hệ:</b> @nhanhoang09
"""
    
    await update.message.reply_text(welcome_message, parse_mode='HTML') 