# sqlalchemy的使用

##sqlalchemy 可以导入的包

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
```

## 增加

```python
engine = create_engine(SQLITE_URI, echo=False)  # 操作数据句柄
dataframe.to_sql(table_name, engine, if_exists='append', index=False)
```

## 删除数据

1、 普通的删除操作：

```python
# 1: 实例化session
session = Session(engine)
# 2:先进行查询操作
session.execute(delete(User).where(User.name == "梁山"))
# 3：提交与关闭
session.commit()
session.close()
```

2、基于查询进行删除（测试使用不了）

```python
# 1: 实例化session
session = Session(engine)
# 2:先进行查询操作
user = session.query(User).filter(User.name == "梁山").first()
session.delete(user)
# 3：提交与关闭
session.commit()
session.close()
```

## 删除表

调用`drop()`表对象，使用给定的Connectable进行连接，为此Table发出DROP语句。

```cobol
User.__table__.drop()
```

## 更新

1、普通的更新操作

```python
# 进行更新操作
session.execute(update(User).where(User.name == "梁山").values(name="王老五"))
# 提交与关闭
session.commit()
session.close()
```

2、基于查询更新

```python
# 1: 实例化session
session = Session(engine)
# 2:先进行查询操作
user = session.query(User).filter(User.name == "王老五").first()
user.name = "梁山"
# 3：提交与关闭
session.commit()
session.close()
```

## 查询

将model读取的数据转为pandas.dataframe

```python
engine = create_engine(SQLITE_URI, echo=True)
Session = sessionmaker(bind=engine)  # 这里一定要用上下文去管理session,否则会出现很多诡异的情况！！！切记
session = Session(engine)
query = session.query(MyTable).filter(MyTable.age > 21)
df = pd.read_sql(query.statement, query.session.bind)
session.close()
```
封装部分代码
```python
def query(self, query_magic):
    """用 sqlAlchemy 的 session.query 查询数据库，结合pandas.read_sql"""
    df = pd.read_sql(query_magic.statement, query_magic.session.bind)
    session.close()
    return df
# 查询数据
query_magic = session.query(Test).filter(Test.id > 1).filter(Test.exchange=='SSE')
df = query(query_magic)
```

## 原生sql

```python
def sql(sql_str):
    data = session.execute(sql_str)
    session.close()
    df = pd.DataFrame(data)
    return df
```