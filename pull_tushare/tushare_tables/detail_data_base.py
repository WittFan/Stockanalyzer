"""  明细数据下载到本地的基类  """
import sqlite3
import datetime
import time
from sqlalchemy import desc, asc

from config import tushare_api
from models.table_models import *
from models.api import *
from utils import to_datetime
from utils import today_todatetime
from utils.logger import LoggerTushare


class DetailDataBase:
    def __init__(self):
        self.from_api = tushare_api.daily
        self.to_table = Daily
        self.fields = None
        self.to_datetime_list = ['trade_date']
        self.frequency = 'dayly'
        self.begin_time = datetime.datetime.now()
        self.logger = LoggerTushare(self.__class__.__name__).logger

    def get_last_date(self):
        """ 读取本地数据库最新日期的数据 """
        # 取下更细记录上数据标记日期，上次更新到n月m日。
        query_magic = session.query(UpdateRecord.data_datetime).filter(UpdateRecord.table_name==self.to_table.__tablename__).order_by(desc(UpdateRecord.data_datetime)).limit(1)
        df_table = data_api.query(query_magic)
        if len(df_table) == 0:
            date = None
        else:
            date = df_table['data_datetime'][0]
        return date

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

    def get_end_date(self):
        # 设end_date为今日，若今日不在日历里，则向前取最近的一个
        end_date = self.today
        while True:
            if end_date in self.record_cal:
                return end_date
            else:
                end_date = end_date - datetime.timedelta(days=1)

    def get_record_cal(self):
        # 股票的交易日历
        # SSE开始于19901219 SZSE开始于19910703，因此只需要SSE。返回的交易日历仅仅是从开始时间到今年最后一天，扣除节假日。
        query_magic = session.query(TradeCal).filter(TradeCal.exchange=='SSE').filter(TradeCal.is_open == '1').order_by(asc(TradeCal.cal_date))
        trade_cal = data_api.query(query_magic)['cal_date']
        trade_cal = list(trade_cal)
        return trade_cal

    def get_update_date_list(self):
        ##########  赋值下载的开始日期、结束日期  ###################
        if self.last_date is None:
            start_date = self.record_cal[0]
            self.last_date = start_date
        else:
            self.logger.info(f'{self.to_table.__tablename__}上一次更新到{str(self.last_date)}')
            start_date = self.record_cal[self.record_cal.index(self.last_date)+1]  # 在数据库的最后一个日期再往后移动一天
        # 计算需要更新的百分比
        update_percent = round(self.record_cal.index(self.last_date) / self.record_cal.index(self.end_date) * 100, 2)
        self.logger.info(f'表{self.to_table.__tablename__}已更新： {update_percent}%.下一步：{str(start_date)}至{str(self.end_date)}')
        # 准备下载日期区间[start_date, end_date]
        update_date_list = self.record_cal[self.record_cal.index(start_date):self.record_cal.index(self.end_date)+1]
        return update_date_list

    def get_data_from_tushare(self, date):
        df = self.from_api(trade_date=date.strftime('%Y%m%d'), fields=self.fields)
        return df

    def get_data_from_tushare_wait(self, date):
        # 如果接口有限制则等待20秒，直到可以继续调用
        while True:
            try:
                df = self.get_data_from_tushare(date)
                break
            except Exception as e:
                self.logger.warning(f'在下载表{self.to_table.__tablename__}{date}时等待20秒', e)
                time.sleep(20)
        return df

    def set_primary_key(self, df):
        # 添加primary key
        df['ts_code_trade_date'] = df.apply(lambda x: x['ts_code'] + str(x['trade_date']), axis=1)
        df = df.drop_duplicates('ts_code_trade_date')
        return df

    def process_data(self, df, date):
        # 判断date日期下是否有数据，有数据则添加primary key，添加更新记录
        if len(df) > 0:
            # 转换成时间
            for column_name in self.to_datetime_list:
                df[column_name] = df.apply(lambda x: to_datetime(x[column_name]), axis=1)
            # 设置关键值
            df = self.set_primary_key(df)
            # print(f'表{self.to_table.__tablename__}，日期{date}，下载处理数据成功，数据长度{len(df)}')
        return df

    def update_data(self):
        percent = 2
        for date in self.update_date_list:               # 遍历更新日期列表
            if round(self.update_date_list.index(date) / self.update_date_list.index(self.end_date) * 100, 2) >= percent:
                during_time = datetime.datetime.now() - self.begin_time
                self.logger.info(f'{self.to_table.__tablename__}写入{percent}%，已经用时{during_time}')
                percent += 2
            df = self.get_data_from_tushare_wait(date)   # 下载数据（从数据库最后日期到今天的
            df = self.process_data(df, date)             # 处理数据
            with engine.begin() as con:
                df.to_sql(self.to_table.__tablename__, con=con, if_exists='append', index=False)  # 写入数据库
                # 标记更新日期到update_record上
                df_table = pd.DataFrame([[date]], columns=['data_datetime'])
                df_table['table_name'] = self.to_table.__tablename__
                df_table['created_datetime'] = self.today
                df_table.to_sql(UpdateRecord.__tablename__, con=con, if_exists='append', index=False) # 记录更新

    def pull(self):
        # 判断现在到没到更新频率
        self.last_date = self.get_last_date()                # 更新最新记录日期
        frequency_date = self.get_frequency_date()           # 依据更新频率，设置更新日期边界
        self.today = today_todatetime()                      # 记录现在时间 2023-04-29 10:15:59.517954
        if self.today <= frequency_date:
            self.logger.info(f'{self.to_table.__tablename__}已经更新到{str(self.last_date)}, 现在不需要，大于{str(frequency_date)}再更新')
            return

        # 判断更新日期是不是到了日历最新
        self.record_cal = self.get_record_cal()              # 数据记录日历
        self.end_date = self.get_end_date()                  # 依据today，向前取日历结束日期
        if self.last_date == self.end_date:                  # 如果记录日期更新到日历结束日期，停止；否则继续
            self.logger.info(f'表{self.to_table.__tablename__}已更新到最近的日期{str(self.end_date)}')
            return
        self.update_date_list = self.get_update_date_list()  # 数据更新日期列表
        self.update_data()                                   # 更新数据


if __name__ == '__main__':
    DetailDataBase().pull()


