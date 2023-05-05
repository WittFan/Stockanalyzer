import tushare as ts
import pandas as pd
import numpy as np
import datetime, time
import sqlite3
import sqlite_data
from sqlite_data import DataApi
from sqlite_data import delete_table

class PullStockDailyNewData:
    def __init__(self, table_name):
        self.table_name = table_name
        self.data_api = DataApi() # 本地数据库数据接口
        self.pro = ts.pro_api()   # tushare云端数据接口
        self.today = datetime.datetime.now()
        self.last_day_sql=f"""select trade_date from {self.table_name} where ts_code=='update_date_record' order
                 by rowid desc limit 1;"""

    def get_record_cal(self):
        # 股票的交易日历
        # SSE开始于19901219 SZSE开始于19910703，因此只需要SSE。返回的交易日历仅仅是从开始时间到今年最后一天，扣除节假日。
        trade_cal = list(self.data_api.trade_cal(exchange='SSE', is_open='1',fields=['cal_date'])['cal_date'][::-1])
        return trade_cal

    def get_last_day(self):
        """读取本地数据库最新日期的数据"""
        # 从数据库的update_date_record中查询更新的最后一个日期
        conn = sqlite3.connect(self.data_api.database)
        c = conn.cursor()
        c.execute(self.last_day_sql)
        conn.commit()
        date = c.fetchall()
        if date == []:
            return None
        date = date[0][0]
        conn.close()
        return date

    def get_end_date(self):
        # end_date为今日，若今日不在日历里，则向前取最近的一个
        end_date_timestamp = self.today
        self.end_date = end_date_timestamp.strftime("%Y%m%d")
        while True:
            if self.end_date in self.record_cal:
                return
            else:
                end_date_timestamp = end_date_timestamp - datetime.timedelta(days=1)
                self.end_date = end_date_timestamp.strftime("%Y%m%d")

    def get_update_date_list(self):
        ##########  赋值下载的开始日期、结束日期  ###################
        if self.last_day is None:
            start_date = self.record_cal[0]
            self.last_day = self.record_cal[0] #为了在下一个if判断有数值，该变量必须有数值
        else:
            print('上一次更新到', self.last_day)
            start_date = self.record_cal[self.record_cal.index(self.last_day)+1]  # 在数据库的最后一个日期再往后移动一天
        # 计算需要更新的百分比
        update_percent = round(self.record_cal.index(self.last_day) / self.record_cal.index(self.end_date) * 100, 2)
        print(f'表{self.table_name}已更新： {update_percent}%，', '下一步', start_date, self.end_date)
        # 准备下载日期区间[start_date, end_date]
        update_date_list = self.record_cal[self.record_cal.index(start_date):self.record_cal.index(self.end_date)+1]
        return update_date_list

    def get_data_from_tushare(self, date):
        df = self.pro.query(self.table_name, trade_date=date)
        return df

    def get_data_from_tushare_wait(self, date):
        # 如果接口有限制则等待5秒，直到可以继续调用
        while True:
            try:
                df = self.get_data_from_tushare(date)
                break
            except Exception as e:
                print(f'在下载表{self.table_name}{date}时等待20秒', e)
                time.sleep(20)
        return df

    def set_primary_key(self, df):
        # 添加primary key
        df['ts_code_trade_date'] = df.apply(lambda x: x['ts_code'] + str(x['trade_date']), axis=1)
        df = df.drop_duplicates('ts_code_trade_date')
        return df

    def add_update_date_record(self, df, date):
        # 标记已更新日期到ts_code = update_date_record 数据上
        df2 = pd.DataFrame({'trade_date': [date]})
        df2['ts_code'] = 'update_date_record'
        df2 = self.set_primary_key(df2)
        df = pd.concat([df, df2], axis=0)
        return df

    def process_data(self, df, date):
        # 判断date日期下是否有数据，有数据则添加primary key，添加更新记录
        if len(df) > 0:
            df = self.set_primary_key(df)
            print(f'表{self.table_name}，日期{date}，下载处理数据成功，数据长度{len(df)}')
            df = self.add_update_date_record(df, date)
        return df

    def write_sqlite_data(self, df, date):
        # 将下载的数据插入数据库
        try:
            sqlite_data.write(df, self.table_name)
            print(f'表{self.table_name}，日期{date}，入库数据成功   ，数据长度{len(df)}')
        except sqlite3.IntegrityError:
            print('表{table_name}已经存在或%s' % sqlite3.IntegrityError)

    def update_data(self):
        for date in self.update_date_list:  # 遍历更新日期列表
            df = self.get_data_from_tushare_wait(date)  # 下载数据（从数据库最后日期到今天的
            df = self.process_data(df, date)  # 处理数据
            self.write_sqlite_data(df, date)  # 写入数据库

    def run(self):
        self.last_day = self.get_last_day()  # 更新的最新日期
        self.record_cal = self.get_record_cal()  # 数据记录日历
        self.get_end_date()  # 获取结束日期
        if self.last_day == self.end_date:  # 如果更新到今天，停止；否则获取更新日期列表
            print(f'表{self.table_name}已更新到最近的日期{self.end_date}')
            return
        self.update_date_list = self.get_update_date_list()  # 数据更新日期列表
        self.update_data()

class PullStkHolderTradeDailyNewData(PullStockDailyNewData):
    def __init__(self, table_name):
        super().__init__(table_name)
        self.last_day_sql = f"""select ann_date from {self.table_name} where ts_code=='update_date_record' order
         by rowid desc limit 1;"""

    def get_record_cal(self):
        # 股票的交易日历
        # SSE开始于19901219 SZSE开始于19910703，因此只需要SSE。返回的交易日历仅仅是从开始时间到今年最后一天，包括节假日。
        trade_cal = list(self.data_api.trade_cal(exchange='SSE', fields=['cal_date'])['cal_date'][::-1])
        return trade_cal

    def get_data_from_tushare(self, date):
        df = self.pro.query(self.table_name, ann_date=date)
        return df

    def set_primary_key(self, df):
        # 添加primary key
        df['ts_code_ann_date_holder_name_after_share'] = df.apply(
            lambda x: x['ts_code'] + x['ann_date'] + x['holder_name'] + str(x['after_share']), axis=1)
        df = df.drop_duplicates('ts_code_ann_date_holder_name_after_share')
        return df

    def add_update_date_record(self, df, date):
        df2 = pd.DataFrame({'ann_date': [date]})
        df2['ts_code'] = 'update_date_record'
        df2['holder_name'] = 'null'
        df2['after_share'] = 100
        df2 = self.set_primary_key(df2)
        df = pd.concat([df, df2], axis=0)
        return df

class PullStockWeeklyNewData(PullStockDailyNewData):
    def __init__(self, table_name):
        super().__init__(table_name)

    def get_record_cal(self):
        # 交易日历上每周最后一个交易日
        # SSE开始于19901219 SZSE开始于19910703，因此只需要SSE。返回的交易日历仅仅是从开始时间到今年最后一天，扣除节假日。
        trade_cal = pd.DataFrame(self.data_api.trade_cal(exchange='SSE', is_open='1', fields=['cal_date'])['cal_date'][::-1])
        trade_cal['week_info'] = trade_cal.apply(
            lambda x: datetime.datetime.strptime(x['cal_date'], '%Y%m%d').date().isocalendar(), axis=1)
        trade_cal['year'] = trade_cal.apply(lambda x: x['week_info'][0], axis=1)
        trade_cal['week'] = trade_cal.apply(lambda x: x['week_info'][1], axis=1)
        trade_cal['day'] = trade_cal.apply(lambda x: x['week_info'][2], axis=1)
        df = trade_cal.groupby(['year', 'week']).apply(lambda x: x[x['day'] == x['day'].max()])
        cal_date_list = list(df['cal_date'])
        return cal_date_list

class PullStockMonthlyNewData(PullStockDailyNewData):
    """ 下载股票月度行情 """
    def __init__(self, table_name):
        super().__init__(table_name)

    def get_record_cal(self):
        # 交易日历上每周最后一个交易日
        # SSE开始于19901219 SZSE开始于19910703，因此只需要SSE。返回的交易日历仅仅是从开始时间到今年最后一天，扣除节假日。
        trade_cal = pd.DataFrame(self.data_api.trade_cal(exchange='SSE', is_open='1', fields=['cal_date'])['cal_date'][::-1])
        trade_cal['month_info'] = trade_cal.apply(
            lambda x: datetime.datetime.strptime(x['cal_date'], '%Y%m%d').date(), axis=1)
        trade_cal['year'] = trade_cal.apply(lambda x: x['month_info'].year, axis=1)
        trade_cal['month'] = trade_cal.apply(lambda x: x['month_info'].month, axis=1)
        trade_cal['day'] = trade_cal.apply(lambda x: x['month_info'].day, axis=1)
        df = trade_cal.groupby(['year', 'month']).apply(lambda x: x[x['day'] == x['day'].max()])
        cal_date_list = list(df['cal_date'])
        return cal_date_list

class PullFxDailyNewData(PullStockDailyNewData):
    """ 下载外汇日线行情 """
    def __init__(self, table_name):
        super().__init__(table_name)

    def get_record_cal(self):
        trade_cal = list(self.data_api.trade_cal(exchange='SSE', fields=['cal_date'])['cal_date'][::-1])
        return trade_cal

class PullStockMxNewData(PullStockDailyNewData):
    """ 下载外汇日线行情 """
    def __init__(self, table_name):
        super().__init__(table_name)

    def get_record_cal(self):
        trade_cal = list(self.data_api.trade_cal(exchange='SSE', is_open='1', fields=['cal_date'])['cal_date'][::-1])
        trade_cal = trade_cal[trade_cal.index('20140102'):]
        return trade_cal

    def set_primary_key(self, df):
        # 添加primary key
        df.dropna(subset=['ts_code', 'trade_date'], inplace=True)
        df['ts_code_trade_date'] = df.apply(lambda x: x['ts_code'] + str(x['trade_date']), axis=1)
        df = df.drop_duplicates('ts_code_trade_date')
        return df

class PullIndexDailyNewData(PullStockDailyNewData):
    """ 下载外汇日线行情 """
    def __init__(self, table_name):
        super().__init__(table_name)
        self.ts_code_set = {'000001.SH': '上证指数', '000300.SH': '沪深300', '000905.SH': '中证500', '399001.SZ': '深证成指',
                        '399005.SZ': '中小100', '399006.SZ': '创业板指', '399016.SZ': '', '399300.SZ': '沪深300',
                        '000005.SH': '商业指数', '000006.SH': '地产指数', '000016.SH': '上证５０', '399905.SZ': '中证 500'}
        self.day_num = 7999  # day_num为tushare的接口限制

    def get_record_cal(self):
        # 股票的交易日历
        # SSE开始于19901219 SZSE开始于19910703，因此只需要SSE。返回的交易日历仅仅是从开始时间到今年最后一天，扣除节假日。
        trade_cal = list(self.data_api.trade_cal(exchange='SSE', fields=['cal_date'])['cal_date'][::-1])
        return trade_cal

    def get_data_from_tushare(self, ts_code, start_date, end_date):
        """从tushare获取数据"""
        df = self.pro.query(self.table_name, ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df

    def get_data_from_tushare_wait(self, ts_code, start_date, end_date):
        # 如果接口有限制则等待5秒，直到可以继续调用
        while True:
            try:
                df = self.get_data_from_tushare(ts_code, start_date, end_date)
                break
            except Exception as e:
                print(f'在下载表{self.table_name}{start_date}-{end_date}时等待20秒', e)
                time.sleep(20)
        return df

    def add_update_date_record(self, df, date):
        # 标记已更新日期到ts_code = update_date_record 数据上
        df2 = pd.DataFrame({'trade_date': date})
        df2['ts_code'] = 'update_date_record'
        df2 = self.set_primary_key(df2)
        df = pd.concat([df, df2], axis=0)
        return df

    def write_sqlite_data(self, df, dates, ts_code):
        # 将下载的数据插入数据库
        try:
            sqlite_data.write(df, self.table_name)
            print(f'表{self.table_name}，日期{dates[0]}-{dates[-1]}，{ts_code}入库数据成功   ，数据长度{len(df)}')
        except sqlite3.IntegrityError:
            print(f'表{self.table_name}{ts_code}已经存在或%s' % sqlite3.IntegrityError)

    def update_data(self):
        data_length = 0
        for ts_code in self.ts_code_set:
            # 遍历IndexDailybasic的所有代码ts_code
            day_num = self.day_num  # day_num为tushare的接口限制
            start_date = self.update_date_list[0]
            end_date = self.update_date_list[-1]
            if len(self.update_date_list) >= day_num:
                mid_date = self.update_date_list[day_num - 1]
            else:
                mid_date = end_date
            df = pd.DataFrame()
            while int(mid_date) < int(end_date):
                # 如果mid_date没有超过end_date，就一直获取
                df2 = self.get_data_from_tushare_wait(ts_code=ts_code, start_date=start_date, end_date=mid_date)
                df = pd.concat([df, df2], axis=0)
                start_date = self.update_date_list[day_num]
                day_num += day_num
                if len(self.update_date_list) >= day_num:
                    mid_date = self.update_date_list[day_num - 1]
                else:
                    mid_date = end_date
            df2 = self.get_data_from_tushare_wait(ts_code=ts_code, start_date=start_date, end_date=mid_date)
            df = pd.concat([df, df2], axis=0)
            if len(df)==0:
                continue
            # 按照trade_date排序
            df = df.sort_values(by='trade_date')
            # 将排序前的序号删掉
            df = df.reset_index(drop=True)
            self.set_primary_key(df)
            self.write_sqlite_data(df, self.update_date_list, ts_code)
            data_length += len(df)
        print(f'更新表{self.table_name}，日期{self.update_date_list[0]}-{self.update_date_list[-1]},数据长度{data_length}')
        if data_length > 0:
            print(f'表{self.table_name}，日期{self.update_date_list[0]}-{self.update_date_list[-1]}，入库数据成功，数据长度{data_length}')
            df = self.data_api.query(self.table_name, ts_code='')
            df = self.add_update_date_record(df, self.update_date_list)
            self.write_sqlite_data(df, self.update_date_list, 'update_date_record')

    def run(self):
        self.last_day = self.get_last_day()  # 更新的最新日期
        self.record_cal = self.get_record_cal()  # 数据记录日历
        self.get_end_date()  # 获取结束日期
        if self.last_day == self.end_date:  # 如果更新到今天，停止；否则获取更新日期列表
            print(f'表{self.table_name}已更新到最近的日期{self.end_date}')
            return
        self.update_date_list = self.get_update_date_list()  # 数据更新日期列表
        self.update_data()

class PullIndexDailyBasicNewData(PullIndexDailyNewData):
    """ 下载外汇日线行情 """
    def __init__(self, table_name):
        super().__init__(table_name)
        self.ts_code_set = {'000001.SH': '上证指数', '000300.SH': '沪深300', '000905.SH': '中证500', '399001.SZ': '深证成指',
                        '399005.SZ': '中小100', '399006.SZ': '创业板指', '399016.SZ': '', '399300.SZ': '沪深300',
                        '000005.SH': '商业指数', '000006.SH': '地产指数', '000016.SH': '上证５０', '399905.SZ': '中证 500'}
        self.day_num = 12*360 # tushare的个数限制

class PullMetaData:
    def __init__(self):
        self.pro = ts.pro_api()

    def pull_stock_basic_all(self):
        """1.股票列表stock_basic"""
        df = self.pro.stock_basic(fields='ts_code,symbol,name,area,industry,fullname,enname,cnspell,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
        delete_table('stock_basic')
        print('删除stock_basic')
        try:
            sqlite_data.write(df, 'stock_basic')
            print('stock_basic下载成功')
        except sqlite3.IntegrityError:
            print('stock_basic已经存在或%s' %sqlite3.IntegrityError)

    def pull_trade_cal_all(self):
        """2.交易日历trade_cal"""
        # 交易所SSE上交所, SZSE深交所, CFFEX中金所, SHFE上期所, CZCE郑商所, DCE大商所, INE上能源
        df = pd.DataFrame()
        for i in ['SSE', 'SZSE', 'CFFEX', 'SHFE', 'CZCE', 'DCE', 'INE']:
            df2 = self.pro.trade_cal(exchange=i)
            df = pd.concat([df, df2], axis=0)
        df['exchange_cal_date'] = df.apply(lambda x: x['exchange'] + str(x['cal_date']), axis=1)
        delete_table('trade_cal')
        print('删除trade_cal')
        try:
            sqlite_data.write(df, 'trade_cal')
            print('trade_cal下载成功')
        except sqlite3.IntegrityError:
            print('trade_cal已经存在或%s' %sqlite3.IntegrityError)

    def pull_namechange_all(self):
        """3.股票曾用名namechange"""
        df = self.pro.namechange()
        delete_table('namechange')
        print('删除namechange')
        try:
            sqlite_data.write(df, 'namechange')
            print('namechange下载成功')
        except sqlite3.IntegrityError:
            print('namechange已经存在或%s' % sqlite3.IntegrityError)

    def pull_hs_const_all(self):
        """4.沪深股通成份股hs_const"""
        df1 = self.pro.hs_const(hs_type='SH')
        df2 = self.pro.hs_const(hs_type='SZ')
        df = pd.concat([df1, df2], axis=0)
        delete_table('hs_const')
        print('删除hs_const')
        try:
            sqlite_data.write(df, 'hs_const')
            print('hs_const下载成功')
        except sqlite3.IntegrityError:
            print('hs_const已经存在或%s' % sqlite3.IntegrityError)

    def pull_stock_company_all(self):
        """5.上市公司基本信息stock_company"""
        df1 = self.pro.stock_company(exchange='SSE',
                                fields='ts_code, exchange, chairman, manager, secretary, reg_capital,setup_date,province, city, introduction, website, email, office, employees, main_business, business_scope')
        df2 = self.pro.stock_company(exchange='SZSE',
                                fields='ts_code, exchange, chairman, manager, secretary, reg_capital, setup_date,province, city, introduction, website, email, office, employees, main_business, business_scope')
        df = pd.concat([df1, df2], axis=0)
        delete_table('stock_company')
        print('删除stock_company')
        try:
            sqlite_data.write(df, 'stock_company')
            print('stock_company下载成功')
        except sqlite3.IntegrityError:
            print('stock_company已经存在或%s' % sqlite3.IntegrityError)

    def pull_index_basic_all(self):
        """6.指数基本信息index_basic"""
        df = self.pro.index_basic(fields=["ts_code", "name", "fullname", "market", "publisher", "index_type", "category",
                                     "base_date", "base_point", "list_date", "weight_rule", "desc", "exp_date"])
        from sqlite_data import delete_table
        delete_table('index_basic')
        print('删除index_basic')
        try:
            sqlite_data.write(df, 'index_basic')
            print('index_basic下载成功')
        except sqlite3.IntegrityError:
            print('index_basic已经存在或%s' % sqlite3.IntegrityError)

    def pull_index_classify_all(self):
        """15.申万行业分类index_classify"""
        # 获取申万一级行业列表
        df1 = self.pro.index_classify(level='L1', src='SW2021',
                                 fields='index_code, industry_name, level, industry_code, is_pub, parent_code, src')
        # 获取申万二级行业列表
        df2 = self.pro.index_classify(level='L2', src='SW2021',
                                 fields='index_code, industry_name, level, industry_code, is_pub, parent_code, src')
        # 获取申万三级级行业列表
        df3 = self.pro.index_classify(level='L3', src='SW2021',
                                 fields='index_code, industry_name, level, industry_code, is_pub, parent_code, src')
        df = pd.concat([df1, df2, df3], axis=0)
        delete_table('index_classify')
        print('删除index_classify')
        try:
            sqlite_data.write(df, 'index_classify')
            print('index_classify下载成功')
        except sqlite3.IntegrityError:
            print('index_classify已经存在或%s' % sqlite3.IntegrityError)

    def pull_fx_obasic_all(self):
        df = self.pro.fx_obasic()
        delete_table('fx_obasic')
        print('删除fx_obasic')
        try:
            sqlite_data.write(df, 'fx_obasic')
            print('fx_obasic下载成功')
        except sqlite3.IntegrityError:
            print('fx_obasic已经存在或%s' % sqlite3.IntegrityError)

    def pull_index_daily_all_data(self):
        """
        拉取大盘指数每日指标index_daily到本地，并存储
        指数范围：self.ts_code_set
        :return:
        """
        for ts_code in self.ts_code_set:
            # 遍历IndexDailybasic的所有代码ts_code
            start_date = datetime.date(1990, 1, 1) # 开始时间
            end_date = datetime.date.today() # 结束时间
            day_num = 7900 # tushare的个数限制
            df = self.get_daily_data(start_date, end_date, ts_code, day_num, self.pro.index_daily)
            df['ts_code_trade_date'] = df.apply(lambda x: x['ts_code'] + str(x['trade_date']), axis=1)
            try:
                sqlite_data.write(df, 'index_daily')
                print('%s下载成功' % ts_code)
            except sqlite3.IntegrityError:
                print('%s已经存在' %ts_code)

    def pull_index_dailybasic_all_data(self):
        # 拉取大盘指数每日指标index_dailybasic到本地，并存储
        for ts_code in self.ts_code_set:
            # 遍历IndexDailybasic的所有代码ts_code
            start_date = datetime.date(2004, 1, 1) # 开始时间
            end_date = datetime.date.today() # 结束时间
            day_num = 12*360 # tushare的个数限制
            df = self.get_daily_data(start_date, end_date, ts_code, day_num, self.pro.index_dailybasic)
            df['ts_code_trade_date'] = df.apply(lambda x: x['ts_code'] + str(x['trade_date']), axis=1)
            try:
                sqlite_data.write(df, 'index_dailybasic')
            except sqlite3.IntegrityError:
                print('%s已经存在' %ts_code)

    def pull_index_member_all(self):
        data_api = DataApi()
        index_codes = data_api.index_classify(fields=['index_code'])
        df = self.pro.index_member(index_code=index_codes.values[0][0], fields=['index_code', 'index_name',
                                                                           'con_code', 'con_name', 'in_date',
                                                                           'out_date', 'is_new'])
        for index_code in index_codes.values[1:]:
            # 获取黄金分类的成份股
            print(index_code[0])
            while True:
                try:
                    df2 = self.pro.index_member(index_code=index_code[0])
                    break
                except:
                    print('等待5秒')
                    time.sleep(5)
            df = pd.concat([df, df2], axis=0)
        df = df.drop_duplicates()
        df['index_code_con_code_in_date'] = df.apply(lambda x: x['index_code'] + x['con_code'] + str(x['in_date']),
                                                     axis=1)
        try:
            sqlite_data.write(df, 'index_member')
            print('index_member下载成功')
        except sqlite3.IntegrityError:
            print('index_member已经存在或%s' % sqlite3.IntegrityError)

    def pull_all_meta_data(self):
        """
        tushare所有全量数据拉取到本地并存储，基本信息部分
        :return:
        """
        self.pull_stock_basic_all()
        self.pull_trade_cal_all()
        self.pull_namechange_all()
        self.pull_hs_const_all()
        self.pull_stock_company_all()
        self.pull_index_basic_all()
        self.pull_index_classify_all()
        self.pull_fx_obasic_all()
        self.pull_index_member_all()

def pull_all_detail_data():
    """
    tushare所有全量数据拉取到本地并存储，明细表部分
    :return:
    """
    # 只需遍历日期
    PullStkHolderTradeDailyNewData('stk_holdertrade').run()  # 股东增减持
    PullStockDailyNewData('daily_basic').run()               # 每日指标
    PullStockDailyNewData('daily').run()                     # 日线行情
                                                             # 复权因子
                                                             # 复权日线行情
    PullStockWeeklyNewData('weekly').run()                   # 周线行情
    PullStockMonthlyNewData('monthly').run()                 # 月线行情
    PullFxDailyNewData('fx_daily').run()                     # 外汇日线行情fx_daily
    PullStockMxNewData('stock_mx').run()                     # 动能因子stock_mx
    PullStockMxNewData('stock_vx').run()                     # 估值因子stock_vx

    # 先遍历日期，再遍历ts_code或index_code
    # self.pull_stk_rewards_all_data()                       # 1 管理层薪酬和持股 按照日期遍历(报告期才有数据),query股票股票列表所有数据
    PullIndexDailyNewData('index_daily').run()               # 3 先日期再遍历指数，指数只更新一部分
    PullIndexDailyBasicNewData('index_dailybasic').run()     # 2 先日期再遍历指数

    # 特色数据有接口限制
    PullStockDailyNewData('stk_factor').run()                # 股票技术因子（量化因子）ts_code、trade_date必须选择一个

if __name__ == '__main__':
    # from sqlite_data import delete_table
    # delete_table('index_dailybasic')

    # from sql_create_table import create_table
    # create_table()
    # PullMetaData().pull_all_meta_data()
    pull_all_detail_data()

