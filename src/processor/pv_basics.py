# Standard
import numpy as np

def process1min(data):
    '''write a function to iterate all names in one date folder
    Main functionality to generate features
    '''
    column_names = ['code', 'open', 'close', 'pre_close',
                    'low', 'high', 'open_std',
                    'close_std', 'total_volume', 'total_turnover', 'volume_std', 'turnover_std']
    # TODO: sprecial handling for 0 value??
    open = data.iloc[0].open
    close = data.iloc[-1].close
    pre_close = data.iloc[0].pre_close
    low = data.low.min()
    high = data.high.max()
    # 1 min return volatility
    open_std = data.open.pct_change().replace([np.inf, -np.inf], np.nan).dropna().std()
    close_std = data.close.pct_change().replace([np.inf, -np.inf], np.nan).dropna().std()
    total_volume = data.iloc[-1].accvolume
    total_turnover = data.iloc[-1].accturover
    volume_std = data.volume.std()
    turnover_std = data.turover.std()  # typo here?
    return [data.iloc[0].code, open, close, pre_close, low, high, open_std, close_std, total_volume, total_turnover, volume_std, turnover_std], column_names

def processConsistentVolume(data):
    '''Function to generate the consistent volume feature'''
    a = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    columns = ['code'] + [f'consistent_volume_{i}' for i in a]
    consistent_volumes = []
    for i in a:
        consistent_volumes.append((data.volume * ((data.open - data.close).abs()
                                                < (data.high - data.low).abs() * i) * (data.time <= 1457)).sum())
    return [data.iloc[0].code] + consistent_volumes, columns

def processConsistentBuySell(data):
    '''Function to generate the consistent volume feature'''
    a = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    columns = ['code'] + [f'consistent_buy_{i}' for i in a] + [f'consistent_sell_{i}' for i in a]
    consistent_volumes = []
    for i in a:
        consistent_volumes.append((data.volume * ((data.open - data.close).abs()
                                                  < (data.high - data.low).abs() * i) * (data.time <= 1457) * (data.close > data.open)).sum())
    for i in a:
        consistent_volumes.append((data.volume * ((data.open - data.close).abs()
                                                  < (data.high - data.low).abs() * i) * (data.time <= 1457) * (data.close < data.open)).sum())
    return [data.iloc[0].code] + consistent_volumes, columns

def processBuySellVolume(data):
    pass

def processBuySellTurnover(data):
    columns = ['code'] + ['buy_turnover'] + ['sell_turnover']
    turnovers = []
    turnovers.append((data.turover * (data.time <= 1457) * (data.close > data.open)).sum())
    turnovers.append((data.turover * (data.time <= 1457) * (data.close < data.open)).sum())
    return [data.iloc[0].code] + turnovers, columns

def processConsistentBuySellTurnover(data):
    '''Function to generate the consistent turnover feature'''
    a = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    columns = ['code'] + [f'consistent_buy_trv_{i}' for i in a] + [f'consistent_sell_trv_{i}' for i in a]
    consistent_turnover = []
    for i in a:
        consistent_turnover.append((data.turover * ((data.open - data.close).abs()
                                                  < (data.high - data.low).abs() * i) * (data.time <= 1457) * (data.close > data.open)).sum())
    for i in a:
        consistent_turnover.append((data.turover * ((data.open - data.close).abs()
                                                  < (data.high - data.low).abs() * i) * (data.time <= 1457) * (data.close < data.open)).sum())
    return [data.iloc[0].code] + consistent_turnover, columns

def processConsistentTurnover(data):
    '''Function to generate the consistent volume feature'''
    a = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    columns = ['code'] + [f'consistent_turnover_{i}' for i in a]
    consistent_turnover = []
    for i in a:
        consistent_turnover.append((data.turover * ((data.open - data.close).abs()
                                                  < (data.high - data.low).abs() * i) * (data.time <= 1457)).sum())
    return [data.iloc[0].code] + consistent_turnover, columns

def processintradayTurnover(data):
    am_open = data.iloc[0].turover # 09:30
    pm_close = data.loc[data.time >= 1457].turover.sum() # close auction
    
    am_close = data.loc[data.time == 1129].turover.sum() # 11:29
    pm_open = data.loc[data.time == 1300].turover.sum() # 13:00
    
    am_open_5min = data.loc[(data.time >= 931) & (data.time <= 935)].turover.sum() # excluding first minute, 09:31 - 09:35
    am_close_5min = data.loc[(data.time >= 1125) & (data.time <= 1129)].turover.sum() # 11:25 - 11:29
    pm_open_5min = data.loc[(data.time >= 1300) & (data.time <= 1304)].turover.sum() # 13:00 - 13:04
    pm_close_5min = data.loc[(data.time >= 1452) & (data.time <= 1456)].turover.sum() # excluding close auction, 09:31 - 09:35

    high = data.turover.max()
    low = min(data.loc[data.time < 1457].turover.min(), pm_close)

    am_high = data.loc[data.time < 1300].turover.max()
    am_low = data.loc[data.time < 1300].turover.min()
    
    pm_high = max(data.loc[(data.time < 1457) & (data.time >= 1300)].turover.max(), pm_close)
    pm_low = min(data.loc[(data.time < 1457) & (data.time >= 1300)].turover.min(), pm_close)
    
    columns = ['code', 'am_open_trv', 'pm_close_trv', 'am_close_trv', 'pm_open_trv',
               'am_open_5min_trv', 'am_close_5min_trv', 'pm_open_5min_trv', 'pm_close_5min_trv',
               'high_trv', 'low_trv', 'am_high_trv', 'am_low_trv', 'pm_high_trv', 'pm_low_trv']

    return [data.iloc[0].code] + [am_open, pm_close, am_close, pm_open, am_open_5min, am_close_5min, pm_open_5min, pm_close_5min, high, low, am_high, am_low, pm_high, pm_low], columns


def processIlliquidity(data):
    illiquidity1_hl_mean = ((data.high - data.low) / data.turover).replace([np.inf, -np.inf], 0).mean()
    illiquidity1_hl_std = ((data.high - data.low) / data.turover).replace([np.inf, -np.inf], 0).std()
    illiquidity1_hl_range = ((data.high - data.low) / data.turover).replace([np.inf, -np.inf], 0).max() - ((data.high - data.low) / data.turover).replace([np.inf, -np.inf], 0).min()
    
    illiquidity1_ho_mean = ((data.high - data.open) / data.turover).replace([np.inf, -np.inf], 0).mean()
    illiquidity1_ho_std = ((data.high - data.open) / data.turover).replace([np.inf, -np.inf], 0).std()
    illiquidity1_ho_range = ((data.high - data.open) / data.turover).replace([np.inf, -np.inf], 0).max() - ((data.high - data.open) / data.turover).replace([np.inf, -np.inf], 0).min()
    
    illiquidity1_co_mean = ((data.close - data.open) / data.turover).replace([np.inf, -np.inf], 0).mean()
    illiquidity1_co_std = ((data.close - data.open) / data.turover).replace([np.inf, -np.inf], 0).std()
    illiquidity1_co_range = ((data.close - data.open) / data.turover).replace([np.inf, -np.inf], 0).max() - ((data.close - data.open) / data.turover).replace([np.inf, -np.inf], 0).min()
    
    columns = ['code', 'illiquidity1_hl_mean', 'illiquidity1_hl_std', 'illiquidity1_hl_range', 'illiquidity1_ho_mean',
               'illiquidity1_ho_std', 'illiquidity1_ho_range', 'illiquidity1_co_mean', 'illiquidity1_co_std', 'illiquidity1_co_range']

    return [data.iloc[0].code] + [illiquidity1_hl_mean, illiquidity1_hl_std, illiquidity1_hl_range, illiquidity1_ho_mean, illiquidity1_ho_std, illiquidity1_ho_range, illiquidity1_co_mean, illiquidity1_co_std, illiquidity1_co_range], columns
