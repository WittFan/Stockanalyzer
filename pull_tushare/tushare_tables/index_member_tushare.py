""" 申万行业成分 """
import datetime
import time

from config import tushare_api
from models.table_models import *
from models.api import *
from pull_tushare.tushare_tables.meta_data_base import MetaDataBase


class IndexMemberTushare(MetaDataBase):
    def __init__(self):
        super().__init__()
        self.from_api = tushare_api.index_member
        self.to_table = IndexMember
        self.fields = ['index_code', 'index_name', 'con_code', 'con_name', 'in_date', 'out_date', 'is_new']
        self.to_datetime_list = ['in_date', 'out_date']
        self.frequency = 'monthly'

    def down(self):
        """ 下载数据 """
        index_codes = data_api.IndexClassify(fields=['index_code'])
        df = self.from_api(index_code=index_codes.values[0][0], fields=self.fields)
        for index_code in index_codes.values[1:]:
            # 获取各个分类的成份股
            print(f'表{self.to_table.__tablename__}指数{index_code}的成分股')
            while True:
                try:
                    df2 = self.from_api(index_code=index_code[0])
                    break
                except:
                    print(f'表{self.to_table.__tablename__}等待5秒')
                    time.sleep(10)
            df = pd.concat([df, df2], axis=0)
        df = df.drop_duplicates()
        df['index_code_con_code_in_date'] = df.apply(lambda x: x['index_code'] + x['con_code'] + str(x['in_date']),
                                                     axis=1)
        return df


if __name__ == "__main__":
    IndexMemberTushare().pull()