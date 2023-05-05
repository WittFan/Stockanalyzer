""" 股票基本信息 """
import sqlite3
import datetime
import pendulum

from config import tushare_api
from models.table_models import *
from models.api import *
from utils import to_datetime
from pull_tushare.tushare_tables.meta_data_base import MetaDataBase

# 任务：
# 1.重构基本信息下载的基类
# 2.解决tushare一次下载8000的限制
# 3.重写trade_cal


class StockBasicTushare(MetaDataBase):
    def __init__(self):
        super().__init__()
        self.from_api = tushare_api.stock_basic
        self.to_table = StockBasic
        self.fields = 'ts_code,symbol,name,area,industry,fullname,enname,cnspell,market,exchange,curr_type,list_status,list_date,delist_date,is_hs'
        self.to_datetime_list = ['list_date', 'list_date']
        self.frequency = 'monthly'


if __name__ == "__main__":
    StockBasicTushare().pull()
