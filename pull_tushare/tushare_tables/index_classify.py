""" 申万行业分类 """
import datetime

from config import tushare_api
from models.table_models import *
from models.api import *
from pull_tushare.tushare_tables.meta_data_base import MetaDataBase


class IndexClassifyTushare(MetaDataBase):
    def __init__(self):
        super().__init__()
        self.from_api = tushare_api.index_classify
        self.to_table = IndexClassify
        self.fields = 'index_code, industry_name, level, industry_code, is_pub, parent_code, src'
        self.to_datetime_list = []
        self.frequency = 'monthly'
        self.begin_time = datetime.datetime.now()

    def down(self):
        """ 下载数据 """
        # 获取申万一级行业列表
        df1 = self.from_api(level='L1', src='SW2021', fields=self.fields)
        # 获取申万二级行业列表
        df2 = self.from_api(level='L2', src='SW2021', fields=self.fields)
        # 获取申万三级级行业列表
        df3 = self.from_api(level='L3', src='SW2021', fields=self.fields)
        df = pd.concat([df1, df2, df3], axis=0)
        if len(df) == 0:
            print(f'{self.to_table.__tablename__}下载失败')
        return df

if __name__ == "__main__":
    IndexClassifyTushare().pull()