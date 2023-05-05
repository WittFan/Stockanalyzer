import models
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from config import SQLITE_URI
import pandas as pd

# engine = create_engine(SQLITE_URI) # 操作数据句柄
engine = create_engine(SQLITE_URI, echo=True) # 操作数据句柄
Session = sessionmaker(bind=engine)  # 这里一定要用上下文去管理session,否则会出现很多诡异的情况！！！切记
session = scoped_session(Session)    # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
                                     # 内部会采用threading.local进行隔离

def add():
    trade_cal1 = models.Test(
        exchange='SSE',
        cal_date='20230416',
        is_open=1,
        pretrade_date='20230415')
    session.add(trade_cal1)
    session.commit()
    session.close()

def query():
    result = session.query(models.Test.cal_date, models.Test.exchange).all()
    print(pd.DataFrame(result))
    for i in result:
        print(i)
    session.close()

if __name__=='__main__':
    add()

