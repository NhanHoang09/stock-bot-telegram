import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from utils.formatters import format_vnd
from utils.stock_info import get_full_stock_info
from utils.loading import (
    finish_loading, 
    finish_loading_with_error
)

try:
    from entities.coin_price.entity import StockPrice
    from entities.index import SessionLocal
except ImportError:
    StockPrice = None
    SessionLocal = None

async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please use: /stock <symbol> or /stock info <symbol>")
        return
    
    if context.args[0].lower() == "info":
        if len(context.args) <= 1:
            await update.message.reply_text("Please provide a stock symbol. Example: /stock info VNM")
            return
        symbol = context.args[1].upper()
        try:
            info = await get_full_stock_info(symbol, debug_raw=False, update=update)
            if info:
                await update.message.reply_text(info, parse_mode='HTML')
            else:
                await update.message.reply_text(f"No company information found for symbol: {symbol}")
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
        return
    
    symbol = context.args[0].upper()
    loading_msg = await update.message.reply_text("⏳ Fetching data, please wait...", parse_mode='HTML')
    
    try:
        from vnstock import Trading
        prices = Trading(source='TCBS').price_board([symbol])
        if prices.empty:
            await finish_loading_with_error(loading_msg, f"No stock found for symbol {symbol}")
            return
        # Try to extract price from possible columns
        price = None
        possible_columns = ['match_price', 'price', 'close', 'Giá']
        for col in possible_columns:
            if col in prices.columns:
                price = float(prices.iloc[0][col])
                break
        if price is None:
            # Try to find the first float column
            for col in prices.columns:
                val = prices.iloc[0][col]
                try:
                    price = float(val)
                    break
                except Exception:
                    continue
        if price is None:
            print('DEBUG: prices.columns =', prices.columns)
            await finish_loading_with_error(loading_msg, f"Could not extract price from columns: {list(prices.columns)}")
            return
        formatted_price = format_vnd(price)
        reply = f"💹 Current price of <b>{symbol}</b>: <b>{formatted_price}₫</b> 🇻🇳"
        if StockPrice and SessionLocal:
            session = SessionLocal()
            try:
                stock_price = StockPrice(symbol=symbol, price=price, timestamp=datetime.utcnow())
                session.add(stock_price)
                session.commit()
            except Exception as e:
                print(f"Database error: {e}")
            finally:
                session.close()
        await finish_loading(loading_msg, reply)
    except Exception as e:
        await finish_loading_with_error(loading_msg, f"Error: {e}")

