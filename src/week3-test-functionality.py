from alphacalc import alpha_calc
from alpha_perfmc import perfmc

import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    # plots and daily pnl results will be saved in the plot folder    
    cfg_list = []
    for delay in [3, 5, 10, 20, 60, 120]:
    # for delay in [60]:
    # for long_term in [20, 60, 120]:
    #     for short_term in [3, 5, 10]:
    #         cfg_list.append(('YaoReV002', {'start_date': '20180101',
    #                                     'end_date': '20201231',
    #                                        'shortTerm': short_term,
    #                                         'longTerm': long_term,
    #                                     'universe': 'zz1000',
    #                                     'refresh': True}))
        cfg_list.append(('YaoReV005', {'start_date': '20180101',
                                    'end_date': '20201231',
                                        'window': delay,
                                    'universe': 'zz1000',
                                    'refresh': True}))
        # cfg_list.append(('YaoMoM007', {'start_date': '20180101',
        #                     'end_date': '20201231',
        #                         'window': delay,
        #                     'universe': 'zz1000',
        #                     'refresh': True}))
                # ('YaoReV002', {'start_date': '20180101',
                #                'end_date': '20201231',
                #                'shortTerm': 5,
                #                'longTerm': 60,
                #                'universe': 'zz1000',
                #                'refresh': True}),
                # ('YaoReV002', {'start_date': '20180101',
                #                'end_date': '20201231',
                #                'shortTerm': 3,
                #                'longTerm': 20,
                #                'universe': 'zz1000',
                #                'refresh': True}),
                # ('YaoReV002', {'start_date': '20180101',
                #                'end_date': '20201231',
                #                'shortTerm': 1,
                #                'longTerm': 20,
                #                'universe': 'zz1000',
                #                'refresh': True}),
                # ]
    # alpha_calc.calc(cfg_list)
    
    args_dict_list = []
    for delay in [3, 5, 10, 20, 60, 120]:
    # for long_term in [20, 60, 120]:
    #     for short_term in [3, 5, 10]:
    # # for delay in [60]:
        for holdings in [1, 3, 5, 10, 20, 60]:
    #             args_dict_list.append({
    #                 'table_name': f'alpha.YaoReV002-{short_term}days-{long_term}days-zz1000',
    #                 'start_date': '20180101',
    #                 'end_date': '20201231',
    #                 'transform': 'Rank',
    #                 'neutralize': 'Industry',
    #                 'holding': holdings
    #             })
            # args_dict_list.append({
            #     'table_name': f'alpha.YaoMoM003-{delay}days-zz1000',
            #     'start_date': '20180101',
            #     'end_date': '20201231',
            #     'transform': 'Rank',
            #     'neutralize': 'Industry',
            #     'holding': holdings
            # })
            args_dict_list.append({
                'table_name': f'alpha.YaoReV007-{delay}days-zz1000',
                'start_date': '20180101',
                'end_date': '20201231',
                'transform': 'Rank',
                'neutralize': 'Industry_with_weighted_cap',
                'holding': holdings
            })            
            # args_dict_list.append({
            #     'table_name': f'alpha.YaoMoM007-{delay}days-zz1000',
            #     'start_date': '20180101',
            #     'end_date': '20201231',
            #     'transform': 'Rank',
            #     'neutralize': 'Industry',
            #     'holding': holdings
            # })
            # args_dict_list.append({
            #     'table_name': f'alpha.YaoReV004-{delay}days-zz1000',
            #     'start_date': '20180101',
            #     'end_date': '20201231',
            #     'transform': 'Rank',
            #     'neutralize': 'None',
            #     'holding': holdings
            # })
            # args_dict_list.append({
            #     'table_name': f'alpha.YaoReV004-{delay}days-zz1000',
            #     'start_date': '20180101',
            #     'end_date': '20201231',
            #     'transform': 'None',
            #     'neutralize': 'Industry',
            #     'holding': holdings
            # })      
            # args_dict_list.append({
            #     'table_name': f'alpha.YaoReV004-{delay}days-zz1000',
            #     'start_date': '20180101',
            #     'end_date': '20201231',
            #     'transform': 'None',
            #     'neutralize': 'None',
            #     'holding': holdings
            # })
    # args_dict_list = [
    #     {
    #         'table_name': 'alpha.YaoReV004-20days-zz1000',
    #         'start_date': '20180101',
    #         'end_date': '20201231',
    #         'transform': 'Rank',
    #         'neutralize': 'Industry',
    #         'holding': 5
    #     },               
    #     # {
    #     #     'table_name': 'alpha.YaoReV006-20days-zz1000',
    #     #     'start_date': '20180101',
    #     #     'end_date': '20201231',
    #     #     'transform': 'Rank',
    #     #     'neutralize': 'Industry',
    #     #     'holding': 3
    #     # },      
    #     # {
    #     #     'table_name': 'alpha.YaoReV006-20days-zz1000',
    #     #     'start_date': '20180101',
    #     #     'end_date': '20201231',
    #     #     'transform': 'Rank',
    #     #     'neutralize': 'Industry',
    #     #     'holding': 10
    #     # },
    #     # {
    #     #     'table_name': 'alpha.YaoReV006-20days-zz1000',
    #     #     'start_date': '20180101',
    #     #     'end_date': '20201231',
    #     #     'transform': 'Rank',
    #     #     'neutralize': 'Industry',
    #     #     'holding': 1
    #     # },
    #     # {
    #     #     'table_name': 'alpha.YaoReV005-60days-zz1000',
    #     #     'start_date': '20180101',
    #     #     'end_date': '20201231',
    #     #     'transform': 'Rank',
    #     #     'neutralize': 'Industry',
    #     #     'holding': 20
    #     # },
    #     # {
    #     #     'table_name': 'alpha.YaoReV005-60days-zz1000',
    #     #     'start_date': '20180101',
    #     #     'end_date': '20201231',
    #     #     'transform': 'Rank',
    #     #     'neutralize': 'Industry',
    #     #     'holding': 60
    #     # },
    #     # {
    #     #     'table_name': 'alpha.YaoReV002-3days-20days-zz1000',
    #     #     'start_date': '20180101',
    #     #     'end_date': '20201231',
    #     #     'transform': 'Rank',
    #     #     'neutralize': 'Industry',
    #     #     'holding': 1
    #     # },
    #     # {
    #     #     'table_name': 'alpha.YaoReV002-1days-20days-zz1000',
    #     #     'start_date': '20180101',
    #     #     'end_date': '20201231',
    #     #     'transform': 'Rank',
    #     #     'neutralize': 'Industry',
    #     #     'holding': 1
    #     # },
    # ]
    perfmc.calc(args_dict_list)