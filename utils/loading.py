import asyncio
from telegram import Update
from telegram.ext import ContextTypes

# Loading emojis
LOADING_EMOJIS = [
    "🔄", "⚡", "💫", "🌟", "✨", "💎", "🔥", "💥", "⚡", "🔄"
]

SPINNER_EMOJIS = [
    "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"
]

DOTS_EMOJIS = [
    "⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"
]

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

async def show_loading_status(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str = "🔄 Processing..."):
    """Show loading status to user"""
    try:
        loading_msg = await update.message.reply_text(message, parse_mode='HTML')
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        return loading_msg
    except Exception as e:
        print(f"Error showing loading: {e}")
        return None

async def update_loading_message(loading_msg, new_message: str):
    """Update loading message"""
    try:
        if loading_msg is not None:
            await loading_msg.edit_text(new_message, parse_mode='HTML')
    except Exception as e:
        print(f"Error updating loading message: {e}")

async def animate_loading(loading_msg, base_message: str, duration: int = 10):
    """Create animated loading effect"""
    try:
        for i in range(duration):
            spinner = SPINNER_EMOJIS[i % len(SPINNER_EMOJIS)]
            animated_message = f"{spinner} {base_message}"
            await loading_msg.edit_text(animated_message, parse_mode='HTML')
            await asyncio.sleep(0.3)
    except Exception as e:
        print(f"Error creating animation: {e}")

async def show_animated_loading(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str = "Processing..."):
    """Show animated loading message"""
    try:
        spinner = SPINNER_EMOJIS[0]
        initial_message = f"{spinner} {message}"
        loading_msg = await update.message.reply_text(initial_message, parse_mode='HTML')
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        return loading_msg
    except Exception as e:
        print(f"Error showing animated loading: {e}")
        return None

async def update_loading_with_animation(loading_msg, base_message: str, step: int = 0):
    """Update loading with animation"""
    try:
        spinner = SPINNER_EMOJIS[step % len(SPINNER_EMOJIS)]
        animated_message = f"{spinner} {base_message}"
        await loading_msg.edit_text(animated_message, parse_mode='HTML')
    except Exception as e:
        print(f"Error updating animated loading: {e}")

async def update_loading_with_company_animation(loading_msg, base_message: str, step: int = 0):
    try:
        spinner = COMPANY_SPINNERS[step % len(COMPANY_SPINNERS)]
        animated_message = f"{spinner} {base_message}"
        if loading_msg is not None:
            await loading_msg.edit_text(animated_message, parse_mode='HTML')
    except Exception as e:
        print(f"Error updating company animated loading: {e}")

async def update_loading_with_stock_animation(loading_msg, base_message: str, step: int = 0):
    try:
        spinner = STOCK_SPINNERS[step % len(STOCK_SPINNERS)]
        animated_message = f"{spinner} {base_message}"
        if loading_msg is not None:
            await loading_msg.edit_text(animated_message, parse_mode='HTML')
    except Exception as e:
        print(f"Error updating stock animated loading: {e}")

async def update_loading_with_money_animation(loading_msg, base_message: str, step: int = 0):
    try:
        spinner = MONEY_SPINNERS[step % len(MONEY_SPINNERS)]
        animated_message = f"{spinner} {base_message}"
        if loading_msg is not None:
            await loading_msg.edit_text(animated_message, parse_mode='HTML')
    except Exception as e:
        print(f"Error updating money animated loading: {e}")

async def finish_loading(loading_msg, final_message: str, parse_mode: str = 'HTML'):
    """Finish loading and show final result"""
    try:
        completion_emoji = "✅"
        final_with_emoji = f"{completion_emoji} {final_message}"
        if loading_msg is not None:
            await loading_msg.edit_text(final_with_emoji, parse_mode=parse_mode)
        else:
            pass
    except Exception as e:
        print(f"Error finishing loading: {e}")

async def finish_loading_with_error(loading_msg, error_message: str):
    """Finish loading with error"""
    try:
        error_emoji = "❌"
        error_with_emoji = f"{error_emoji} {error_message}"
        if loading_msg is not None:
            await loading_msg.edit_text(error_with_emoji, parse_mode='HTML')
        else:
            pass
    except Exception as e:
        print(f"Error finishing loading with error: {e}") 