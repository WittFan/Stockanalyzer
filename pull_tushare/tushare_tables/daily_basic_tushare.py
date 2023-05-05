"""  股票每日指标  """
import sys
sys.path.append('.')

from pull_tushare.tushare_tables.detail_data_base import *


class DaylyBasicTushare(DetailDataBase):
    def __init__(self):
        super().__init__()
        self.from_api = tushare_api.daily_basic
        self.to_table = DailyBasic
        self.fields = None
        self.to_datetime_list = ['trade_date']
        self.frequency = 'dayly'


if __name__ == '__main__':
    DaylyBasicTushare().pull()