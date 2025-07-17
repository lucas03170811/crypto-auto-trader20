import os
import time
from binance.client import Client
from binance.error import ClientError
from utils import calculate_rsi, calculate_volume_signal, get_klines

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

client = UMFutures(key=API_KEY, secret=API_SECRET)
symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT"]
quantity = 0.05

def check_and_trade():
    for symbol in symbols:
        try:
            klines = get_klines(symbol, "1m", 100)
            rsi = calculate_rsi([float(k[4]) for k in klines])
            vol_signal = calculate_volume_signal(klines)

            position = client.get_position_risk(symbol=symbol)
            pos_amt = float(position[0]["positionAmt"])

            mark_price = float(client.mark_price(symbol=symbol)["markPrice"])
            entry_price = float(position[0]["entryPrice"])
            pnl = (mark_price - entry_price) / entry_price * 100 if pos_amt != 0 else 0

            if rsi < 30 and vol_signal == "BUY" and pos_amt == 0:
                print(f"[{symbol}] 開多單")
                client.new_order(symbol=symbol, side="BUY", type="MARKET", quantity=quantity)
            elif rsi > 70 and vol_signal == "SELL" and pos_amt == 0:
                print(f"[{symbol}] 開空單")
                client.new_order(symbol=symbol, side="SELL", type="MARKET", quantity=quantity)
            elif pos_amt > 0 and pnl > 5:
                print(f"[{symbol}] 多單平倉 +5%")
                client.new_order(symbol=symbol, side="SELL", type="MARKET", quantity=abs(pos_amt))
            elif pos_amt < 0 and pnl < -5:
                print(f"[{symbol}] 空單止損 -5%")
                client.new_order(symbol=symbol, side="BUY", type="MARKET", quantity=abs(pos_amt))

        except ClientError as e:
            print(f"Error: {e}")
        time.sleep(1)
