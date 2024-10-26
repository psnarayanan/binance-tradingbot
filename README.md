# Binance Trading Bot
This trading bot template uses the Binance API to create Buy and Sell orders based on the MACD (5,13,2) strategy on 3-hour charts. The bot connects to Binance's WebSocket to receive real-time price data and executes trades automatically. This code serves as a bare minimum working template for building more advanced strategies later on.

## Features
1. Real-time Price Data: Connects to Binance WebSocket for up-to-the-minute price information.
2. MACD Strategy: Implements the MACD (5,13,2) strategy for making buy and sell decisions.
3. Automated Trading: Places market orders based on the MACD signals.
4. Balance Monitoring: Checks and prints the user's USDT and ETH balances before making trades.

## Requirements
- Python 3.x
- websocket-client library
- python-binance library

## Installation

Clone the repository:
```
git clone https://github.com/yourusername/binance-trading-bot.git
cd binance-trading-bot
```

Install dependencies:
```
pip install -r requirements.txt
```

## Configuration
API Keys: Obtain your Binance API Key and Secret from your Binance account and replace the placeholders in the code:

```python
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"
```
Initial EMA and Signal Values: Input the latest EMA and Signal Line values when prompted:

```
Previous_EMA_5 = [float(input("Enter the Latest EMA 5: "))]
Previous_EMA_13 = [float(input("Enter the Latest EMA 13: "))]
Previous_signal_line = [float(input("Enter the Latest Signal Line: "))]
```

## Usage

Run the bot using Python:
```
python trading_bot.py
```
Upon starting, the bot will:


1. Connect to Binance WebSocket and print "Opened connection".
2. Prompt for the latest EMA and Signal Line values.
3. Retrieve and print your USDT and ETH balances.
4. Monitor the price data and execute trades based on the MACD strategy every 3 hours.

## Functions:
- get_precision(): Retrieves asset precision.
- get_balance(asset): Returns the balance of a specified asset.
- get_symbol_price(): Returns the current symbol price.
- calculate_macd(closes, prev_ema_5, prev_ema_13, prev_signal): Calculates the EMA and MACD values.
- create_order(side, quantity): Places a market order.
- on_open(ws): Called when WebSocket connection opens.
- on_close(ws): Called when WebSocket connection closes.
- on_message(ws, message): Main logic for receiving and processing messages.

## Notes
- This code is a bare minimum working template designed for building more advanced trading strategies. You can extend it with additional indicators, risk management, and other custom logic as needed.
- Ensure you have sufficient balance and permissions for trading on your Binance account.
- Use a test environment or small amounts when testing to avoid unintended large trades.
- The bot currently trades ETH/USDT pair. To change the pair, modify the TRADE_SYMBOL and TRADE_ASSET constants.

## Disclaimer
Trading cryptocurrencies involves significant risk and may not be suitable for all investors. This bot is provided "as is" without any warranty and is for educational purposes only. Use it at your own risk.
