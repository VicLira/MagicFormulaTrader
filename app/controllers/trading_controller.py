from app.services.trading_service import TradingService
from app.repositories.stock_repository import StockRepository
from app.repositories.meta_trader_repository import MetaTraderRepository
from app.visualizations.dashboard import Dashboard

class TradingController:
    def __init__(self, mt5_login, mt5_password, mt5_server):
        self.stock_repo = StockRepository()
        self.meta_trader_repo = MetaTraderRepository(mt5_login, mt5_password, mt5_server)
        self.trading_service = TradingService(self.stock_repo, self.meta_trader_repo)
        self.dashboard = Dashboard()

    def execute(self):
        try:
            self.trading_service.download_and_load_data()
            print("DOWNLOAD E LOAD_DATA CONCLUIDOS")
            # self.trading_service.calculate_returns()
            # print("CALCULATE RETURNS CONCLUIDO")
            self.trading_service.filter_liquidity()
            print("FILTER LIQUIDITY CONCLUIDO")
            self.trading_service.rank_indicators()
            print("RANK INDICATORS CONCLUIDO")
            self.trading_service.create_portfolios()
            print("CREATE PORTFOLIOS CONCLUIDO")
            self.trading_service.calculate_returns_per_portfolio()
            print("CALCULATE RETURNS PER PORTFOLIO CONCLUIDO")
            self.trading_service.calculate_model_returns()
            print("CALCULATE MODEL RETURNS CONCLUIDO")
            self.trading_service.calculate_ibovespa_returns()
            print("CALCULATE IBOVESPA CONCLUIDO")
            self.trading_service.analyze_results()
            print("ANALYZE RESULTS CONCLUIDO")
            self.dashboard.visualize_results(self.trading_service.portfolio_returns)
            print("VIZUALIZE RESULTS RODANDO")
        except Exception as e:
            print(f"Erro durante a execução: {e}")
