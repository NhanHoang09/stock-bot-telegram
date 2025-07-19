import os
from watchfiles import run_process

def main():
    """Chạy bot với hot reload"""
    # Kiểm tra xem có bot modular không
    if os.path.exists('bot_new.py'):
        print("🚀 Chạy bot modular với hot reload...")
        run_process('.', target='python bot_new.py')
    elif os.path.exists('bot.py'):
        print("🚀 Chạy bot cũ với hot reload...")
        run_process('.', target='python bot.py')
    else:
        print("❌ Không tìm thấy file bot.py hoặc bot_new.py")
        print("💡 Hãy chạy: python split_commands.py để tạo bot modular")

if __name__ == "__main__":
    main() 