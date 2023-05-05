"""
数据库的模型，模型使用sqlalchemy的ORM方法，面向对象的关系映射。
"""
from sqlalchemy.ext.declarative import declarative_base

# 定义sqlalchemy包ORM表的基类，其他文件的model继承
Base = declarative_base()

