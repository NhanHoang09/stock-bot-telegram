#!/usr/bin/env python3
"""
Script migration từ bot cũ sang bot modular
"""

import os
import shutil
from datetime import datetime

def backup_old_bot():
    """Backup bot cũ"""
    if os.path.exists('bot.py'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'bot_backup_{timestamp}.py'
        shutil.copy2('bot.py', backup_name)
        print(f"✅ Đã backup bot cũ thành: {backup_name}")
        return backup_name
    return None

def check_modules():
    """Kiểm tra các module đã được tạo"""
    required_modules = [
        'commands/basic/start.py',
        'commands/basic/help.py',
        'commands/stock/stock.py',
        'commands/stock/etf.py',
        'commands/stock/history.py',
        'commands/stock/realtime.py',
        'commands/stock/financial.py',
        'commands/stock/company.py',
        'commands/market/market.py',
        'commands/market/top.py',
        'commands/market/sector.py',
        'commands/market/index.py',
        'commands/funds/funds.py',
        'commands/news/news.py',
        'commands/filter/filter.py',
        'commands/analysis/commodities.py',
        'utils/formatters.py',
        'utils/stock_info.py',
        'bot_new.py'
    ]
    
    missing_modules = []
    for module in required_modules:
        if not os.path.exists(module):
            missing_modules.append(module)
    
    if missing_modules:
        print("❌ Thiếu các module sau:")
        for module in missing_modules:
            print(f"   - {module}")
        return False
    
    print("✅ Tất cả modules đã được tạo")
    return True

def migrate():
    """Thực hiện migration"""
    print("🚀 Bắt đầu migration từ bot cũ sang bot modular...")
    
    # 1. Backup bot cũ
    backup_file = backup_old_bot()
    
    # 2. Kiểm tra modules
    if not check_modules():
        print("❌ Migration thất bại: Thiếu modules")
        return False
    
    # 3. Tách commands nếu chưa có
    if not os.path.exists('commands/stock/stock.py'):
        print("📦 Tách commands từ bot cũ...")
        os.system('python split_commands.py')
    
    # 4. Đổi tên bot mới thành bot chính
    if os.path.exists('bot_new.py'):
        shutil.move('bot_new.py', 'bot.py')
        print("✅ Đã đổi tên bot_new.py thành bot.py")
    
    # 5. Tạo file .gitignore cho backup
    with open('.gitignore', 'a') as f:
        f.write('\n# Backup files\nbot_backup_*.py\n')
    
    print("\n🎉 Migration hoàn thành!")
    print("📊 Bot modular đã sẵn sàng sử dụng")
    print("🔧 Để rollback: mv bot.py bot_new.py && mv bot_backup_*.py bot.py")
    
    return True

def rollback():
    """Rollback về bot cũ"""
    backup_files = [f for f in os.listdir('.') if f.startswith('bot_backup_')]
    
    if not backup_files:
        print("❌ Không tìm thấy file backup")
        return False
    
    # Lấy file backup mới nhất
    latest_backup = max(backup_files)
    
    if os.path.exists('bot.py'):
        shutil.move('bot.py', 'bot_new.py')
    
    shutil.copy2(latest_backup, 'bot.py')
    print(f"✅ Đã rollback về: {latest_backup}")
    
    return True

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'rollback':
            rollback()
        elif sys.argv[1] == 'check':
            check_modules()
        else:
            print("Usage: python migrate.py [migrate|rollback|check]")
    else:
        migrate()

if __name__ == "__main__":
    main() 