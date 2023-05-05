"""
数据库的模型，模型使用sqlalchemy的ORM方法，面向对象的关系映射。
"""
from models.table_models import *  # 导入所有table model
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from config import SQLITE_URI
"""
Sqlite连接：注意注意注意：这个URI连接的相对地址，指的是相对于最外层调用的文件的相对位置，而不是此文件的相对位置。所以最好是使用绝对路径。
"""
engine = create_engine(SQLITE_URI, echo=True) # 操作数据句柄
Session = sessionmaker(bind=engine)  # 这里一定要用上下文去管理session,否则会出现很多诡异的情况！！！切记
session = scoped_session(Session)    # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
                                     # 内部会采用threading.local进行隔离

# Base.metadata.drop_all(engine)     # 删除表
Base.metadata.create_all(engine)     # 创建表