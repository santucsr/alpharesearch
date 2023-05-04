# Reversion 011: residual return reversion wiht market, smb and consistent volume
# r* = r - beta1*r_m - beta2*r_smb - beta3*r_cv - const
# here we define smb as zz1000 - zz800, see Reversion 009 for consistent volume definition
# this is a three factor model

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


class YaoReV011():
    def __init__(self, args_dict):
        self.__name = 'YaoReV011'
        self.__universe = args_dict['universe']
        self.__start = args_dict['start_date']
        self.__end = args_dict['end_date']
        self.__window = args_dict['window']
        self.__a = args_dict['a']
        # self.__delay = args_dict['delay'] # Delay 0? Delay 1?
        self.__refresh = True if 'refresh' not in args_dict else args_dict['refresh']

    def __compute_rolling_capm(self, x):
        endog = x.ret_1d
        exog = sm.add_constant(x[['mkt_ret_1d', 'smb_ret_1d', 'consistency']])

        try:
            rols = RollingOLS(endog, exog, window=60,
                              min_nobs=self.__window, expanding=True)
            rres = rols.fit()
            rolling_resid = endog - (rres.params * exog).sum(1, skipna=False)
            return -rolling_resid.rolling(self.__window).sum()
        except:
            rolling_resid = endog.copy()
            rolling_resid[:] = np.nan
            return pd.Series(rolling_resid.values, index=rolling_resid.index)

    def __prepare_for_factor_model(self, stocks):
        market = dataloader.loading(
            tab_name="Index", start=self.__start, end=self.__end, fields=['code', 'name', 'close'])
        big = market.loc[market.name == '中证800']
        small = market.loc[market.name == '中证1000']
        market = market.loc[market.name == '沪深300']
        
        market['mkt_ret_1d'] = np.log(
            market.close.shift(1)) - np.log(market.close.shift(2))
        small['small_ret_1d'] = np.log(
            small.close.shift(1)) - np.log(small.close.shift(2))
        big['big_ret_1d'] = np.log(
            big.close.shift(1)) - np.log(big.close.shift(2))
        
        stocks['ret_1d'] = stocks.groupby(
            'code').adj_close.apply(lambda x: np.log(x.shift(1)) - np.log(x.shift(2)))
        stocks = stocks.reset_index().merge(market['mkt_ret_1d'].reset_index(),
                                            on=['time'], how='left').set_index('time')
        stocks = stocks.reset_index().merge(small['small_ret_1d'].reset_index(),
                                    on=['time'], how='left').set_index('time')
        stocks = stocks.reset_index().merge(big['big_ret_1d'].reset_index(),
                                            on=['time'], how='left').set_index('time')
        stocks['smb_ret_1d'] = stocks['small_ret_1d'] - stocks['big_ret_1d']
        return stocks

    def __compute_future_return(self, x):
        '''Delay 1: return from T+0 to T+1'''
        return np.log(x.shift(-1)) - np.log(x)
    
    def __prepare_consistency(self, stocks):
        logger().debug("Loading consistent volumes...")
        consistent_volumes = dataloader.loading(
            tab_name="Consistent Volume", start=self.__start, end=self.__end, fields=['code', 'consistent_volume_0.1', 'consistent_volume_0.2', 'consistent_volume_0.3', 'consistent_volume_0.4', 'consistent_volume_0.5', 'consistent_volume_0.6', 'consistent_volume_0.7', 'consistent_volume_0.8', 'consistent_volume_0.9'])
        logger().debug("Loading consistent volumes...Done!")

        # merge PV data with consistent volumes
        stocks = stocks.reset_index().merge(consistent_volumes.reset_index(),
                                            on=['time', 'code'], how='left').set_index('time')

        consistency = stocks.groupby('code').apply(
            self.__compute_consistency).reset_index().rename(columns={0: 'consistency'})
        stocks = stocks.reset_index().merge(
            consistency, on=['time', 'code'], how='left').set_index('time')

        return stocks
    
    def __compute_consistency(self, x):
        '''function to compute trading consistency'''
        # closed='left' to avoid look ahead bias
        # return (x[f'consistent_volume_{self.__a}'] / x['total_volume']).rolling(self.__window, min_periods=self.__window, closed='left').mean()
        return (x[f'consistent_volume_{self.__a}'] / x['total_volume']).rolling(1, closed='left').mean()

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
        
        stocks['fut_ret_1d'] = stocks.groupby(
            'code').adj_close.apply(self.__compute_future_return)

        stocks = self.__prepare_consistency(stocks)
        stocks = self.__prepare_for_factor_model(stocks)
        alpha = stocks.groupby('code').apply(
            self.__compute_rolling_capm).reset_index().rename(columns={0: 'alpha'})
        stocks = stocks.reset_index().merge(
            alpha, on=['time', 'code'], how='left').set_index('time')

        # select stocks in the universe
        stocks = stocks.reset_index().merge(population.reset_index(),
                                            on=['time', 'code'], how='inner').set_index('time')

        # purging the first windows date
        dates = [d.strftime("%Y%m%d") for d in stocks.index.unique()]
        dates.sort()
        dates = dates[(self.__window*2-1):]

        self.__save(stocks, dates)

    def __save(self, df, dates):
        tableName = f"{self.__name}-{self.__window}days-a{int(self.__a*10)}-{self.__universe}"
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
