# Volatility 013: mean(max(high/low-1, m)，N)
# N should generally be larger than m?

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

class YaoVol013():
    def __init__(self, args_dict):
        self.__name = 'YaoVol013'
        self.__universe = args_dict['universe']
        self.__start = args_dict['start_date']
        self.__end = args_dict['end_date']
        self.__maxWindow = args_dict['maxWindow']
        self.__meanWindow = args_dict['meanWindow']
        # self.__delay = args_dict['delay'] # Delay 0? Delay 1?
        self.__refresh = True if 'refresh' not in args_dict else args_dict['refresh']
        
    def __compute_max_range(self, x):
        range = x.rolling(self.__maxWindow, closed='left').max()#.rolling(self.__meanWindow, closed='left').mean()
        return pd.Series(range.rolling(self.__meanWindow, closed='left').mean())

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
            tab_name="PV Basics", start=self.__start, end=self.__end, fields=['code', 'close', 'high', 'low'])
        logger().debug("Loading Stock PV...Done!")

        # merge PV data with adj factor
        stocks = stocks.reset_index().merge(cum_adjf.reset_index(),
                                            on=['time', 'code'], how='left').set_index('time')

        # adj close
        stocks['adj_close'] = stocks['close'] * stocks['cum_adjf']
        
        stocks['high_low_ratio'] = stocks['high'] / stocks['low']
        stocks['high_low_ratio'] = stocks['high_low_ratio'].replace([np.inf, -np.inf], np.nan)
        
        stocks['fut_ret_1d'] = stocks.groupby(
            'code').adj_close.apply(self.__compute_future_return)

        stocks['alpha'] = -stocks.groupby(
            'code').high_low_ratio.apply(self.__compute_max_range)

        # select stocks in the universe
        stocks = stocks.reset_index().merge(population.reset_index(),
                                            on=['time', 'code'], how='inner').set_index('time')

        # purging the first windows date
        dates = [d.strftime("%Y%m%d") for d in stocks.index.unique()]
        dates.sort()
        dates = dates[(self.__meanWindow):]

        self.__save(stocks, dates)

    def __save(self, df, dates):
        tableName = f"{self.__name}-{self.__maxWindow}days-{self.__meanWindow}days-{self.__universe}"
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
