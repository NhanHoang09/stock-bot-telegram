import pandas as pd
import pandas_ta as pta
# from vnstock import stock_historical_data  # Bản vnstock hiện tại không hỗ trợ hàm này, hãy dùng class Vnstock nếu cần lấy dữ liệu lịch sử
from telegram import Update
from telegram.ext import CallbackContext
from vnstock import Vnstock  # Thêm import class Vnstock

def get_technical_summary(symbol: str, start_date: str, end_date: str) -> str:
    try:
        """
        Fetch OHLCV data for a given symbol and date range, calculate key technical indicators,
        and return a formatted summary string in English.
        """
        # df = stock_historical_data(symbol=symbol, start_date=start_date, end_date=end_date, resolution="1D")
        # Đổi source từ 'VCI' sang 'TCBS'
        stock = Vnstock().stock(symbol=symbol, source='TCBS')
        df = stock.quote.history(start=start_date, end=end_date, interval='1D')
        if df is None or df.empty:
            return f"No data available for symbol {symbol} in the selected date range."

        # Debug: print DataFrame info
        print("DataFrame head:\n", df.head())
        print("DataFrame columns:", df.columns)
        print("DataFrame info:")
        print(df.info())
        print("Null values per column:\n", df.isnull().sum())

        # Check required columns
        required_columns = {'open', 'high', 'low', 'close', 'volume'}
        if not required_columns.issubset(df.columns):
            return f"Data for {symbol} is missing required columns: {required_columns - set(df.columns)}"

        # Check for null values in required columns
        if df[['open', 'high', 'low', 'close', 'volume']].isnull().any().any():
            return f"Data for {symbol} contains null values in required columns."

        # Momentum
        df['rsi'] = pta.rsi(df['close'], length=14)
        stoch = pta.stoch(df['high'], df['low'], df['close'])
        df['stoch_k'] = stoch['STOCHk_14_3_3'] if 'STOCHk_14_3_3' in stoch else None
        df['cci'] = pta.cci(df['high'], df['low'], df['close'], length=20)

        # Trend
        macd = pta.macd(df['close'])
        df = df.join(macd)
        df['ema_20'] = pta.ema(df['close'], length=20)
        df['sma_50'] = pta.sma(df['close'], length=50)
        adx = pta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx['ADX_14'] if 'ADX_14' in adx else None

        # Volatility
        bbands = pta.bbands(df['close'])
        df = df.join(bbands)
        df['atr'] = pta.atr(df['high'], df['low'], df['close'], length=14)

        # Volume
        df['obv'] = pta.obv(df['close'], df['volume'])
        df['mfi'] = pta.mfi(df['high'], df['low'], df['close'], df['volume'], length=14)

        latest = df.iloc[-1]
        summary = (
            f"Technical indicators for {symbol} (latest data):\n"
            f"- RSI: {latest['rsi']:.2f}\n"
            f"- Stochastic %K: {latest['stoch_k']:.2f}\n"
            f"- CCI: {latest['cci']:.2f}\n"
            f"- MACD: {latest.get('MACD_12_26_9', float('nan')):.2f}\n"
            f"- MACD Signal: {latest.get('MACDs_12_26_9', float('nan')):.2f}\n"
            f"- EMA 20: {latest['ema_20']:.2f}\n"
            f"- SMA 50: {latest['sma_50']:.2f}\n"
            f"- ADX: {latest['adx']:.2f}\n"
            f"- Bollinger Bands: Upper {latest.get('BBU_20_2.0', float('nan')):.2f}, Lower {latest.get('BBL_20_2.0', float('nan')):.2f}\n"
            f"- ATR: {latest['atr']:.2f}\n"
            f"- OBV: {latest['obv']:.2f}\n"
            f"- MFI: {latest['mfi']:.2f}"
        )
        return summary
    except Exception as e:
        return f"Đã xảy ra lỗi khi lấy dữ liệu kỹ thuật: {e}"


async def ta_technical(update: Update, context: CallbackContext) -> None:
    """
    Telegram command handler for /ta_technical.
    Usage: /ta_technical <symbol> [start_date] [end_date]
    """
    args = context.args
    if len(args) < 1:
        await update.message.reply_text(
            "Please provide a stock symbol. Example: /ta_technical VNM [start_date] [end_date]"
        )
        return
    symbol = args[0].upper()
    start_date = args[1] if len(args) > 1 else "2023-01-01"
    end_date = args[2] if len(args) > 2 else "2023-12-31"
    summary = get_technical_summary(symbol, start_date, end_date)
    await update.message.reply_text(summary) 