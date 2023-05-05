""" 日历 """
import sqlite3
import datetime

from config import tushare_api
from models.table_models import *
from models.api import *
from pull_tushare.tushare_tables.meta_data_base import MetaDataBase
from utils import to_datetime


class TradeCalTushare(MetaDataBase):
    def __init__(self):
        super().__init__()
        self.from_api = tushare_api.trade_cal
        self.to_table = TradeCal
        self.fields = None

    def down(self):
        """ 下载数据 """
        # 交易所SSE上交所, SZSE深交所, CFFEX中金所, SHFE上期所, CZCE郑商所, DCE大商所, INE上能源
        df_table = pd.DataFrame()
        for i in ['SSE', 'SZSE', 'CFFEX', 'SHFE', 'CZCE', 'DCE', 'INE']:
            df_table2 = tushare_api.trade_cal(exchange=i)
            df_table = pd.concat([df_table, df_table2], axis=0)
        if len(df_table) == 0:
            self.logger.error(f'{self.to_table.__tablename__}下载失败')
        return df_table

    def process(self, df_table):
        """  处理数据  """
        df_table['cal_date'] = df_table.apply(lambda x: to_datetime(x['cal_date']), axis=1)
        df_table['pretrade_date'] = df_table.apply(lambda x: to_datetime(x['pretrade_date']), axis=1)
        df_table['exchange_cal_date'] = df_table.apply(lambda x: x['exchange'] + str(x['cal_date']), axis=1)
        return df_table

    def write(self, df_table):
        """2.交易日历trade_cal"""
        data_api.delete_data(delete(TradeCal))
        data_api.delete_data(delete(TradeWeek))
        data_api.delete_data(delete(TradeMonth))
        self.logger.info('删除trade_cal、trade_week、trade_month')
        try:
            data_api.write(df_table, TradeCal)
            self.logger.info('trade_cal写入数据成功')
            self.write_TradeWeek()
            self.write_TradeMonth()
        except sqlite3.IntegrityError:
            self.logger.warning('trade_cal已经存在或%s' % sqlite3.IntegrityError)

    def write_TradeWeek(self):
        # 交易日历上每周最后一个交易日
        # SSE开始于19901219 SZSE开始于19910703，因此只需要SSE。返回的交易日历仅仅是从开始时间到今年最后一天，扣除节假日。
        trade_cal = pd.DataFrame(data_api.query(session.query(TradeCal).filter(TradeCal.exchange=='SSE').filter(TradeCal.is_open=='1'))['cal_date'][::-1])
        trade_cal['week_info'] = trade_cal.apply(lambda x: x['cal_date'].date().isocalendar(), axis=1)
        trade_cal['year'] = trade_cal.apply(lambda x: x['week_info'][0], axis=1)
        trade_cal['week'] = trade_cal.apply(lambda x: x['week_info'][1], axis=1)
        trade_cal['day'] = trade_cal.apply(lambda x: x['week_info'][2], axis=1)
        df = trade_cal.groupby(['year', 'week']).apply(lambda x: x[x['day'] == x['day'].max()])
        df['pretrade_date'] = df['cal_date'].shift()
        df['exchange'] = 'SSE'
        df = df.drop(columns=['week_info', 'year', 'week', 'day'])
        try:
            data_api.write(df, TradeWeek)
            self.logger.info('trade_week写入数据成功')
        except sqlite3.IntegrityError:
            self.logger.warning('trade_week已经存在或%s' % sqlite3.IntegrityError)

    def write_TradeMonth(self):
        # 交易日历上每周最后一个交易日
        # SSE开始于19901219 SZSE开始于19910703，因此只需要SSE。返回的交易日历仅仅是从开始时间到今年最后一天，扣除节假日。
        trade_cal = pd.DataFrame(data_api.query(session.query(TradeCal).filter(TradeCal.exchange=='SSE').filter(TradeCal.is_open=='1'))['cal_date'][::-1])
        trade_cal['month_info'] = trade_cal.apply(lambda x: x['cal_date'].date(), axis=1)
        trade_cal['year'] = trade_cal.apply(lambda x: x['month_info'].year, axis=1)
        trade_cal['month'] = trade_cal.apply(lambda x: x['month_info'].month, axis=1)
        trade_cal['day'] = trade_cal.apply(lambda x: x['month_info'].day, axis=1)
        df = trade_cal.groupby(['year', 'month']).apply(lambda x: x[x['day'] == x['day'].max()])
        df['pretrade_date'] = df['cal_date'].shift()
        df['exchange'] = 'SSE'
        df = df.drop(columns=['month_info', 'year', 'month', 'day'])
        try:
            data_api.write(df, TradeMonth)
            self.logger.info('trade_month写入数据成功')
        except sqlite3.IntegrityError:
            self.logger.warning('trade_month已经存在或%s' % sqlite3.IntegrityError)

    def record(self, today, df_table):
        df_record = pd.DataFrame()
        df_record['data_datetime'] = df_table['cal_date']
        df_record['table_name'] = self.to_table.__tablename__
        df_record['created_datetime'] = today
        data_api.write(df_record, UpdateRecord)

    def pull(self):
        # 取下更细记录上数据标记日期，上次更新到n年12月2m日。
        query_magic = session.query(UpdateRecord.data_datetime).filter(UpdateRecord.table_name==self.to_table.__tablename__).limit(1)
        df_table = data_api.query(query_magic)
        # 记录现在时间 2023-04-29 10:15:59.517954
        today = datetime.datetime.today()
        if len(df_table) == 0:
            date = datetime.datetime(year=1990, month=1, day=1)
        else:
            date = df_table['data_datetime'][0]
        # 是否过了n年11月30，如果过了每次尝试更新下一年（n = 日历最后一天的年份）
        if today > datetime.datetime(year=date.year, month=11, day=30):
            df_table = self.down()       # 下载数据
            df_table = self.process(df_table)  # 处理数据
            self.write(df_table)         # 写入数据
            self.record(today, df_table)     # 记录更新
        else:
            self.logger.info(f'表{self.to_table.__tablename__}已经更新到{date}, 不需要再更新')


if __name__ == "__main__":
    TradeCalTushare().pull()