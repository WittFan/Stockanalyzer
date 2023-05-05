""" 注册的sqlAlchemy ORM表主要是指数相关"""
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

class IndexBasic(Base):
    __tablename__ = "index_basic"
    ts_code = Column(String, primary_key=True, comment='TS代码')
    name = Column(String, index=True, comment='简称')
    fullname = Column(String, comment='指数全称')
    market = Column(String, index=True, comment='市场')
    publisher = Column(String, index=True, comment='发布方')
    index_type = Column(String, comment='指数风格')
    category = Column(String, index=True, comment='指数类别')
    base_date = Column(String, comment='基期')
    base_point = Column(Float, comment='基点')
    list_date = Column(DateTime, comment='发布日期')
    weight_rule = Column(String, comment='加权方式')
    desc = Column(String, comment='描述')
    exp_date = Column(DateTime, comment='终止日期')


class IndexDaily(Base):
    __tablename__ = "index_daily"
    ts_code_trade_date = Column(String, primary_key=True)
    ts_code = Column(String, index=True, comment='None')
    trade_date = Column(DateTime, index=True, comment='None')
    close = Column(Float, comment='None')
    open = Column(Float, comment='None')
    high = Column(Float, comment='None')
    low = Column(Float, comment='None')
    pre_close = Column(Float, comment='None')
    change = Column(Float, comment='None')
    pct_chg = Column(Float, comment='None')
    vol = Column(Float, comment='None')
    amount = Column(Float, comment='None')

class IndexDailybasic(Base):
    __tablename__ = "index_dailybasic"
    ts_code_trade_date = Column(String, primary_key=True)
    ts_code = Column(String, index=True, comment='TS代码')
    trade_date = Column(DateTime, index=True, comment='交易日期')
    total_mv = Column(Float, comment='当日总市值')
    float_mv = Column(Float, comment='当日流通市值')
    total_share = Column(Float, comment='当日总股本')
    float_share = Column(Float, comment='当日流通股本')
    free_share = Column(Float, comment='当日自由流通股本')
    turnover_rate = Column(Float, comment='换手率')
    turnover_rate_f = Column(Float, comment='换手率(自由流通股本)')
    pe = Column(Float, comment='市盈率')
    pe_ttm = Column(Float, comment='市盈率TTM')
    pb = Column(Float, comment='市净率')

class IndexClassify(Base):
    """申万行业分类index_classify"""
    __tablename__ = "index_classify"
    index_code = Column(String, index=True, primary_key=True, comment='指数代码')
    industry_name = Column(String, comment='行业名称')
    level = Column(String, index=True, comment='行业名称')
    industry_code = Column(String, comment='行业代码')
    is_pub = Column(String, comment='是否发布指数')
    parent_code = Column(String, index=True, comment='父级代码')
    src = Column(String, index=True, comment='行业分类（SW申万）')

class IndexMember(Base):
    """申万行业成分构成index_member"""
    __tablename__ = "index_member"
    index_code_con_code_in_date = Column(String, primary_key=True, comment='指数代码+成分股票代码+纳入日期')
    index_code = Column(String, index=True, comment='指数代码')
    index_name = Column(String, comment='指数名称')
    con_code = Column(String, comment='成分股票代码')
    con_name = Column(String, comment='成分股票名称')
    in_date = Column(DateTime, comment='纳入日期')
    out_date = Column(DateTime, comment='剔除日期')
    is_new = Column(String, index=True, comment='是否最新Y是N否')

