# Momentum 001: N day return.
# We define the N day return at T0 to be return from T-(N+1) to T-1, following delay 1 scheme

# 
from datetime import datetime
from functools import partial
import logging
from multiprocessing import Pool
import warnings
warnings.filterwarnings('ignore')

#
from collections import defaultdict
import numpy as np
import pandas as pd

# Local Library imports
from utils.calendar import CALENDAR, START, END
from pathmgmt import pathmgmt as myPath
from loader import dataloader
from logger import logger as myLogger

logger = myLogger.Logger(__name__)
logger.init(console_handler=True)

class YaoMoM001():
    # this way cannot handle multiprocessing?
    # cur_adjf = pd.DataFrame()
    # population = defaultdict(pd.Dataframe)
    
    # better create a global variable for all common data?
    
    def __init__(self, args_dict):
        self.__name = 'YaoMoM001'
        self.__universe = args_dict['universe']
        self.__start = args_dict['start_date']
        self.__end = args_dict['end_date']
        self.__window = args_dict['window']
        # self.__delay = args_dict['delay'] # Delay 0? Delay 1?
        self.__refresh = True if 'refresh' not in args_dict else args_dict['refresh']
        
    def __compute_return(self, x):
        '''function to compute lag return'''
        return np.log(x.shift(1)) - np.log(x.shift(1 + self.__window))

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
            tab_name="PV Basics", start=self.__start, end=self.__end, fields=['code', 'close'])
        logger().debug("Loading Stock PV...Done!")

        # merge PV data with adj factor
        stocks = stocks.reset_index().merge(cum_adjf.reset_index(),
                                            on=['time', 'code'], how='left').set_index('time')

        # select stocks in the universe
        # select universe here can cause a problem: change of universe would exclude some stocks unintentionally
        # stocks = stocks.reset_index().merge(population.reset_index(),
        #                                     on=['time', 'code'], how='inner').set_index('time')
        
        # adj close
        stocks['adj_close'] = stocks['close'] * stocks['cum_adjf']

        stocks['alpha'] = stocks.groupby(
            'code').adj_close.apply(self.__compute_return)
        
        stocks['fut_ret_1d'] = stocks.groupby(
            'code').adj_close.apply(self.__compute_future_return)
        
        # select stocks in the universe
        stocks = stocks.reset_index().merge(population.reset_index(),
                                            on=['time', 'code'], how='inner').set_index('time')
        
        # purging the first windows date
        dates = [d.strftime("%Y%m%d") for d in stocks.index.unique()]
        dates.sort()
        dates = dates[(self.__window):]
        
        # ERROR: daemonic processes are not allowed to have children
        # with Pool() as pool:
        #     pool.map(partial(writeToFile, stocks, tableName, refresh),
        #              dates)
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