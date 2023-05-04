# Reversion 012: residual return on return std 
# we run a cross section regression on return against intraday std, then we construct N-day residual return

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
warnings.filterwarnings('ignore')

logger = myLogger.Logger(__name__)
logger.init(console_handler=True)


class YaoReV012():
    def __init__(self, args_dict):
        self.__name = 'YaoReV012'
        self.__universe = args_dict['universe']
        self.__start = args_dict['start_date']
        self.__end = args_dict['end_date']
        self.__window = args_dict['window']
        # self.__delay = args_dict['delay'] # Delay 0? Delay 1?
        self.__refresh = True if 'refresh' not in args_dict else args_dict['refresh']

    def __compute_std(self, x):
        '''function to compute intraday std'''
        # closed='left' to avoid look ahead bias
        return x['close_std'].rolling(self.__window, min_periods=self.__window, closed='left').mean()

    def __compute_future_return(self, x):
        '''Delay 1: return from T+0 to T+1'''
        return np.log(x.shift(-1)) - np.log(x)

    def __prepare_model(self, stocks):
        intraday_std = dataloader.loading(
            tab_name="PV Basics", start=self.__start, end=self.__end, fields=['code', 'close_std'])

        # merge PV data with intraday stds
        stocks = stocks.reset_index().merge(intraday_std.reset_index(),
                                            on=['time', 'code'], how='left').set_index('time')
        stocks['ret_1d'] = stocks.groupby(
            'code').adj_close.apply(lambda x: np.log(x.shift(1)) - np.log(x.shift(2)))

        ret_std = stocks.groupby('code').apply(
            self.__compute_std).reset_index().rename(columns={'close_std': 'ret_std'})
        stocks = stocks.reset_index().merge(
            ret_std, on=['time', 'code'], how='left').set_index('time')

        return stocks

    def __regress(self, x):
        x.dropna(subset=['ret_1d', 'ret_std'], inplace=True)
        endog = x.ret_1d
        exog = sm.add_constant(x[['ret_std']])
        try:
            model = sm.OLS(endog, exog)
            res = model.fit()
            # x['resid'] = res.resid
            return pd.concat([x.code, res.resid], axis=1)
        except:
            resid = endog.copy()
            resid[:] = np.nan
            return pd.concat([x.code, resid], axis=1)

    def __compute_residuals(self, stocks):
        residuals = stocks.reset_index().groupby('time').apply(
            lambda x: self.__regress(x))
        residuals = residuals.reset_index()[['time', 'code', 0]]
        residuals.rename(columns={0: 'resid'}, inplace=True)
        stocks = stocks.reset_index().merge(
            residuals, on=['time', 'code'], how='left').set_index('time')
        return stocks

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

        stocks = self.__prepare_model(stocks)
        stocks = self.__compute_residuals(stocks)

        alpha = stocks.groupby('code').resid.rolling(
            self.__window).sum().reset_index().rename(columns={'resid': 'alpha'})
        alpha['alpha'] = -alpha['alpha']

        stocks = stocks.reset_index().merge(
            alpha, on=['time', 'code'], how='left').set_index('time')

        # select stocks in the universe
        stocks = stocks.reset_index().merge(population.reset_index(),
                                            on=['time', 'code'], how='inner').set_index('time')

        # purging the first windows date
        dates = [d.strftime("%Y%m%d") for d in stocks.index.unique()]
        dates.sort()
        dates = dates[(self.__window*2-2):]

        self.__save(stocks, dates)

    def __save(self, df, dates):
        tableName = f"{self.__name}-{self.__window}days-{self.__universe}"
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
