"""  基础数据下载到本地的基类  """
import sqlite3
import datetime
from sqlalchemy import desc

from config import tushare_api
from models.table_models import *
from models.api import *
from utils import to_datetime
from utils import LoggerTushare


class MetaDataBase:
    def __init__(self):
        self.from_api = tushare_api.index_basic
        self.to_table = IndexBasic
        self.fields = ["ts_code", "name", "fullname", "market", "publisher", "index_type", "category",
                    "base_date", "base_point", "list_date", "weight_rule", "desc", "exp_date"]
        self.to_datetime_list = ['list_date', 'exp_date']
        self.frequency = 'monthly'
        self.logger = LoggerTushare(self.__class__.__name__).logger

    def get_frequency_date(self):
        # date是n年m月l日，全年第k周
        # yearly:  是否过了n年11月30，如果过了每次尝试更新下一年（n = 日历最后一天的年份）
        # monthly: 是否过了m+1月25，如果过了每天尝试更新m+1月
        # weekly:  是否过了第k+1周周五，如果过了每天尝试更新k+1周
        # dayly:   每天更新
        # 是否过了n+1月25，如果过了每天尝试更新n+1月
        if self.last_date == None:
            return datetime.datetime(year=1990, month=1, day=1)
        if self.frequency == 'yearly':
            return datetime.datetime(year=self.last_date.year, month=11, day=25)
        elif self.frequency == 'monthly':
            if self.last_date.month == 12:
                next_month = 1
            else:
                next_month = self.last_date.month+1
            return datetime.datetime(year=self.last_date.year, month=next_month, day=25)
        elif self.frequency == 'weekly':
            day = self.last_date.isocalendar()[2] # 周几
            if day >= 5:
                day_number = 5 - day + 7
            else:
                day_number = 5 - day
            return self.last_date + datetime.timedelta(days=day_number)
        elif self.frequency == 'dayly':
            return self.last_date

    def down(self):
        """ 下载数据 """
        df_table = self.from_api(fields=self.fields)
        if len(df_table)==0:
            self.logger.error(f'{self.to_table.__tablename__}下载失败')
        return df_table

    def process(self, df_table):
        """  处理数据  """
        for column_name in self.to_datetime_list:
            df_table[column_name] = df_table.apply(lambda x: to_datetime(x[column_name]), axis=1)
        return df_table

    def get_last_date(self):
        # 取下更细记录上数据标记日期，上次更新到n月2m日。
        query_magic = session.query(UpdateRecord.data_datetime).filter(UpdateRecord.table_name==self.to_table.__tablename__).order_by(desc(UpdateRecord.data_datetime)).limit(1)
        df_table = data_api.query(query_magic)
        if len(df_table) == 0:
            last_date = datetime.datetime(year=1990, month=1, day=1)
        else:
            last_date = df_table['data_datetime'][0]
        return last_date

    def pull(self):
        self.last_date = self.get_last_date()
        # date是n年m月l日，全年第k周
        # yearly:  是否过了n年11月30，如果过了每次尝试更新下一年（n = 日历最后一天的年份）
        # monthly: 是否过了m+1月25，如果过了每天尝试更新m+1月
        # weekly:  是否过了第k+1周周五，如果过了每天尝试更新k+1周
        # dayly:   每天更新
        # 记录现在时间 2023-04-29 10:15:59.517954
        today = datetime.datetime.today()
        if today > self.get_frequency_date():
            df_table = self.down()             # 下载数据
            df_table = self.process(df_table)  # 处理数据
            with engine.begin() as con:
                # 删除table
                data_api.delete_table(self.to_table)
                self.logger.info(f'删除{self.to_table.__tablename__}')
                df_table.to_sql(self.to_table.__tablename__, con=con, if_exists='append', index=False)  # 写入数据库
                # 标记更新日期到update_record上
                df_table2 = pd.DataFrame([[today]], columns=['data_datetime'])
                df_table2['table_name'] = self.to_table.__tablename__
                df_table2['created_datetime'] = today
                df_table2.to_sql(UpdateRecord.__tablename__, con=con, if_exists='append', index=False) # 记录更新
                self.logger.info(f'{self.to_table.__tablename__}写入成功')
        else:
            self.logger.info(f'表{self.to_table.__tablename__}已经更新到{self.last_date}, 不需要再更新')


if __name__ == "__main__":
    MetaDataBase().pull()
