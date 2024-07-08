class Stock:
    def __init__(self, ticker, price, ebit_ev, roic, volume_traded):
        self.ticker = ticker
        self.price = price
        self.ebit_ev = ebit_ev
        self.roic = roic
        self.volume_traded = volume_traded
        self.return_rate = 0
        self.rank_bit_ev = 0
        self.rank_roic = 0
        self.final_rank = 0