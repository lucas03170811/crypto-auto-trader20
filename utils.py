import requests

def get_klines(symbol, interval="1m", limit=100):
    url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    return response.json()

def calculate_rsi(closing_prices, period=14):
    gains, losses = [], []
    for i in range(1, len(closing_prices)):
        change = closing_prices[i] - closing_prices[i - 1]
        if change > 0:
            gains.append(change)
        else:
            losses.append(abs(change))
    if not gains or not losses:
        return 50
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    return 100 - (100 / (1 + rs))

def calculate_volume_signal(klines):
    volumes = [float(k[5]) for k in klines]
    avg_volume = sum(volumes[:-1]) / len(volumes[:-1])
    return "BUY" if volumes[-1] > 1.5 * avg_volume else "SELL"
