#!/usr/bin/env python3
"""
Script để tách các command từ file bot.py cũ thành các module riêng biệt
"""

import re
import os

def extract_function_content(file_path, function_name):
    """Trích xuất nội dung của một function từ file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Tìm function
    pattern = rf'async def {function_name}\(.*?\):(.*?)(?=async def|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    return None

def create_module_file(module_path, function_name, function_content, imports=None):
    """Tạo file module với function"""
    os.makedirs(os.path.dirname(module_path), exist_ok=True)
    
    with open(module_path, 'w', encoding='utf-8') as f:
        if imports:
            f.write(imports + '\n\n')
        
        f.write(f'async def {function_name}(update: Update, context: ContextTypes.DEFAULT_TYPE):\n')
        f.write(function_content)
        f.write('\n')

def main():
    """Tách các command từ bot.py"""
    
    # Định nghĩa cấu trúc modules
    modules = {
        'commands/stock/stock.py': {
            'functions': ['stock'],
            'imports': '''from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd
from utils.stock_info import get_full_stock_info'''
        },
        'commands/stock/etf.py': {
            'functions': ['etf'],
            'imports': '''from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd'''
        },
        'commands/stock/history.py': {
            'functions': ['history'],
            'imports': '''from telegram import Update
from telegram.ext import ContextTypes
import matplotlib.pyplot as plt
import os
from utils.formatters import format_vnd'''
        },
        'commands/stock/realtime.py': {
            'functions': ['realtime'],
            'imports': '''from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd'''
        },
        'commands/stock/financial.py': {
            'functions': ['financial'],
            'imports': '''from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd'''
        },
        'commands/stock/company.py': {
            'functions': ['company'],
            'imports': '''from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd
from utils.stock_info import get_company_info'''
        },
        'commands/market/market.py': {
            'functions': ['market'],
            'imports': '''from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd'''
        },
        'commands/market/top.py': {
            'functions': ['top'],
            'imports': '''from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd'''
        },
        'commands/market/sector.py': {
            'functions': ['sector'],
            'imports': '''from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd'''
        },
        'commands/market/index.py': {
            'functions': ['index', 'index_detail', 'index_history', 'index_compare', 'index_sector'],
            'imports': '''from telegram import Update
from telegram.ext import ContextTypes
import matplotlib.pyplot as plt
import os
from utils.formatters import format_vnd'''
        },
        'commands/funds/funds.py': {
            'functions': ['funds', 'fund_detail', 'fund_performance', 'fund_compare', 'fund_sector', 'fund_ranking'],
            'imports': '''from telegram import Update
from telegram.ext import ContextTypes
import matplotlib.pyplot as plt
import os
from utils.formatters import format_vnd'''
        },
        'commands/news/news.py': {
            'functions': ['news', 'news_stock', 'market_news', 'events', 'calendar', 'announcements'],
            'imports': '''from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta'''
        },
        'commands/filter/filter.py': {
            'functions': ['filter_pe', 'filter_roe', 'filter_market_cap', 'filter_volume', 'filter_price', 'filter_sector', 'screener'],
            'imports': '''from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd'''
        },
        'commands/analysis/commodities.py': {
            'functions': ['gold', 'metals', 'commodities'],
            'imports': '''from telegram import Update
from telegram.ext import ContextTypes
from utils.formatters import format_vnd'''
        }
    }
    
    # Tạo các module
    for module_path, config in modules.items():
        print(f"Tạo module: {module_path}")
        
        # Tạo __init__.py cho package
        package_dir = os.path.dirname(module_path)
        init_file = os.path.join(package_dir, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write(f"# {os.path.basename(package_dir)} package\n")
        
        # Tạo module file
        with open(module_path, 'w', encoding='utf-8') as f:
            f.write(config['imports'] + '\n\n')
            
            for function_name in config['functions']:
                print(f"  - Trích xuất function: {function_name}")
                function_content = extract_function_content('bot.py', function_name)
                
                if function_content:
                    f.write(f'async def {function_name}(update: Update, context: ContextTypes.DEFAULT_TYPE):\n')
                    f.write(function_content)
                    f.write('\n\n')
                else:
                    print(f"    ⚠️ Không tìm thấy function: {function_name}")
    
    print("\n✅ Hoàn thành tách commands!")
    print("📁 Cấu trúc thư mục mới:")
    print("commands/")
    print("├── basic/")
    print("│   ├── start.py")
    print("│   └── help.py")
    print("├── stock/")
    print("│   ├── stock.py")
    print("│   ├── etf.py")
    print("│   ├── history.py")
    print("│   ├── realtime.py")
    print("│   ├── financial.py")
    print("│   └── company.py")
    print("├── market/")
    print("│   ├── market.py")
    print("│   ├── top.py")
    print("│   ├── sector.py")
    print("│   └── index.py")
    print("├── funds/")
    print("│   └── funds.py")
    print("├── news/")
    print("│   └── news.py")
    print("├── filter/")
    print("│   └── filter.py")
    print("└── analysis/")
    print("    └── commodities.py")
    print("\nutils/")
    print("├── formatters.py")
    print("└── stock_info.py")

if __name__ == "__main__":
    main() 