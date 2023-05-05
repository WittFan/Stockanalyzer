""" 注册的sqlAlchemy ORM表主要是股票报表"""
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

class TushareStkRewards(Base):
    __tablename__ = "tushare_stk_rewards"
    ts_code_ann_date = Column(String, primary_key=True)
    ts_code = Column(String, index=True, comment='TS股票代码')
    ann_date = Column(DateTime, comment='公告日期')
    end_date = Column(DateTime, index=True, comment='报告期')
    name = Column(String, comment='姓名')
    title = Column(String, comment='职务')
    reward = Column(Float, comment='报酬')
    hold_vol = Column(Float, comment='持股数')