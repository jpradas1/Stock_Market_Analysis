import numpy as np
import pandas as pd
from datetime import datetime

import os
from contextlib import redirect_stdout
from functools import reduce

import yfinance as yf

import warnings
warnings.filterwarnings('ignore')

class Finance(object):
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500 = pd.read_html(url)[0]

    end = datetime.now()
    start = datetime(2000, 1, 1)

    def get_sector(self):
        sectors = self.sp500['GICS Sector'].unique()
        sectors = [x for x in sectors]
        return sectors
    
    def get_subindustry(self, sector: str):
        subind = self.sp500.loc[self.sp500['GICS Sector'] == sector]['GICS Sub-Industry'].unique()
        subind = [x for x in subind]
        return subind
    
    def get_stock(self, sector: str, sub: str):
        stock = self.sp500.loc[(self.sp500['GICS Sector'] == sector) \
                               & (self.sp500['GICS Sub-Industry'] == sub), 'Symbol'] \
                               .values
        stock = [x for x in stock]
        return stock
    
    def _pathing(self, sector: str, sub: str):
        path = './dataset/{}/{}/'.format(sector, sub)

        if not os.path.exists(path):
            os.makedirs(path)

        return path
    
    def _download_stock_csv(self, sector: str, sub: str, stock: str):
        with open("/dev/null", "w") as null_file:
            with redirect_stdout(null_file):
                df = yf.download(stock, self.start, self.end)
        
        df.to_csv(self._pathing(sector, sub) + str(stock) + '.csv')

    def create_csv(self):
        total = self.sp500['Symbol'].values.shape[0]
        ii = 1
        for sector in self.get_sector():
            for industry in self.get_subindustry(sector):
                for stock in self.get_stock(sector, industry):
                    self._download_stock_csv(sector, industry, stock)
                    progress = f"Downloading file {ii} of {total}"
                    ii = ii + 1
                    print(progress, end='\r')

    def verify_stock(self, sector: str, sub: str, stock: str):
        path = './dataset/{}/{}/{}.csv'.format(sector, sub, stock)
        try:
            if os.path.exists(path):
                pass
            else:
                self._download_stock_csv(sector, sub, stock)
        except:
            pass
    
    def _local_adj_close(self, sector:str, sub: str, stock: str):
        self.verify_stock(sector, sub, stock)
        path = './dataset/{}/{}/'.format(sector, sub)
        df = pd.read_csv(path + str(stock) + '.csv')
        df = df[['Date','Adj Close']].rename(columns={'Adj Close':str(stock)})
        return df

    def adj_close_sector(self, sector: str):
        companies = []
        for industry in self.get_subindustry(sector):
            for stock in self.get_stock(sector, industry):
                df = self._local_adj_close(sector, industry, stock)
                companies.append(df)

        merge = reduce(lambda left, right: pd.merge(left, right, on='Date', how='outer'), companies)
        merge = merge.set_index('Date')
        merge_mean = pd.DataFrame(merge.sum(axis=1), columns=[str(sector)])
        return merge_mean
    
    def adj_close_mean_sector(self):
        sector = self.get_sector()
        dfs = []
        for s in sector:
            dfs.append(self.adj_close_sector(s).reset_index())

        merge = reduce(lambda left, right: pd.merge(left, right, on='Date', how='outer'), dfs)
        merge.set_index('Date', inplace=True)
        return merge
    
    def adj_close_industry(self, sector: str, sub: str):
        companies = []
        for stock in self.get_stock(sector, sub):
            df = self._local_adj_close(sector, sub, stock)
            companies.append(df)

        merge = reduce(lambda left, right: pd.merge(left, right, on='Date', how='outer'), companies)
        merge = merge.set_index('Date')
        merge_total = pd.DataFrame(merge.sum(axis=1), columns=[str(sub)])
        return merge_total
    
    def adj_close_total_sub(self, sector: str):
        industry = self.get_subindustry(sector)
        dfs = []
        for ii in industry:
            dfs.append(self.adj_close_industry(sector, ii))

        merge = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True), dfs)
        return merge

def Returns_Risk(df_adj_close: pd.DataFrame, time_type: str):
    F = Finance()
    ttype = time_type.lower()[0]
    type = {'y': "%Y", 'm': "%Y-%m", 'w': "%Y-%U"}

    df_returns = round(df_adj_close.pct_change()*100, 2)
    df_returns.index = pd.to_datetime(df_returns.index)

    volatility, expected_return, total_return = [], [], []
    for item in df_returns.columns:
        v = df_returns[item].std()
        m = df_returns[item].mean()
        t = df_returns[item].sum()
        expected_return.append(m)
        volatility.append(v)
        total_return.append(t)

    sample = zip(df_returns.columns, expected_return, volatility, total_return)
    risk = {k: [ex, vo, t] for (k, ex, vo, t) in sample}
    risk = pd.DataFrame(risk, index=['Expected Return', 'Volatility', 'Total Return']).T
    risk = risk.reset_index()
    risk.rename(columns={'index':'Sector'}, inplace=True)

    df_returns[time_type] = df_returns.index.strftime(type[ttype])
    df_returns = df_returns.groupby(time_type).sum()

    return df_returns, risk

# sector = 'Health Care'
# sub = 'Biotechnology'
# df = Finance().adj_close_total_sub(sector)
# print(Returns_Risk(df, 'year'))