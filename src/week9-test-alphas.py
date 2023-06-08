from alphacalc import alpha_calc
from alpha_perfmc import perfmc

import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    # plots and daily pnl results will be saved in the plot folder
    cfg_list = []
    # for delay in [3, 5, 10, 60]:
    for delay in [20]:
        cfg_list.append(('YaoLqd024', {'start_date': '20180101',
                                        'end_date': '20201231',
                                        'window': delay,
                                        'universe': 'zz9999',
                                        'refresh': True}))

    # alpha_calc.calc(cfg_list)

    args_dict_list = []
    # for delay in [3, 5, 10, 60]:
    for delay in [20]:
        # for holdings in [1, 3, 5, 10, 20, 60]:
        for holdings in [20]:
            args_dict_list.append({
                'table_name': f'alpha.YaoLqd024-{delay}days-zz9999',
                # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
                'start_date': '20180101',
                'end_date': '20201231',
                'transform': 'None',
                'neutralize': 'Industry',
                'holding': holdings
            })
            # args_dict_list.append({
            #     'table_name': f'alpha.YaoLqd010-{delay}days-zz9999',
            #     # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
            #     'start_date': '20180101',
            #     'end_date': '20201231',
            #     'transform': 'Rank',
            #     'neutralize': 'Industry',
            #     'holding': holdings
            # })
    # perfmc.calc(args_dict_list)
# #


    cfg_list = []
    for k in range(24, 26):
        for delay in [3, 5, 10, 20, 60]:
            cfg_list.append((f'YaoLqd0{k}', {'start_date': '20180101',
                                        'end_date': '20201231',
                                        'window': delay,
                                        'universe': 'zz9999',
                                        'refresh': True}))

    # # alpha_calc.calc(cfg_list)
    # for delay in [3, 5, 10, 20, 60]:
    #     cfg_list.append(('YaoLqd002', {'start_date': '20180101',
    #                                    'end_date': '20201231',
    #                                    'window': delay,
    #                                    'universe': 'zz9999',
    #                                    'refresh': True}))

    # for delay in [3, 5, 10, 20, 60]:
    #     cfg_list.append(('YaoLqd003', {'start_date': '20180101',
    #                                    'end_date': '20201231',
    #                                    'window': delay,
    #                                    'universe': 'zz9999',
    #                                    'refresh': True}))

    # for delay in [3, 5, 10, 20, 60]:
    #     cfg_list.append(('YaoLqd004', {'start_date': '20180101',
    #                                    'end_date': '20201231',
    #                                    'window': delay,
    #                                    'universe': 'zz9999',
    #                                    'refresh': True}))
        
    # for delay in [3, 5, 10, 20, 60]:
    #     cfg_list.append(('YaoLqd008', {'start_date': '20180101',
    #                                    'end_date': '20201231',
    #                                    'window': delay,
    #                                    'universe': 'zz9999',
    #                                    'refresh': True}))

    # for delay in [3, 5, 10, 20, 60]:
    # # for delay in [20]:
    #     for a in [0.1, 0.3, 0.5, 0.7, 0.9]:
    #         cfg_list.append(('YaoLqd007', {'start_date': '20180101',
    #                                     'end_date': '20201231',
    #                                     'window': delay,
    #                                     'a': a,
    #                                     'universe': 'zz9999',
    #                                     'refresh': True}))
            
    # for delay in [3, 5, 10, 20, 60]:
    #             # for delay in [20]:
    #     for a in [0.1, 0.3, 0.5, 0.7, 0.9]:
    #         cfg_list.append(('YaoLqd006', {'start_date': '20180101',
    #                                        'end_date': '20201231',
    #                                        'window': delay,
    #                                        'a': a,
    #                                        'universe': 'zz9999',
    #                                        'refresh': True}))

    alpha_calc.calc(cfg_list)

    args_dict_list = []
    for k in range(24, 26):
        for delay in [3, 5, 10, 20, 60]:
        # for delay in [20]:
            for holdings in [1, 3, 5, 10, 20, 60]:
            # for holdings in [20]:
                args_dict_list.append({
                    'table_name': f'alpha.YaoLqd0{k}-{delay}days-zz9999',
                    # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
                    'start_date': '20180101',
                    'end_date': '20201231',
                    'transform': 'None',
                    'neutralize': 'Industry',
                    'holding': holdings
                })
                # args_dict_list.append({
                #     'table_name': f'alpha.YaoLqd0{k}-{delay}days-zz9999',
                #     # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
                #     'start_date': '20180101',
                #     'end_date': '20201231',
                #     'transform': 'Rank',
                #     'neutralize': 'Industry',
                #     'holding': holdings
                # })
            # args_dict_list.append({
            #     'table_name': f'alpha.YaoLqd002-{delay}days-zz9999',
            #     # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
            #     'start_date': '20180101',
            #     'end_date': '20201231',
            #     'transform': 'None',
            #     'neutralize': 'Industry',
            #     'holding': holdings
            # })
            # args_dict_list.append({
            #     'table_name': f'alpha.YaoLqd002-{delay}days-zz9999',
            #     # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
            #     'start_date': '20180101',
            #     'end_date': '20201231',
            #     'transform': 'Rank',
            #     'neutralize': 'Industry',
            #     'holding': holdings
            # })
            # args_dict_list.append({
            #     'table_name': f'alpha.YaoLqd003-{delay}days-zz9999',
            #     # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
            #     'start_date': '20180101',
            #     'end_date': '20201231',
            #     'transform': 'None',
            #     'neutralize': 'Industry',
            #     'holding': holdings
            # })
            # args_dict_list.append({
            #     'table_name': f'alpha.YaoLqd003-{delay}days-zz9999',
            #     # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
            #     'start_date': '20180101',
            #     'end_date': '20201231',
            #     'transform': 'Rank',
            #     'neutralize': 'Industry',
            #     'holding': holdings
            # })
            # args_dict_list.append({
            #     'table_name': f'alpha.YaoLqd004-{delay}days-zz9999',
            #     # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
            #     'start_date': '20180101',
            #     'end_date': '20201231',
            #     'transform': 'None',
            #     'neutralize': 'Industry',
            #     'holding': holdings
            # })
            # args_dict_list.append({
            #     'table_name': f'alpha.YaoLqd004-{delay}days-zz9999',
            #     # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
            #     'start_date': '20180101',
            #     'end_date': '20201231',
            #     'transform': 'Rank',
            #     'neutralize': 'Industry',
            #     'holding': holdings
            # })
            # args_dict_list.append({
            #     'table_name': f'alpha.YaoLqd008-{delay}days-zz9999',
            #     # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
            #     'start_date': '20180101',
            #     'end_date': '20201231',
            #     'transform': 'None',
            #     'neutralize': 'Industry',
            #     'holding': holdings
            # })
            # args_dict_list.append({
            #     'table_name': f'alpha.YaoLqd008-{delay}days-zz9999',
            #     # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
            #     'start_date': '20180101',
            #     'end_date': '20201231',
            #     'transform': 'Rank',
            #     'neutralize': 'Industry',
            #     'holding': holdings
            # })

            
    perfmc.calc(args_dict_list)
    
    args_dict_list = []
    for delay in [3, 5, 10, 20, 60]:
    # for delay in [20]:
        for holdings in [1, 3, 5, 10, 20, 60]:
            # for holdings in [1]:
            for a in [0.1, 0.3, 0.5, 0.7, 0.9]:
                # args_dict_list.append({
                #     'table_name': f'alpha.YaoLqd007-{delay}days-a0{int(a*10)}-zz9999',
                #     # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
                #     'start_date': '20180101',
                #     'end_date': '20201231',
                #     'transform': 'None',
                #     'neutralize': 'Industry',
                #     'holding': holdings
                # })
                # args_dict_list.append({
                #     'table_name': f'alpha.YaoLqd007-{delay}days-a0{int(a*10)}-zz9999',
                #     # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
                #     'start_date': '20180101',
                #     'end_date': '20201231',
                #     'transform': 'Rank',
                #     'neutralize': 'Industry',
                #     'holding': holdings
                # })
                # args_dict_list.append({
                #     'table_name': f'alpha.YaoLqd006-{delay}days-a0{int(a*10)}-zz9999',
                #     # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
                #     'start_date': '20180101',
                #     'end_date': '20201231',
                #     'transform': 'None',
                #     'neutralize': 'Industry',
                #     'holding': holdings
                # })
                args_dict_list.append({
                    'table_name': f'alpha.YaoLqd006-{delay}days-a0{int(a*10)}-zz9999',
                    # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
                    'start_date': '20180101',
                    'end_date': '20201231',
                    'transform': 'Rank',
                    'neutralize': 'Industry',
                    'holding': holdings
                })
                
    # perfmc.calc(args_dict_list)
