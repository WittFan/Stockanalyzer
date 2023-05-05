#  logging模块

主要参考：Python3，1行代码就输出日志文件，从此跟logging模块说拜拜https://blog.51cto.com/u_15910936/5932540

python 实现logging动态变更输出日志文件名https://www.jb51.net/article/207587.htm

重复打印问题https://blog.csdn.net/u011417820/article/details/112861970

python完美logging日志实现，按日期存储+解决多线程，可直接复制使用https://valuebai.github.io/2020/02/10/python%E5%AE%8C%E7%BE%8Elogging%E6%97%A5%E5%BF%97%E5%AE%9E%E7%8E%B0-%E6%8C%89%E6%97%A5%E6%9C%9F%E5%AD%98%E5%82%A8+%E8%A7%A3%E5%86%B3%E5%A4%9A%E7%BA%BF%E7%A8%8B-%E5%8F%AF%E7%9B%B4%E6%8E%A5%E5%A4%8D%E5%88%B6%E4%BD%BF%E7%94%A8/

## 日志等级

日志等级排序critical > error  > warning > info > debug

DEBUG：最详细的日志信息，典型应用场景是问题诊断。

INFO：记录关键节点信息，用于确认一切都是按照我们预想的那样工作。

WARNING：不期望发生的事情发生时记录的信息，程序还能正常运行，比如磁盘可用空间较低。

ERROR：某些功能不能正常运行时记录的信息。

CRITICAL：严重错误发生导致程序不能继续运行时记录的信息。

## 模块级别函数

### 创建日志记录

| 函数                                   | 说明                                 |
| -------------------------------------- | ------------------------------------ |
| logging.debug(msg, *args, **kwargs)    | 创建一条严重级别为DEBUG的日志记录    |
| logging.info(msg, *args, **kwargs)     | 创建一条严重级别为INFO的日志记录     |
| logging.warning(msg, *args, **kwargs)  | 创建一条严重级别为WARNING的日志记录  |
| logging.error(msg, *args, **kwargs)    | 创建一条严重级别为ERROR的日志记录    |
| logging.critical(msg, *args, **kwargs) | 创建一条严重级别为CRITICAL的日志记录 |
| logging.log(level, *args, **kwargs)    | 创建一条严重级别为level的日志记录    |
| logging.basicConfig(**kwargs)          | 对root logger进行一次性配置·         |

```python
import logging
logging.debug('Python debug')
logging.info('Python info')
logging.warning('Python warning')
logging.error('Python Error')
logging.critical('Python critical')
```

当指定一个日志级别之后，会记录大于或等于这个日志级别的日志信息，小于的将会被丢弃， 默认情况下日志打印只显示大于等于 WARNING 级别的日志。

### 基本配置 basicConfig

| 关键字   | 描述                                                         |
| -------- | ------------------------------------------------------------ |
| filename | 创建一个 FileHandler，使用指定的文件名，而不是使用 StreamHandler。 |
| filemode | 如果指明了文件名，指明打开文件的模式（如果没有指明 filemode，默认为 ‘a’）。 |
| format   | handler 使用指明的格式化字符串。                             |
| datefmt  | handler 使用指明的格式化字符串。                             |
| level    | 指明根 logger 的级别。                                       |
| stream   | 使用指明的流来初始化 StreamHandler。该参数与 ‘filename’ 不兼容，如果两个都有，‘stream’ 被忽略。 |

Logging.basicConfig() 需要在开头就设置，在中间设置并无作用

```python
logging.basicConfig(filename='./test.log', format='%(asctime)s  %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
logging.debug('This message should go to the logs file')
logging.info('So should this')
logging.warning('And this, too')
```

在脚本的目录，会生成 test.log文件

## 四大组件

| 组件名称 | 对应类名  | 功能描述                                                     |
| -------- | --------- | ------------------------------------------------------------ |
| 日志器   | Logger    | 暴露函数给应用程序，基于日志记录器和过滤器级别决定哪些日志有效 |
| 处理器   | Handler   | 将 logger 创建的日志记录发送到合适的目的输出                 |
| 过滤器   | Filter    | 提供了更细粒度的控制工具来决定输出哪条日志记录，丢弃哪条日志记录 |
| 格式器   | Formatter | 决定日志记录的最终输出格式                                   |

###日志器Logger

Logger是一个树形层级结构，在使用接口 debug，info，warn，error，critical 之前必须创建 Logger 实例：

```python
logger = logging.getLogger(logger_name)
```

创建Logger实例后，可以使用以下方法进行日志级别设置，增加处理器 Handler：

logger.setLevel(logging.ERROR) : 设置日志级别为 ERROR，即只有日志级别大于等于 ERROR 的日志才会输出；
logger.addHandler(handler_name) :为 Logger 实例增加一个处理器；

logger.removeHandler(handler_name) : 为 Logger 实例删除一个处理器；

### 处理器Handler

Handler 处理器类型有很多种，比较常用的有三个：StreamHandler，FileHandler，NullHandler
StreamHandler创建方法：

```python
ch = logging.StreamHandler(stream=None)
# 指定日志级别，低于WARN级别的日志将被忽略
ch.setLevel(logging.WARN) 
# 设置一个格式化器formatter
ch.setFormatter(formatter_name) 
# 增加一个过滤器，可以增加多个
ch.addFilter(filter_name) 
 # 删除一个过滤器
ch.removeFilter(filter_name)
```

创建 StreamHandler 之后，可以通过使用以下方法：设置日志级别，设置格式化器 Formatter，增加或删除过滤器 Filter：

### 过滤器 - Filter

Handlers 和 Loggers 可以使用 Filters 来完成比级别更复杂的过滤。Filter 基类只允许特定 Logger 层次以下的事件。创建方法

```python
filter = logging.Filter(name='')
```

### 格式器 - Formatter

使用Formatter对象设置日志信息最后的规则、结构和内容，默认的时间格式为%Y-%m-%d %H:%M:%S。
创建方法

```python
formatter = logging.Formatter(fmt=None, datefmt=None)
```

fmt 是消息的格式化字符串，datefmt 是日期字符串。

如果不指明 fmt，将使用 ‘%(message)s’ ;

如果不指明 datefmt，将使用 ISO8601 日期格式。

## 配置log文件

配置log文件,文件名称 logger.conf:

```python
[loggers]
keys=root,infoLogger

[logger_root]
level=DEBUG
handlers=consoleHandler,fileHandler

[logger_infoLogger]
handlers=consoleHandler,fileHandler
qualname=infoLogger
propagate=0

[handlers]
keys=consoleHandler,fileHandler


[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=form02
args=(sys.stderr,)
#args = (sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=INFO
formatter=form01
args=('../logs/testlog.logs', 'a')
[formatters]
keys=form01,form02

[formatter_form01]
format=%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s

[formatter_form02]
format=%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s
```

##  封装log方法

```python
# -*- coding:utf-8 -*-
# @Time   : 2021-10-21
# @Author : carl_DJ
 
import logging
import os.path
import time
 
 
class Logger(object):
 
    def __init__(self, logger_name):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        :param logger:
        """
        # 拼接日志文件夹，如果不存在则自动创建
        cur_path = os.path.dirname(os.path.realpath(__file__))
        log_path = os.path.join(os.path.dirname(cur_path), 'logs')
        if not os.path.exists(log_path):os.mkdir(log_path)
 
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
 
        # 创建一个handler，用于写入日志文件
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        # log_path = os.path.dirname(os.getcwd()) + '/Logs/'
        # log_name = log_path + rq + '.logs'
 
        log_name = os.path.join(log_path,'%s.logs ' %rq)
        fh = logging.FileHandler(log_name)
        fh.setLevel(logging.INFO)
 
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
 
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
 
        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
 
    def getlog(self):
        return self.logger
```

调用log

```python
import time
from selenium import webdriver
from autoFramewrok.utils.log import Logger
logger  = Logger(logger_name='TestMylog').getlog()
class TestMylog(object):
    def print_log(self):
        driver = webdriver.Chrome()
        # logger.info("打开浏览器")
        driver.maximize_window()
        logger.info("最大化浏览器窗口。")
        driver.implicitly_wait(8)
        driver.get("https://www.baidu.com")
        logger.info("打开百度首页。")
        time.sleep(1)
        logger.info("暂停一秒。")
        driver.quit()
        logger.info("关闭并退出浏览器。")
testlog = TestMylog()
testlog.print_log()
```







