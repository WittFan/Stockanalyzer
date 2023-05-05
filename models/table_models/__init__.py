"""
   SqlAichemy ORM数据模型
"""

# table models模块
# 将各个文件下（exchange_info.py 等）的table model导入__init__.py，导入models模块后可以直接使用这些table model
from models.table_models.exchange_info import *
from models.table_models.foreign_currency import *
from models.table_models.index import *
from models.table_models.reports import *
from models.table_models.stock_info import *
from models.table_models.stock_trade import *
from models.table_models.update_info import *
