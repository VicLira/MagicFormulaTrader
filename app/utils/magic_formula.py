class MagicFormula:
    @staticmethod
    def apply(df):
        df['ranking_ev_ebit'] = df['EV/EBIT'].rank(ascending=True)
        df['ranking_roic'] = df['ROIC'].rank(ascending=False)
        df['ranking_total'] = df['ranking_ev_ebit'] + df['ranking_roic']
        return df.sort_values('ranking_total').head(10)