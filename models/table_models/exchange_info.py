""" 注册的sqlAlchemy ORM表主要是交易所相关的表，还有日历相关的"""
from models.base import Base  # 多个model继承同一个Base
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

class Test(Base):
    """交易日历表"""
    __tablename__ = "test"
    id = Column(Integer, primary_key=True, autoincrement=True)
    exchange = Column(String, index=True, comment='交易所 SSE上交所 SZSE深交所')
    cal_date = Column(DateTime, index=True, comment='日历日期')
    is_open = Column(String, index=True, comment='是否交易 0休市 1交易')
    pretrade_date = Column(DateTime, comment='上一个交易日')

class TradeCal(Base):
    """交易日历表"""
    __tablename__ = "trade_cal"
    exchange_cal_date = Column(String, primary_key=True, comment='唯一标识')
    id = Column(Integer, autoincrement=True)
    exchange = Column(String, index=True, comment='交易所 SSE上交所 SZSE深交所')
    cal_date = Column(DateTime, index=True, comment='日历日期')
    is_open = Column(String, index=True, comment='是否交易 0休市 1交易')
    pretrade_date = Column(DateTime, comment='上一个交易日')

class TradeWeek(Base):
    __tablename__ = "trade_week"
    id = Column(Integer, primary_key=True, autoincrement=True)
    exchange = Column(String, index=True, comment='交易所 SSE上交所 SZSE深交所')
    cal_date = Column(DateTime, index=True, comment='每周交易日期')
    pretrade_date = Column(DateTime, comment='上一个周最后一个交易日')

class TradeMonth(Base):
    __tablename__ = "trade_month"
    id = Column(Integer, primary_key=True, autoincrement=True)
    exchange = Column(String, index=True, comment='交易所 SSE上交所 SZSE深交所')
    cal_date = Column(DateTime, index=True, comment='每月交易日期')
    pretrade_date = Column(DateTime, comment='上一个月最后一个交易日')