import os
import platform
import tushare as ts


""" 配置数据模型及数据库的属性 """
# 获取当前文件的绝对路径，改成数据库路径
SQLITE_URI = None
if str(platform.system().lower()) == 'windows':
    path = os.path.dirname(__file__)
    SQLITE_URI = fr'sqlite:///{path}\data\fast.db''?check_same_thread=False'
    # print(f'数据库路径：{SQLITE_URI}')
elif str(platform.system().lower()) == 'linux' or 'darwin':
    path = os.path.dirname(__file__)
    SQLITE_URI = fr'sqlite:///{path}/data/fast.db''?check_same_thread=False'
    # print(f'数据库路径：{SQLITE_URI}')
else:
    pass
    # print(f"未知系统：{platform.system().lower()}")

tushare_token = '*****65481***********************************'
ts.set_token(tushare_token)
tushare_api = ts.pro_api()

cpu_count = 4
# 获取系统cpu核心数
# cpu_count = os.cpu_count()


if __name__=="__main__":
    pass