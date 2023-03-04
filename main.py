from flask import Flask, request

import json
import os
import requests
from src.trading import BinanceTrading
from src.logger import logger

app = Flask(__name__)

binance_trading = BinanceTrading(os.environ.get('API_KEY'), os.environ.get('API_SECRET_KEY'))


@app.route('/webhook', methods=['POST'])
async def tradingview_request():
    data = json.loads(request.data)
    logger.info(data)
    if data.get('passphrase', None) != os.environ.get('PASSPHRASE'):
        logger.warning('Wrong passphrase')
        return {
            'code': 'error',
            'message': 'Invalid passphrase'
        }

    symbol = data.get('symbol')
    leverage = data.get('leverage')
    quantity = data.get('quantity')
    max_quantity_ratio = data.get('max_quantity_ratio')

    if data.get('message') == 'Sell' or data.get('message') == 'Buy_Exit':
        logger.info(f'SELL: {symbol}, leverage: {leverage}, quantity: {quantity}, max_quantity_ratio: {max_quantity_ratio}')
        binance_trading.sell(symbol, leverage, quantity, max_quantity_ratio)
    elif data.get('message') == 'Buy' or data.get('message') == 'Sell_Exit':
        logger.info(f'BUY: {symbol}, leverage: {leverage}, quantity: {quantity}, max_quantity_ratio: {max_quantity_ratio}')
        binance_trading.buy(symbol, leverage, quantity, max_quantity_ratio)
    return {"message": "successful"}


@app.route('/', methods=['GET'])
def home():
    return 'Hello, World!'


if __name__ == "__main__":
    my_ip = requests.get('https://api.my-ip.io/ip').text
    logger.info(f"My IP: {my_ip}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))
