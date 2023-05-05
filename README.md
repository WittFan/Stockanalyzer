# Stockanalyser
该项目用于分析上市公司及股票价格，辅助选股。

## Quick Start

### 1.修改配置文件config.py

从GitHub.com下载代码，配置python环境，依据requirements.txt安装包就不在这里说了，可以通过百度获取相关知识，代码环境就绪后：

将config_default.py文件名改为config.py。

修改tushare_token，供tushare接口函数配置参数，通过tushare接口可以调用股票数据；若没有tushare的token，请到https://tushare.pro/注册账号，购买积分，我最开始购买了200元（2000积分），根据官网介绍文档了解积分权限和接口参数。

默认计算机的核心数是4，设置线程数时会使用。通过如下代码获取系统cpu核心数。

```python
cpu_count = os.cpu_count()
```

### 2.注册数据库及表

运行shell命令

```shell
python models/register.py
```

若需要删除表，将代码改成如下：

```python
session = scoped_session(Session)    # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
                                     # 内部会采用threading.local进行隔离
Base.metadata.drop_all(engine)       # 删除表
Base.metadata.create_all(engine)     # 创建表
```

### 3.下载tushare数据

运行shell命令

```python
python pull_tushare/main.py
```

可以修改列表中的类名，选择需要下载的表。例如月度基本信息列表tushare_api_monthly_basics中的IndexBasicTushare。

```python
tushare_api_monthly_basics = [IndexBasicTushare, StockBasicTushare, IndexClassifyTushare]
```

要想了解表的信息，可以查看models/table_models，比如，IndexBasicTushare对应的表index_basic在index.py文件里。

```python
# models/table_models/index.py
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
```

### 4.增删改查数据

通过如下代码查询数据，更多增删改查功能参考models/api.py。

```python
from models.table_models import *
# 按条件查询数据
query_magic = session.query(Test.id, Test.cal_date).filter(Test.id > 0).filter(Test.exchange=='SSE')
df = data_api.query(query_magic)
print(df)
# 查询整个表
query_magic = session.query(TradeCal)
df = data_api.query(query_magic)
print(df)
```

## Models(table models)



## Pull Tushare (pull data from tussore)

更新判断条件

## Utils



## Stragegy1-big_data_invest





