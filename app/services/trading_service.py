import pandas as pd

class TradingService:
    def __init__(self, stock_repo, meta_trader_repo):
        self.stock_repo = stock_repo
        self.meta_trader_repo = meta_trader_repo
        self.data = None
        self.portfolios = None
        self.portfolio_returns = None

    def download_and_load_data(self):
        dados_baixados = self.stock_repo.download_data()

        # Carrega os dados do arquivo CSV
        if dados_baixados is not None:
            self.data = self.stock_repo.load_data("../../app/data/dados_empresas_fundamentus.csv")
            print("Dados carregados com sucesso!")
            print(self.data)
        else:
            print("Falha ao carregar os dados.")
        
    def close_driver(self):
        self.driver.quit()

    # def calculate_returns(self):
    #     print(self.data)
    #    if self.data is not None:
    #         try:
    #            print("CALCULATING RETURNS")
    #            # Calcula os retornos percentuais por ticker
    #            self.data["retorno"] = self.data.groupby("Papel")["preco_fechamento_ajustado"].pct_change()
    #            # Shift para trazer os retornos de um dia para cima
    #            self.data["retorno"] = self.data.groupby("Papel")["retorno"].shift(-1)
    #            print(self.data)
    #        except Exception as e:
    #            print(f"Erro durante o cálculo de retornos: {e}")


    def filter_liquidity(self):
        if self.data is not None:
            self.data = self.data[self.data["Liq.2meses"] > 1000000]
            print(self.data)

    def rank_indicators(self):
        if self.data is not None:
            self.data = self.data[self.data["EV/EBIT"] > 0]
            self.data = self.data[self.data["ROIC"] > 0]
            self.data["ranking_ev_ebit"] = self.data["EV/EBIT"].rank(ascending = True)
            self.data["ranking_roic"] = self.data["ROIC"].rank(ascending = False)
            self.data["ranking_final"] = self.data["ranking_ev_ebit"] + self.data["ranking_roic"]
            print(self.data)

    def get_sector(self, ticker):
        try:
            sector = self.stock_repo.get_sector(ticker)
            return sector
        except Exception as e:
            print(f'Erro ao obter tipo para {ticker}: {e}')
            return None

    def create_portfolios(self):
        if self.data is not None:
            self.data['sector'] = self.data['Papel'].apply(self.get_sector)
            self.portfolios = self.data.groupby('sector').apply(
                lambda x: x.sort_values('ranking_final').head(10)['Papel'].tolist()
            )
            print(self.portfolios)

    def calculate_returns_per_portfolio(self):
        if self.data is not None:
            returns_data = []
            for sector, tickers in self.portfolios.items():
                returns = []
                for ticker in tickers:
                    return_value = self.stock_repo.get_return(ticker)
                    if return_value is not None:
                        returns.append(return_value)
                if returns:
                    average_return = sum(returns) / len(returns)
                    returns_data.append({'sector': sector, 'average_return': average_return})
            
            self.portfolio_returns = pd.DataFrame(returns_data)
            print(self.portfolio_returns)

    def calculate_model_returns(self):
        if self.portfolio_returns is not None:
            self.portfolio_returns["Magic Formula"] = (self.portfolio_returns["retorno"] + 1).cumprod() - 1
        print(self.portfolio_returns)

    def calculate_ibovespa_returns(self):
        if self.data is not None:
            ibovespa_data = self.data[self.data["ticker"] == "IBOV"]
            ibovespa_data = ibovespa_data.groupby("data")["retorno"].mean().to_frame()
            ibovespa_data["IBOV"] = (ibovespa_data["retorno"] + 1).cumprod() - 1
            self.ibovespa_returns = ibovespa_data[["IBOV"]]
        print(self.data)

    def analyze_results(self):
        if self.portfolio_returns is not None and self.ibovespa_returns is not None:
            self.comparison = self.portfolio_returns.join(self.ibovespa_returns)
            print(self.comparison)
        print(self.portfolio_returns)