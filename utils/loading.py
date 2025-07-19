import asyncio
from telegram import Update
from telegram.ext import ContextTypes

# Các emoji loading động
LOADING_EMOJIS = [
    "🔄", "⚡", "💫", "🌟", "✨", "💎", "🔥", "💥", "⚡", "🔄"
]

SPINNER_EMOJIS = [
    "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"
]

DOTS_EMOJIS = [
    "⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"
]

# Hiệu ứng loading nâng cao
ADVANCED_SPINNERS = [
    "🌍", "🌎", "🌏", "🌍", "🌎", "🌏"
]

MONEY_SPINNERS = [
    "💰", "💵", "💸", "💳", "💎", "💍", "💎", "💳", "💸", "💵"
]

STOCK_SPINNERS = [
    "📈", "📊", "📉", "📈", "📊", "📉"
]

COMPANY_SPINNERS = [
    "🏢", "🏭", "🏪", "🏬", "🏢", "🏭"
]

async def show_loading_status(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str = "🔄 Đang xử lý..."):
    """Hiển thị trạng thái loading cho người dùng"""
    try:
        # Gửi tin nhắn loading với emoji động
        loading_msg = await update.message.reply_text(message, parse_mode='HTML')
        
        # Bắt đầu hiển thị typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        return loading_msg
    except Exception as e:
        print(f"Lỗi khi hiển thị loading: {e}")
        return None

async def update_loading_message(loading_msg, new_message: str):
    """Cập nhật tin nhắn loading"""
    try:
        await loading_msg.edit_text(new_message, parse_mode='HTML')
    except Exception as e:
        print(f"Lỗi khi cập nhật loading message: {e}")

async def animate_loading(loading_msg, base_message: str, duration: int = 10):
    """Tạo hiệu ứng loading động"""
    try:
        for i in range(duration):
            # Sử dụng emoji xoay
            spinner = SPINNER_EMOJIS[i % len(SPINNER_EMOJIS)]
            animated_message = f"{spinner} {base_message}"
            
            await loading_msg.edit_text(animated_message, parse_mode='HTML')
            await asyncio.sleep(0.3)  # Cập nhật mỗi 300ms
            
    except Exception as e:
        print(f"Lỗi khi tạo animation: {e}")

async def show_animated_loading(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str = "Đang xử lý..."):
    """Hiển thị loading với animation"""
    try:
        # Bắt đầu với emoji đầu tiên
        spinner = SPINNER_EMOJIS[0]
        initial_message = f"{spinner} {message}"
        
        loading_msg = await update.message.reply_text(initial_message, parse_mode='HTML')
        
        # Bắt đầu hiển thị typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        return loading_msg
    except Exception as e:
        print(f"Lỗi khi hiển thị animated loading: {e}")
        return None

async def update_loading_with_animation(loading_msg, base_message: str, step: int = 0):
    """Cập nhật loading với animation"""
    try:
        # Sử dụng emoji xoay
        spinner = SPINNER_EMOJIS[step % len(SPINNER_EMOJIS)]
        animated_message = f"{spinner} {base_message}"
        
        await loading_msg.edit_text(animated_message, parse_mode='HTML')
    except Exception as e:
        print(f"Lỗi khi cập nhật animated loading: {e}")

async def update_loading_with_company_animation(loading_msg, base_message: str, step: int = 0):
    """Cập nhật loading với animation công ty"""
    try:
        spinner = COMPANY_SPINNERS[step % len(COMPANY_SPINNERS)]
        animated_message = f"{spinner} {base_message}"
        
        await loading_msg.edit_text(animated_message, parse_mode='HTML')
    except Exception as e:
        print(f"Lỗi khi cập nhật company animated loading: {e}")

async def update_loading_with_stock_animation(loading_msg, base_message: str, step: int = 0):
    """Cập nhật loading với animation cổ phiếu"""
    try:
        spinner = STOCK_SPINNERS[step % len(STOCK_SPINNERS)]
        animated_message = f"{spinner} {base_message}"
        
        await loading_msg.edit_text(animated_message, parse_mode='HTML')
    except Exception as e:
        print(f"Lỗi khi cập nhật stock animated loading: {e}")

async def update_loading_with_money_animation(loading_msg, base_message: str, step: int = 0):
    """Cập nhật loading với animation tiền tệ"""
    try:
        spinner = MONEY_SPINNERS[step % len(MONEY_SPINNERS)]
        animated_message = f"{spinner} {base_message}"
        
        await loading_msg.edit_text(animated_message, parse_mode='HTML')
    except Exception as e:
        print(f"Lỗi khi cập nhật money animated loading: {e}")

async def finish_loading(loading_msg, final_message: str):
    """Hoàn thành loading và gửi kết quả cuối cùng"""
    try:
        # Thêm emoji hoàn thành
        completion_emoji = "✅"
        final_with_emoji = f"{completion_emoji} {final_message}"
        
        await loading_msg.edit_text(final_with_emoji, parse_mode='HTML')
    except Exception as e:
        print(f"Lỗi khi hoàn thành loading: {e}")

async def finish_loading_with_error(loading_msg, error_message: str):
    """Hoàn thành loading với lỗi"""
    try:
        # Thêm emoji lỗi
        error_emoji = "❌"
        error_with_emoji = f"{error_emoji} {error_message}"
        
        await loading_msg.edit_text(error_with_emoji, parse_mode='HTML')
    except Exception as e:
        print(f"Lỗi khi hoàn thành loading với lỗi: {e}") 