# Automated-Trading-
This repository contains a Python-based trading bot that uses the OANDA API and the yfinance library to perform automated trading on the EUR/USD currency pair. The bot implements a simple trading strategy based on candlestick patterns and manages trades with take profit and stop loss settings.


# Forex Trading Bot

This repository contains a Python-based trading bot that uses the OANDA API and the `yfinance` library to perform automated trading on the EUR/USD currency pair. The bot implements a simple trading strategy based on candlestick patterns and manages trades with take profit and stop loss settings.

## Features

- **Market Data Retrieval**: Downloads historical EUR/USD data at 15-minute intervals using the `yfinance` library.
- **Signal Generation**: Implements a signal generator that identifies bullish and bearish patterns based on recent candlestick data.
- **Trading Logic**: Executes market orders based on generated signals, with automated handling of take profit and stop loss levels.
- **Scheduled Execution**: The bot can be scheduled to run at specified intervals using APScheduler, allowing for automated trading throughout the week.

## Dependencies

- `yfinance`
- `pandas`
- `apscheduler`
- `oandapyV20`
- `oanda_candles`

## Usage

1. **Setup**: 
   - Install the required dependencies using pip:
     ```bash
     pip install yfinance pandas apscheduler oandapyV20 oanda_candles
     ```
   - Update the `access_token` and `accountID` variables with your OANDA account details.

2. **Run the Bot**:
   - You can manually run the bot by executing the script or set it up with a scheduler for automated trading.
   - To execute a trade, the `trading_job` function is called, which retrieves the latest candle data, generates a signal, and executes a market order accordingly.

3. **Modify Trading Parameters**:
   - Adjust the `SLTPRatio` for take profit and stop loss settings.
   - Change the currency pair and trading intervals by modifying the relevant parameters in the code.

## Important Notes

- **Risk Management**: Ensure you understand the risks involved in automated trading. This bot is intended for educational purposes and may not be suitable for live trading without further modifications and testing.
- **API Limits**: Be mindful of OANDA’s API limits and ensure your implementation adheres to them to avoid being rate-limited.

