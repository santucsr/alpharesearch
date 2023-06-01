# Reversion 015: consistent sell volume
# mean(consisten_volume / volume, N); consistent_volume = if(|close - open| <= a|high - low| & close - open < 0, min_volume, else 0)
# the larger the alpha, the more inconsistent volumes would be included
# the larger the alpha, the more volumes would lie in |close - open| / |high - low| <= a, i.e., the price is more diverged, this could indicate a reversion? or momentum?

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
warnings.filterwarnings('ignore')

logger = myLogger.Logger(__name__)
logger.init(console_handler=True)


class YaoReV015():
    def __init__(self, args_dict):
        self.__name = 'YaoReV015'
        self.__universe = args_dict['universe']
        self.__start = args_dict['start_date']
        self.__end = args_dict['end_date']
        self.__window = args_dict['window']
        self.__a = args_dict['a']
        # self.__delay = args_dict['delay'] # Delay 0? Delay 1?
        self.__refresh = True if 'refresh' not in args_dict else args_dict['refresh']

    def __compute_consistency(self, x):
        '''function to compute selling consistency'''
        # should flip sign here?
        return (x[f'consistent_sell_{self.__a}'] / x['total_volume']).rolling(self.__window, min_periods=self.__window, closed='left').mean()

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

        logger().debug("Loading consistent sell...")
        consistent_volumes = dataloader.loading(
            tab_name="Consistent Buy Sell", start=self.__start, end=self.__end, fields=['code', 'consistent_sell_0.1', 'consistent_sell_0.2', 'consistent_sell_0.3', 'consistent_sell_0.4', 'consistent_sell_0.5', 'consistent_sell_0.6', 'consistent_sell_0.7', 'consistent_sell_0.8', 'consistent_sell_0.9'])
        logger().debug("Loading consistent sell...Done!")

        # merge PV data with adj factor
        stocks = stocks.reset_index().merge(cum_adjf.reset_index(),
                                            on=['time', 'code'], how='left').set_index('time')
        # merge PV data with consistent volumes
        stocks = stocks.reset_index().merge(consistent_volumes.reset_index(),
                                            on=['time', 'code'], how='left').set_index('time')

        # adj close
        stocks['adj_close'] = stocks['close'] * stocks['cum_adjf']

        stocks['fut_ret_1d'] = stocks.groupby(
            'code').adj_close.apply(self.__compute_future_return)

        alpha = stocks.groupby('code').apply(
            self.__compute_consistency).reset_index().rename(columns={0: 'alpha'})
        stocks = stocks.reset_index().merge(
            alpha, on=['time', 'code'], how='left').set_index('time')

        # select stocks in the universe
        stocks = stocks.reset_index().merge(population.reset_index(),
                                            on=['time', 'code'], how='inner').set_index('time')

        # purging the first windows date
        dates = [d.strftime("%Y%m%d") for d in stocks.index.unique()]
        dates.sort()
        dates = dates[(self.__window-1):]

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
