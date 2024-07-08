import MetaTrader5 as mt5

class MetaTraderRepository:
    def __init__(self, login, password, server):
        self.login = login
        self.password = password
        self.server = server

        print(self.login, self.password, self.server)

    def initialize_mt5(self):
        mt5.initialize()
        authorized = mt5.login(self.login, self.password)

        if not authorized:
            print(f"Failed to connect to account: {mt5.last_error()}")
        else:
            print("Connected to MetaTrader 5")
            print(mt5.account_info())

    def buy_stocks(self, tickers):
        for ticker in tickers:
            mt5.symbol_select(ticker)
            price = mt5.symbol_info_tick(ticker).ask
            quantity = 100.0
            order = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": ticker,
                "volume": quantity,
                "type": mt5.ORDER_TYPE_BUY,
                "price": price,
                "magic": 1,
                "comment": "Trades automáticos",
                "type_time": mt5.ORDER_TIME_DAY,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }
            mt5.order_send(order)