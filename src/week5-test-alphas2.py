from alphacalc import alpha_calc
from alpha_perfmc import perfmc

import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    # plots and daily pnl results will be saved in the plot folder
    cfg_list = []
    for delay in [20]:
        for a in [0.5]:#, 2, 3, 5, 7, 10]:

            cfg_list.append(('YaoReV015', {'start_date': '20180101',
                                        'end_date': '20201231',
                                        'window': delay,
                                        'a': a,
                                        'universe': 'zz9999',
                                        'refresh': True}))

    alpha_calc.calc(cfg_list)
 
    args_dict_list = []
    for delay in [20]:#, 5, 10, 20, 60, 120]:
        for a in [0.5]:
            for holdings in [1, 3, 5, 10, 20, 60]:
                args_dict_list.append({
                    'table_name': f'alpha.YaoReV015-{delay}days-a{int(a*10)}-zz9999',
                    # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
                    'start_date': '20180101',
                    'end_date': '20201231',
                    'transform': 'Rank',
                    'neutralize': 'Industry',
                    'holding': holdings
                })
    perfmc.calc(args_dict_list)
#