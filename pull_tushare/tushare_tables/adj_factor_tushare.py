"""  股票复权因子  """
import sys
sys.path.append('.')

from pull_tushare.tushare_tables.detail_data_base import *


class AdjFactorTushare(DetailDataBase):
    def __init__(self):
        super().__init__()
        self.from_api = tushare_api.adj_factor
        self.to_table = AdjFactor
        self.fields = None
        self.to_datetime_list = ['trade_date']
        self.frequency = 'dayly'


if __name__ == '__main__':
    AdjFactorTushare().pull()