""" 注册的sqlAlchemy ORM表主要是股票基本信息"""
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

class StockBasic(Base):
    __tablename__ = "stock_basic"
    ts_code = Column(String, primary_key=True, comment='TS代码')
    symbol = Column(String, comment='股票代码')
    name = Column(String, index=True, comment='股票名称')
    area = Column(String, comment='地域')
    industry = Column(String, comment='所属行业')
    fullname = Column(String, comment='股票全称')
    enname = Column(String, comment='英文全称')
    cnspell = Column(String, comment='拼音缩写')
    market = Column(String, index=True, comment='市场类型')
    exchange = Column(String, index=True, comment='交易所代码')
    curr_type = Column(String, comment='交易货币')
    list_status = Column(String, index=True, comment='上市状态 L上市 D退市 P暂停上市')
    list_date = Column(DateTime, comment='上市日期')
    delist_date = Column(DateTime, comment='退市日期')
    is_hs = Column(String, index=True, comment='是否沪深港通标的，N否 H沪股通 S深股通')

class Namechange(Base):
    __tablename__ = "namechange"
    ts_code = Column(String, primary_key=True, comment='TS代码')
    name = Column(String, comment='证券名称')
    start_date = Column(DateTime, index=True, comment='开始日期')
    end_date = Column(DateTime, index=True, comment='结束日期')
    ann_date = Column(DateTime, comment='公告日期')
    change_reason = Column(String, comment='变更原因')

class HsConst(Base):
    __tablename__ = "hs_const"
    ts_code = Column(String, primary_key=True, comment='TS代码')
    hs_type = Column(String, index=True, comment='沪深港通类型SH沪SZ深')
    in_date = Column(DateTime, comment='纳入日期')
    out_date = Column(DateTime, comment='剔除日期')
    is_new = Column(String, index=True, comment='是否最新')

class StockCompany(Base):
    __tablename__ = "stock_company"
    ts_code = Column(String, primary_key=True, comment='股票代码')
    exchange = Column(String, index=True, comment='交易所代码SSE上交所 SZSE深交所')
    chairman = Column(String, comment='法人代表')
    manager = Column(String, comment='总经理')
    secretary = Column(String, comment='董秘')
    reg_capital = Column(Float, comment='注册资本')
    setup_date = Column(DateTime, comment='注册日期')
    province = Column(String, comment='所在省份')
    city = Column(String, comment='所在城市')
    introduction = Column(String, comment='公司介绍')
    website = Column(String, comment='公司主页')
    email = Column(String, comment='电子邮件')
    office = Column(String, comment='办公室')
    ann_date = Column(DateTime, comment='公告日期')
    business_scope = Column(String, comment='经营范围')
    employees = Column(Integer, comment='员工人数')
    main_business = Column(String, comment='主要业务及产品')