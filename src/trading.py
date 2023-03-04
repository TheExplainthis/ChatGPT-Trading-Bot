from binance import Client


class BinanceLeverage:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)
        self.leverage_mapping = {}

    def change_leverage(self, symbol, leverage):
        self.leverage_mapping[symbol] = leverage
        self.client.futures_change_leverage(symbol=symbol, leverage=leverage)


class BinanceBalance:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_max_qty(self, symbol, leverage):
        account_balance = self.client.futures_account_balance()
        ticker_price = self.client.futures_symbol_ticker(symbol=symbol)
        mark_price = float(ticker_price['price'])
        for asset in account_balance:
            if asset['asset'] == symbol[-4:]:
                balance = float(asset['balance'])
        return balance * leverage / mark_price


class BinanceOrder:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)
        self.leverage = BinanceLeverage(api_key, api_secret)
        self.balance = BinanceBalance(api_key, api_secret)

    def get_precision(self, symbol):
        info = self.client.futures_exchange_info()
        for x in info['symbols']:
            if x['symbol'] == symbol:
                return x['quantityPrecision']

    def create_order(self, side, symbol, leverage, quantity=None, max_quantity_ratio=0.1):
        self.leverage.change_leverage(symbol, leverage)
        if not quantity:
            quantity = self.balance.get_max_qty(symbol, leverage) * max_quantity_ratio
        precision = self.get_precision(symbol)
        quantity = float(round(quantity, precision))
        self.client.futures_create_order(
            symbol=symbol,
            type='MARKET',
            side=side,
            quantity=quantity
        )


class BinanceTrading:
    def __init__(self, api_key, api_secret):
        self.order = BinanceOrder(api_key, api_secret)

    def buy(self, symbol, leverage, quantity=None, max_quantity_ratio=0.1):
        self.order.create_order(Client.SIDE_BUY, symbol, leverage, quantity, max_quantity_ratio)

    def sell(self, symbol, leverage, quantity=None, max_quantity_ratio=0.1):
        self.order.create_order(Client.SIDE_SELL, symbol, leverage, quantity, max_quantity_ratio)