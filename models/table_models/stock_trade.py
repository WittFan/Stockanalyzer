""" 注册的sqlAlchemy ORM表主要是股票交易信息"""
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

class Daily(Base):
    __tablename__ = "daily"
    ts_code_trade_date = Column(String, primary_key=True)
    ts_code = Column(String, index=True, comment='股票代码')
    trade_date = Column(DateTime, index=True, comment='交易日期')
    open = Column(Float, comment='开盘价')
    high = Column(Float, comment='最高价')
    low = Column(Float, comment='最低价')
    close = Column(Float, comment='收盘价')
    pre_close = Column(Float, comment='昨收价')
    change = Column(Float, comment='涨跌额')
    pct_chg = Column(Float, comment='涨跌幅')
    vol = Column(Float, comment='成交量')
    amount = Column(Float, comment='成交额')

class Weekly(Base):
    __tablename__ = "weekly"
    ts_code_trade_date = Column(String, primary_key=True)
    ts_code = Column(String, index=True, comment='')
    trade_date = Column(DateTime, index=True, comment='')
    close = Column(Float, comment='')
    open = Column(Float, comment='')
    high = Column(Float, comment='')
    low = Column(Float, comment='')
    pre_close = Column(Float, comment='')
    change = Column(Float, comment='')
    pct_chg = Column(Float, comment='')
    vol = Column(Float, comment='')
    amount = Column(Float, comment='')

class Monthly(Base):
    __tablename__ = "monthly"
    ts_code_trade_date = Column(String, primary_key=True)
    ts_code = Column(String, index=True, comment='')
    trade_date = Column(DateTime, index=True, comment='')
    close = Column(Float, comment='')
    open = Column(Float, comment='')
    high = Column(Float, comment='')
    low = Column(Float, comment='')
    pre_close = Column(Float, comment='')
    change = Column(Float, comment='')
    pct_chg = Column(Float, comment='')
    vol = Column(Float, comment='')
    amount = Column(Float, comment='')

class AdjFactor(Base):
    __tablename__ = "adj_factor"
    ts_code_trade_date = Column(String, primary_key=True)
    ts_code = Column(String, index=True, comment='股票代码')
    trade_date = Column(DateTime, index=True, comment='交易日期')
    adj_factor = Column(Float, comment='复权因子')

class DailyBasic(Base):
    __tablename__ = "daily_basic"
    ts_code_trade_date = Column(String, primary_key=True)
    ts_code = Column(String, index=True, comment='TS股票代码')
    trade_date = Column(DateTime, index=True, comment='交易日期')
    close = Column(Float, comment='当日收盘价')
    turnover_rate = Column(Float, comment='换手率')
    turnover_rate_f = Column(Float, comment='换手率(自由流通股)')
    volume_ratio = Column(Float, comment='量比')
    pe = Column(Float, comment='市盈率（总市值/净利润）')
    pe_ttm = Column(Float, comment='市盈率（TTM）')
    pb = Column(Float, comment='市净率（总市值/净资产）')
    ps = Column(Float, comment='市销率')
    ps_ttm = Column(Float, comment='市销率（TTM）')
    dv_ratio = Column(Float, comment='股息率（%）')
    dv_ttm = Column(Float, comment='股息率（TTM） （%）')
    total_share = Column(Float, comment='总股本')
    float_share = Column(Float, comment='流通股本')
    free_share = Column(Float, comment='自由流通股本')
    total_mv = Column(Float, comment='总市值')
    circ_mv = Column(Float, comment='流通市值')
    limit_status = Column(Integer, comment='涨跌停状态')

class StockMx(Base):
    __tablename__ = "stock_mx"
    ts_code_trade_date = Column(String, primary_key=True)
    ts_code = Column(String, index=True, comment='TS股票代码')
    trade_date = Column(DateTime, index=True, comment='交易日期')
    mx_grade = Column(Integer, comment='动能评级，综合动能指标后分成4个评等，1(高)、2(中)、3(低)、4(弱)。高：周、月、季、半年趋势方向一致，整体看多；中：周、月、季、半年趋势方向不一致，但整体偏多；低：周、月、季、半年趋势方向不一致，但整体偏多；弱：周、月、季、半年趋势方向一致，整体看空')
    com_stock = Column(String, comment='行业轮动指标')
    evd_v = Column(String, comment='速度指标，衡量该个股股价变化的速度')
    zt_sum_z = Column(String, comment='极值，短期均线离差值')
    wma250_z = Column(String, comment='偏离指标，中期均线偏离度指标')

class StockVx(Base):
    __tablename__ = "stock_vx"
    ts_code_trade_date = Column(String, primary_key=True)
    ts_code = Column(String, index=True, comment='TS股票代码')
    trade_date = Column(DateTime, index=True, comment='交易日期')
    level1 = Column(String, index=True, comment='4评级：1(便宜)、2(合理)、3(贵)、4(很贵)')
    level2 = Column(String, index=True, comment='8评级：1,2(便宜)、3,4(合理)、5,6(贵)、7,8(很贵)')
    vx_life_v_l4 = Column(String, index=True, comment='估值长优4条线，根据level1的评级，公司上市后每一天的估值评级平均')
    vx_3excellent_v_l4 = Column(String, index=True, comment='估值3优4条线，根据level1的评级，最新季度的估值评级、近5季度的估值评级平均、上市后的估值评级平均，短中长的估值评级再取一次平均形成三优指标')
    vx_past_5q_avg_l4 = Column(String, index=True, comment='估值4条线近5季平均，根据level1的评级，最近五季度估值评级平均')
    vx_grow_worse_v_l4 = Column(String, index=True, comment='估值进退步-估值4条线,根据level1的评级，最新的估值评级与最近5Q平均的比')
    vx_life_v_l8 = Column(String, index=True, comment='估值长优8条线,根据level2的评级，公司上市后每一季度的估值评级平均')
    vx_3excellent_v_l8 = Column(String, index=True, comment='估值3优8条线,根据level2的评级，最新季度的估值评级、近5季度的估值评级平均、上市后的估值评级平均，短中长的估值评级再取一次平均形成三优指标')
    vx_past_5q_avg_l8 = Column(String, index=True, comment='估值8条线近5季平均,根据level2的评级，最近五季度估值评级平均')
    vx_grow_worse_v_l8 = Column(String, index=True, comment='估值进退步-估值8条线,根据level2的评级，最新的估值评级与最近5Q平均的比较')
    vxx = Column(String, index=True, comment='个股最新估值与亚洲同类股票相较后的标准差，按因子排序，数值越大代表估值越贵')
    vs = Column(String, index=True, comment='个股最新估值与亚洲同类股票自己相较后的标准差，按因子排序，数值越大代表估值越贵')
    vz11 = Column(String, index=True, comment='个股最新估值与亚洲同类股票主行业相较后的标准差，按因子排序，数值越大代表估值越贵')
    vz24 = Column(String, index=True, comment='个股最新估值与亚洲同类股票次行业相较后的标准差，按因子排序，数值越大代表估值越贵')
    vz_lms = Column(String, index=True, comment='个股最新估值与亚洲同类股票市值分类相较后的标准差，按因子排序，数值越大代表估值越贵')

class StkHoldertrade(Base):
    __tablename__ = "stk_holdertrade"
    ts_code_ann_date = Column(String, primary_key=True)
    ts_code = Column(String, index=True, comment='TS股票代码')
    ann_date = Column(DateTime, index=True, comment='公告日期')
    holder_name = Column(String, index=True, comment='股东名称')
    holder_type = Column(String, comment='股东类型G高管P个人C公司')
    in_de = Column(String, comment='类型IN增持DE减持')
    change_vol = Column(Float, comment='变动数量')
    change_ratio = Column(Float, comment='占流通比例（%）')
    after_share = Column(Float, comment='变动后持股')
    after_ratio = Column(Float, comment='变动后占流通比例（%）')
    avg_price = Column(Float, comment='平均价格')
    total_share = Column(Float, comment='持股总数')
    begin_date = Column(String, comment='增减持开始日期')
    close_date = Column(String, comment='增减持结束日期')

class StkFactor(Base):
    __tablename__ = "stk_factor"
    ts_code_trade_date = Column(String, primary_key=True)
    ts_code = Column(String, index=True, comment='TS股票代码')
    trade_date = Column(DateTime, index=True, comment='交易日期')
    close = Column(Float, comment='收盘价')
    open = Column(Float, comment='开盘价')
    high = Column(Float, comment='最高价')
    low = Column(Float, comment='最低价')
    pre_close = Column(Float, comment='昨收价')
    change = Column(Float, comment='涨跌额')
    pct_change = Column(Float, comment='涨跌幅')
    vol = Column(Float, comment='成交量（手）')
    amount = Column(Float, comment='成交额 （千元）')
    adj_factor = Column(Float, comment='复权因子')
    open_hfq = Column(Float, comment='开盘价后复权')
    open_qfq = Column(Float, comment='开盘价前复权')
    close_hfq = Column(Float, comment='收盘价后复权')
    close_qfq = Column(Float, comment='收盘价前复权')
    high_hfq = Column(Float, comment='最高价后复权')
    high_qfq = Column(Float, comment='最高价前复权')
    low_hfq = Column(Float, comment='最低价后复权')
    low_qfq = Column(Float, comment='最低价前复权')
    pre_close_hfq = Column(Float, comment='昨收价后复权')
    pre_close_qfq = Column(Float, comment='昨收价前复权')
    macd_dif = Column(Float, comment='MCAD_DIF (基于前复权价格计算，下同)')
    macd_dea = Column(Float, comment='MCAD_DEA')
    macd = Column(Float, comment='')
    kdj_k = Column(Float, comment='')
    kdj_d = Column(Float, comment='')
    kdj_j = Column(Float, comment='')
    rsi_6 = Column(Float, comment='')
    rsi_12 = Column(Float, comment='')
    rsi_24 = Column(Float, comment='')
    boll_upper = Column(Float, comment='')
    boll_mid = Column(Float, comment='')
    boll_lower = Column(Float, comment='')
    cci = Column(Float, comment='')