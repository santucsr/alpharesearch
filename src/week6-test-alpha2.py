from alphacalc import alpha_calc
from alpha_perfmc import perfmc

import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    # plots and daily pnl results will be saved in the plot folder
    cfg_list = []
    for short in [3, 5, 10]:  # [3, 5, 10, 20, 60]:
        for long in [10, 20, 60]:
            cfg_list.append(('YaoVol013', {'start_date': '20180101',
                                        'end_date': '20201231',
                                           'maxWindow': short,
                                           'meanWindow': long,
                                        'universe': 'zz9999',
                                        'refresh': True}))

    alpha_calc.calc(cfg_list)

    args_dict_list = []
    for short in [3, 5, 10]:  # [3, 5, 10, 20, 60]:
        for long in [10, 20, 60]:
            for holdings in [1, 3, 5, 10, 20, 60]:
                args_dict_list.append({
                    'table_name': f'alpha.YaoVol013-{short}days-{long}days-zz9999',
                    # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
                    'start_date': '20180101',
                    'end_date': '20201231',
                    'transform': 'Rank',
                    'neutralize': 'Industry',
                    'holding': holdings
                })
    perfmc.calc(args_dict_list)
#
