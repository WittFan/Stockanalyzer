""" 注册的sqlAlchemy ORM表主要是外汇相关"""
from models.base import Base # 多个model继承同一个Base
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Float,
    String,
    Enum,
    DECIMAL,
    DateTime,
    Boolean,
    UniqueConstraint,
    Index
)

class FxObasic(Base):
    __tablename__ = "fx_obasic"
    ts_code = Column(String, primary_key=True, comment='外汇代码')
    name = Column(String, index=True, comment='名称')
    classify = Column(String, comment='分类')
    exchange = Column(String, comment='交易商')
    min_unit = Column(Float,  comment='最小交易单位')
    max_unit = Column(Float,  comment='最大交易单位')
    pip = Column(Float,  comment='点')
    pip_cost = Column(Float,  comment='点值')
    traget_spread = Column(Float,  comment='目标差价')
    min_stop_distance = Column(Float,  comment='最小止损距离（点子）')
    trading_hours = Column(Float,  comment='交易时间')
    break_time = Column(Float,  comment='休市时间')

class FxDaily(Base):
    __tablename__ = "fx_daily"
    ts_code_trade_date = Column(String, primary_key=True)
    ts_code = Column(String, comment='外汇代码')
    trade_date = Column(DateTime, index=True, comment='交易日期')
    bid_open = Column(Float,  comment='买入开盘价')
    bid_close = Column(Float,  comment='买入收盘价')
    bid_high = Column(Float,  comment='买入最高价')
    bid_low = Column(Float,  comment='买入最低价')
    ask_open = Column(Float,  comment='卖出开盘价')
    ask_close = Column(Float,  comment='卖出收盘价')
    ask_high = Column(Float,  comment='卖出最高价')
    ask_low = Column(Float,  comment='卖出最低价')
    tick_qty = Column(Integer, index=True, comment='报价笔数')
    exchange = Column(String, index=True, comment='交易商')