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
        
        df.to_csv(self._pathing(sector, sub) + str(stock) + '.csv', index=False)

    def _download_stock(self, stock: str):
        with open("/dev/null", "w") as null_file:
            with redirect_stdout(null_file):
                df = yf.download(stock, self.start, self.end)
        df['Return'] = df['Adj Close'].pct_change()
        df['Symbol'] = str(stock)
        return df
    
    def _download_adj_close(self, stock: str):
        with open("/dev/null", "w") as null_file:
            with redirect_stdout(null_file):
                df = yf.download(stock, self.start, self.end)

        df = df[['Adj Close']].rename(columns={'Adj Close':str(stock)})
        return df

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

    def concat_sector(self, sector: str):
        total = self.sp500.loc[self.sp500['GICS Sector'] == sector, 'Symbol'].shape[0]
        companies = []
        ii = 1
        for industry in self.get_subindustry(sector):
            for stock in self.get_stock(sector, industry):
                df = self._download_stock(stock)
                progress = "Downloading file {} of {}".format(ii, total)
                ii = ii + 1
                print(progress, end='\r')
                companies.append(df)

        companies = pd.concat(companies)
        return companies

    def adj_close_sector(self, sector: str):
        total = self.sp500.loc[self.sp500['GICS Sector'] == sector, 'Symbol'].shape[0]
        companies = []
        ii = 1
        for industry in self.get_subindustry(sector):
            for stock in self.get_stock(sector, industry):
                df = self._download_adj_close(stock)
                progress = "Downloading file {} of {}".format(ii, total)
                ii = ii + 1
                print(progress, end='\r')
                companies.append(df.reset_index())

        merge = reduce(lambda left, right: pd.merge(left, right, on='Date', how='outer'), companies)
        merge = merge.set_index('Date')
        merge_mean = pd.DataFrame(merge.mean(axis=1), columns=[str(sector)])
        return merge_mean
    
    def adj_close_mean_sector(self):
        sector = self.get_sector()
        dfs = []
        for s in sector:
            dfs.append(self.adj_close_sector(s).reset_index())

        merge = reduce(lambda left, right: pd.merge(left, right, on='Date', how='outer'), dfs)
        merge.set_index('Date', inplace=True)
        return merge
    
    # def sector_dividends(self, sector: str):
    #     dividend, ii = [], 1
    #     total =  self.sp500.loc[self.sp500['GICS Sector'] == sector, 'Symbol'].shape[0]

    #     for industry in self.get_subindustry(sector):
    #         for stock in self.get_stock(sector, industry):
    #             divd = pd.DataFrame(yf.Ticker(stock).dividends, columns=['Dividends']).reset_index()
    #             divd['Date'] = pd.to_datetime(divd['Date']).dt.date
    #             divd = divd.loc[divd['Date'] >= pd.to_datetime(self.start)]
    #             dividend.append(divd)

    #             progress = "Downloading file {} of {}".format(ii, total)
    #             ii = ii + 1
    #             print(progress, end='\r')
        
    #     # dividend = reduce(lambda left, right: pd.merge(left, right, on='Date', how='outer'), dividend)
    #     # dividend_mean = pd.DataFrame(dividend.mean(axis=1), columns=[str(sector)+' Mean Dividend'])
    #     return dividend


# F = Finance()
# print(F.concat_sector('Energy').head())