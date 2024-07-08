from app.controllers.trading_controller import TradingController

from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()

    mt5_login = os.getenv('MT5_LOGIN')
    mt5_password = os.getenv('MT5_PASSWORD')
    mt5_server = os.getenv('MT5_SERVER')

    controller = TradingController(mt5_login=mt5_login, mt5_password=mt5_password, mt5_server=mt5_server)
    controller.execute()