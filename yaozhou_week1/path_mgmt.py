import pandas as pd
import numpy as np
import json
from json import JSONEncoder
import glob
from pathlib import Path
from tqdm.auto import tqdm
import os
import zipfile
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR/'data'

DATA_MAPPING = {"stk_1min": '1minProcess',
           "adj_factor": "adj_fct",
           "index": 'idx',
           "limits": "lmt",
           "mkt_value": "mkt_val",
           "industry": "sw",
           "universe": "univ",
           "halt_date": 'dateProcess',
           "ST_date": 'dateProcess'}

def getfilePath(tab_name, date, indexName=None):
    if tab_name in ["index", "adj_factor", "limits", "mkt_value", "industry"]:
        return DATA_DIR/DATA_MAPPING[tab_name]/date[:4]/(date+'.csv')
    elif tab_name == "universe":
        return DATA_DIR/DATA_MAPPING[tab_name]/indexName/date[:4]/(date+'.csv')
    elif tab_name == "stk_1min":
        return DATA_DIR/DATA_MAPPING[tab_name]/(date+'.csv')
    elif tab_name in ["halt_date", "ST_date"]:
        return DATA_DIR/DATA_MAPPING[tab_name]/(tab_name +'.csv')
