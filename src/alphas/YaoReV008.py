# Reversion 008: divergence from industry mean
# return - cor_return ; cor_return = mean(max_corr(return, other_return, n)))
# we use return instead of price
# cor_return is defined on an industry level (group mean)
# we also compute moving average on cor_return and return
# two parameters: look back window, and number of neighbors

from logger import logger as myLogger
from loader import dataloader
from pathmgmt import pathmgmt as myPath
from utils.calendar import CALENDAR, START, END
import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime
from functools import partial
import logging
from multiprocessing import Pool
import warnings
import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS
warnings.filterwarnings('ignore')

#

# Local Library imports

logger = myLogger.Logger(__name__)
logger.init(console_handler=True)


class YaoReV008():
    def __init__(self, args_dict):
        self.__name = 'YaoReV008'
        self.__universe = args_dict['universe']
        self.__start = args_dict['start_date']
        self.__end = args_dict['end_date']
        self.__window = args_dict['window']
        self.__neighbor = args_dict['neighbor']
        # self.__delay = args_dict['delay'] # Delay 0? Delay 1?
        self.__refresh = True if 'refresh' not in args_dict else args_dict['refresh']

    def __compute_return(self, x):
        '''function to compute lag return'''
        return np.log(x.shift(1)) - np.log(x.shift(1 + self.__window))

    def __compute_corr_price(self, stocks):        
        stocks['ret_1d'] = stocks.groupby(
            'code').adj_close.apply(lambda x: np.log(x.shift(1)) - np.log(x.shift(2)))
        
        industry = dataloader.loading(
            tab_name="Sector", start=self.__start, end=self.__end, fields=['code', 'sw1', 'sw2', 'sw3'])
        stocks = pd.merge(stocks.reset_index(), industry.reset_index(), left_on=[
            'time', 'code'], right_on=['time', 'code'], how='left')
        stocks_pivot = stocks.pivot_table(
            index='time', columns=['sw1'], values='ret_1d', aggfunc=np.mean)
        
        rolling_corr = stocks_pivot.rolling(self.__window).corr().reset_index().dropna()
        
        arank = rolling_corr.iloc[:, 2:].apply(np.argsort, axis=1)
        cols = rolling_corr.iloc[:, 2:].columns
        
        for i in range(self.__neighbor):
            rolling_corr[f'nlargest_{i}'] = cols[arank][:, -(i+1)]
        
        stocks_sw1_rolling_ret = rolling_corr[['time', 'sw1'] +
                                              [f'nlargest_{i}' for i in range(self.__neighbor)]]
        stocks = pd.merge(stocks, stocks_sw1_rolling_ret, left_on=[
            'time', 'sw1'], right_on=['time', 'sw1'], how='left')
        
        industry_rolling = stocks.groupby(['time', 'sw1']).ret_1d.mean(
            ).reset_index().set_index('time').groupby('sw1').rolling(self.__window).mean().reset_index()
        
        for i in range(self.__neighbor):
            stocks = pd.merge(stocks, industry_rolling, left_on=['time', f'nlargest_{i}'], right_on=[
                'time', 'sw1'], suffixes=['', f'_nlargest_{i}'], how='left')
            stocks.drop(columns=[f'sw1_nlargest_{i}'], inplace=True)
            
        stocks = stocks.set_index('time')
        
        stocks['alpha'] = stocks.groupby(
            'code').adj_close.apply(self.__compute_return)
        
        for i in range(self.__neighbor):
            stocks['alpha'] = stocks['alpha'] - \
                stocks[f'ret_1d_nlargest_{i}'] / self.__neighbor
        
        stocks = stocks[['code', 'alpha', 'adj_close']]
        stocks['alpha'] = -stocks['alpha']
        return stocks

    def __compute_future_return(self, x):
        '''Delay 1: return from T+0 to T+1'''
        return np.log(x.shift(-1)) - np.log(x)

    def compute(self):
        logger().debug("Loading Cumulative Adjust Factor...")
        cum_adjf = dataloader.loading(
            'Cum Adj Factor', start=self.__start, end=self.__end, fields=['code', 'cum_adjf'])
        logger().debug("Loading Cumulative Adjust Factor...Done!")

        logger().debug("Loading Universe...")
        population = dataloader.loading(
            "Universe", start=self.__start, end=self.__end, fields=self.__universe)
        logger().debug("Loading Universe...Done!")

        # TODO: loading from a rolling window
        logger().debug("Loading Stock PV...")
        # currently we are using close price to compute return
        # TODO: using different point in time to compute return
        stocks = dataloader.loading(
            tab_name="PV Basics", start=self.__start, end=self.__end, fields=['code', 'close', 'total_volume'])
        logger().debug("Loading Stock PV...Done!")

        # merge PV data with adj factor
        stocks = stocks.reset_index().merge(cum_adjf.reset_index(),
                                            on=['time', 'code'], how='left').set_index('time')

        # adj close
        stocks['adj_close'] = stocks['close'] * stocks['cum_adjf']

        stocks = self.__compute_corr_price(stocks)
        stocks['fut_ret_1d'] = stocks.groupby(
            'code').adj_close.apply(self.__compute_future_return)

        # select stocks in the universe
        stocks = stocks.reset_index().merge(population.reset_index(),
                                            on=['time', 'code'], how='inner').set_index('time')

        # purging the first windows date
        dates = [d.strftime("%Y%m%d") for d in stocks.index.unique()]
        dates.sort()
        dates = dates[(self.__window):]

        self.__save(stocks, dates)

    def __save(self, df, dates):
        tableName = f"{self.__name}-{self.__window}days-{self.__neighbor}neighbors-{self.__universe}"
        tableDir = myPath.ALPHA_DIR/tableName
        tableDir.mkdir(parents=True, exist_ok=True)

        logger().debug(f"Start writing to files for alpha {tableName}...")

        for date in dates:
            outputfile = myPath.ALPHA_DIR/tableName/(date+'.csv')
            if outputfile.exists() and not self.__refresh:
                return
            try:
                df1d = df.loc[df.index == date].reset_index()
                df1d.time = df1d.time.dt.strftime("%Y%m%d")
                df1d = df1d[['time', 'code', 'name', 'alpha', 'fut_ret_1d']]
                df1d.to_csv(outputfile, index=False)
                # logger().info(f"Writing to file on date {date} for alpha {tab}...Done!")
            except:
                logger().error(
                    f"Exception when Writing to file on date {date} for alpha {tableName}")

        logger().debug("Writing to files...Done!")
