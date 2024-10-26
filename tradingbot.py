# Import required libraries
import websocket
import json
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from datetime import datetime

# Constants
TRADE_SYMBOL = 'ETHUSDT'
TRADE_ASSET = 'ETH'
SOCKET = f"wss://stream.binance.com:9443/ws/{TRADE_SYMBOL.lower()}@kline_1m"
API_KEY = "xxxxxxxxxxxxxxxxxx"
API_SECRET = "xxxxxxxxxxxxxxxxxx"
MACD_PERIODS = [0, 3, 6, 9, 12, 15, 18, 21]
PRECISION = None

# Initialize Binance client
client = Client(API_KEY, API_SECRET)

def get_precision():
    global PRECISION
    info = client.get_symbol_info(TRADE_SYMBOL)
    PRECISION = info['baseAssetPrecision']

def get_balance(asset):
    balance = client.get_asset_balance(asset=asset)
    return float(balance['free'])

def get_symbol_price():
    avg_price = client.get_avg_price(symbol=TRADE_SYMBOL)
    return float(avg_price['price'])

def calculate_macd(closes, prev_ema_5, prev_ema_13, prev_signal):
    ema_5 = round((closes[-1] * (2 / (1 + 5))) + (prev_ema_5[-1] * (1 - (2 / (1 + 5)))), 4)
    ema_13 = round((closes[-1] * (2 / (1 + 13))) + (prev_ema_13[-1] * (1 - (2 / (1 + 13)))), 4)
    macd = ema_5 - ema_13
    signal_line = round((macd * (2 / (1 + 2))) + (prev_signal[-1] * (1 - (2 / (1 + 2)))), 4)
    return ema_5, ema_13, macd, signal_line

def create_order(side, quantity):
    try:
        order = client.create_order(symbol=TRADE_SYMBOL, side=side, type='MARKET', quantity=quantity)
        print(order)
    except (BinanceAPIException, BinanceOrderException) as e:
        print(e)

def on_open(ws):
    print("Opened connection")

def on_close(ws):
    print("Closed connection")

def on_message(ws, message):
    global closes
    now = datetime.utcnow()
    hour, minute, second = now.hour, now.minute, now.second
    macd_minutes = 60 - minute

    if hour in MACD_PERIODS:
        macd_countdown = f"2 hours {macd_minutes} minutes"
    elif (hour - 1) in MACD_PERIODS:
        macd_countdown = f"1 hour {macd_minutes} minutes"
    elif (hour - 2) in MACD_PERIODS:
        macd_countdown = f"{macd_minutes} minutes"

    print(f"Received message at {now.strftime('%H:%M.%S')}")
    json_message = json.loads(message)
    candle = json_message["k"]
    
    if hour in MACD_PERIODS and minute == 0 and second in {0, 1, 2}:
        close = float(candle["c"])
        closes.append(close)
        print(f"The latest closes are: {closes}")

        ema_5, ema_13, macd, signal_line = calculate_macd(closes, Previous_EMA_5, Previous_EMA_13, Previous_signal_line)
        Previous_EMA_5.append(ema_5)
        Previous_EMA_13.append(ema_13)
        Previous_signal_line.append(signal_line)

        print(f"EMA_5: {ema_5}, EMA_13: {ema_13}, MACD: {macd}, Signal Line: {signal_line}")

        if macd > signal_line:
            print("Buy!")
            usdt_balance = get_balance('USDT')
            symbol_price = get_symbol_price()
            buy_quantity = round(((usdt_balance - 0.01) / symbol_price), 8)
            create_order('BUY', buy_quantity)

        elif macd < signal_line:
            print("Sell!")
            trade_asset_balance = get_balance(TRADE_ASSET)
            sell_quantity = round(trade_asset_balance, PRECISION)
            create_order('SELL', sell_quantity)
    else:
        print(f"Time till next MACD calculation: {macd_countdown}")

# Initialize variables
closes = []
Previous_EMA_5 = [float(input("Enter the Latest EMA 5: "))]
Previous_EMA_13 = [float(input("Enter the Latest EMA 13: "))]
Previous_signal_line = [float(input("Enter the Latest Signal Line: "))]
get_precision()

# Websocket connection
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
