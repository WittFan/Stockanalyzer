from config import SQLITE_URI
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, text, delete
import pandas as pd
from functools import partial
import pendulum
from models import table_models

engine = create_engine(SQLITE_URI, echo=False)  # 操作数据句柄
Session = sessionmaker(bind=engine)  # 这里一定要用上下文去管理session,否则会出现很多诡异的情况！！！切记
session = scoped_session(Session)  # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn #内部会采用threading.local进行隔离

class DataApi:

    @staticmethod
    def write(dataframe, table_model):
        """
        将数据写入本地sqlite
        :param dataframe:
        :param table_name:
        :return:
        """
        dataframe.to_sql(table_model.__tablename__, engine, if_exists='append', index=False)

    @staticmethod
    def delete_data(delete_magic):
        """ 删除表或表中数据 delete_magic: delete(User).where(User.name=='梁山') """
        session.execute(delete_magic)
        session.commit()  # 提交
        session.close()   # 关闭

    @staticmethod
    def delete_table(model):
        """ 删除表或表中数据 delete_magic: delete(User).where(User.name=='梁山') """
        model.__table__.drop(engine)

    def query(self, query_magic):
        """用 sqlAlchemy 的 session.query 查询数据库，结合pandas.read_sql"""
        df = pd.read_sql(query_magic.statement, query_magic.session.bind)
        session.close()
        return df

    @staticmethod
    def update(update_magic):
        # 进行更新操作
        session.execute(update_magic)
        # 提交与关闭
        session.commit()
        session.close()

    @staticmethod
    def sql(sql_str):
        data = session.execute(sql_str)
        session.close()
        df = pd.DataFrame(data)
        return df

    def __getattr__(self, table_name):
        """
        DataApi.name ， name为表名
        使用：
        data_api = DataApi()
        data_api.index_dailybasic('000001.SH', '20040101', '20230101')
        :param name:
        :return:
        """
        return partial(self.read, table_name)

    def read(self, table_name, **kwargs):
        # 构造 SQL 查询语句
        # 输出的字段fields
        table_model = getattr(table_models, table_name)
        try:
            fields = kwargs['fields']
            model_fields = []
            for i in fields:
                model_fields.append(getattr(table_model, i))
            query_magic = session.query(*model_fields)
        except:
            query_magic = session.query(table_model)
        # 查询的字段
        for key, value in kwargs.items():
            if key == 'fields':  # 因为前面对fields进行了处理
                continue
            elif key == 'start_date':
                query_magic = getattr(query_magic, 'filter')
                query_magic = query_magic(getattr(table_model, 'trade_date') >= value)
            elif key == 'end_date':
                query_magic = getattr(query_magic, 'filter')
                query_magic = query_magic(getattr(table_model, 'trade_date') <= value)
            else:
                query_magic = getattr(query_magic, 'filter')
                query_magic = query_magic(getattr(table_model, key) == value)
        df = self.query(query_magic)
        return df

# 创建实体
data_api = DataApi()

if __name__ == '__main__':
    pass
    from models.table_models import *
    # 1.增加数据
    # data_list = [['SSE', pendulum.parse('20230415'), 1, pendulum.parse('20230414')],
    #              ['SSE', pendulum.parse('20230414'), 1, pendulum.parse('20230413')]]
    # df = pd.DataFrame(data_list, columns=['exchange', 'cal_date', 'is_open', 'pretrade_date'])
    # data_api.write(df, Test)

    # 2.删除数据
    # 按照条件删除表数据
    # delete_magic = delete(Test).filter(Test)
    # data_api.delete_data(delete_magic)
    # # 清空表
    # delete_magic = session.execute(delete(Test))
    # data_api.delete_data()

    # 删除表
    data_api.delete_table(VerifyRecord)

    # # 3.更新数据
    # update_magic = update(Test).where(Test.cal_date == "20230415").values(cal_date="王老五")
    # data_api.update(update_magic)
    #
    # 4.查询数据
    query_magic = session.query(Test.id, Test.cal_date).filter(Test.id > 0).filter(Test.exchange=='SSE')
    df = data_api.query(query_magic)
    query_magic = session.query(TradeCal)
    df = data_api.query(query_magic)
    print(df)

    # # 5.原生sql
    # df = data_api.sql(text('select * from test;'))
    # print(df)

    # 6.dot表名查询
    # from datetime import datetime
    # start_time = datetime.now()
    # df = data_api.Daily(fields=['id', 'cal_date'], start_date=pendulum.parse('20230118'), end_date=pendulum.parse('20230401'))
    # time_spend = datetime.now() - start_time
    # print(df)
    # print(time_spend)

