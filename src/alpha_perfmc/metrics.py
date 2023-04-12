import matplotlib.pyplot as plt
plt.style.use('ggplot')

import numpy as np
import pandas as pd

from loader import dataloader
from pathmgmt import pathmgmt as myPath

INDEX_MAPPING = {'hs300': '沪深300',
                 'zz500': '中证500',
                 'zz800': '中证800',
                 'zz1000': '中证1000', }

def compute_matrics(positions, tab_name, start, end, universe, transform, neutralize):
    daily_pnl = positions.reset_index().groupby('time').pnl.sum().to_frame()

    # load benchmark price
    if universe in INDEX_MAPPING:
        universe = INDEX_MAPPING[universe]
    benchmark = dataloader.loading(
        tab_name="Index", start=start, end=end, fields=['code', 'name', 'close'])
    
    # compute benchmark daily return 
    daily_pnl['benchmark_ret'] = benchmark.loc[benchmark.name == universe].close.transform(
        lambda x: np.log(x.shift(-1)) - np.log(x))
    
    # cumulative pnl
    daily_pnl['cum_pnl'] = daily_pnl['pnl'].cumsum()
    daily_pnl['cum_benchmark_ret'] = daily_pnl['benchmark_ret'].cumsum()
    
    # excess return 
    daily_pnl['excess_ret'] = daily_pnl['pnl'] - daily_pnl['benchmark_ret']
    daily_pnl['cum_excess_ret'] = daily_pnl['cum_pnl'] - daily_pnl['cum_benchmark_ret']
    
    # annualized return 
    annual_ret = daily_pnl.pnl.mean() * 252
    # annualized excess return
    annual_excess_ret = daily_pnl.excess_ret.mean() * 252
    # information ratio
    ir1 = daily_pnl.excess_ret.mean() / daily_pnl.excess_ret.std() * np.sqrt(252)
    # raw information raio, not compared to benchmark
    ir2 = daily_pnl.pnl.mean() / daily_pnl.pnl.std() * np.sqrt(252)
    # information coefficient
    # position weights vs 1d return 
    ic = positions.reset_index().groupby('time')[[f'fut_ret_1d', 'weights']].corr().iloc[0::2, -1].mean()
    # max drawdown
    max_drawdown = -(daily_pnl.cum_pnl - daily_pnl.cum_pnl.cummax()).min()
    max_drawdown_excess = -(daily_pnl.cum_excess_ret - daily_pnl.cum_excess_ret.cummax()).min()
    # total turnover
    positions['turnover'] = positions.groupby('code').weights.diff().abs() / 2
    turnover = positions.reset_index().groupby('time').turnover.sum().mean() 
    daily_pnl['turnover'] = positions.reset_index().groupby('time').turnover.sum()
    
    statistics = {'Annualized Return': annual_ret, 
                  'Annualized Excess Return': annual_excess_ret, 
                  'IR': ir1, 
                  'raw IR': ir2,
                  'IC': ic, 
                  'Max Drawdown': max_drawdown,
                  'Max Drawdown (excess)': max_drawdown_excess,
                  'Total Turnover': turnover}
    
    # plot the performance metrics
    plot(tab_name, daily_pnl, statistics, start, end, transform, neutralize)
    
    # return daily_pnl, statistics
    
def plot(tab_name, daily_pnl, statistics, start, end, transform, neutralize):
    # pnl plot
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    fig.autofmt_xdate(rotation=45)
    ax.plot(daily_pnl[['cum_pnl', 'cum_benchmark_ret', 'cum_excess_ret']], label=[
            'cumulative return', 'benchmark return', 'cumulative excess return'])
    ax.legend()
    ax.set_title(f'PnL for {tab_name} from {start} to {end}')
    plt.figtext(.95, .49, pd.DataFrame(
        data=["{:.3%}".format(v) if k not in ['IR', 'raw IR'] else "{:.3}".format(v)
            for k, v in statistics.items()],
        index=statistics.keys())[0].to_string(),
        {'multialignment': 'right', 'fontsize': 12})
    (myPath.PLOT_DIR/tab_name).mkdir(parents=True, exist_ok=True)
    plt.savefig(myPath.PLOT_DIR/tab_name/f'{start}-{end}-{transform}-{neutralize}-PnL.png', bbox_inches='tight')
    # turnover plot
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    fig.autofmt_xdate(rotation=45)
    ax.plot(daily_pnl['turnover'], label='daily turnover')
    ax.legend()
    ax.set_title(f'Daily Turnover for {tab_name} from {start} to {end}')
    (myPath.PLOT_DIR/tab_name).mkdir(parents=True, exist_ok=True)
    plt.savefig(myPath.PLOT_DIR/tab_name/
                f'{start}-{end}-{transform}-{neutralize}-Turnover.png', bbox_inches='tight')

    # save daily pnl
    daily_pnl.to_csv(myPath.PLOT_DIR/tab_name /
                     f'{start}-{end}-{transform}-{neutralize}-dailyPnL.csv')

def stratified_model():
    pass