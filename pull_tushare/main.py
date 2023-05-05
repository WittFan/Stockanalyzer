import datetime
from concurrent.futures import ThreadPoolExecutor
import sys

sys.path.append('.')

from pull_tushare.tushare_tables import *
from config import cpu_count
from utils.logger import LoggerTushare

logger = LoggerTushare('pull_tushare_main').logger


def manual_start():
    """ 手动更新所有tushare数据（非定时任务）"""
    ###### 一、基础信息更新
    logger.info(' 1.基础信息更新频率：年')
    tushare_api_yearly_basics = [TradeCalTushare]  # 年度日历
    for tushare_api_object in tushare_api_yearly_basics:
        tushare_api_object().pull()

    logger.info(' 2.基础信息更新频率：月')
    tushare_api_monthly_basics = [IndexBasicTushare, StockBasicTushare, IndexClassifyTushare]
    # 指数基本信息、股票基本信息、申万行业分类、
    for tushare_api_object in tushare_api_monthly_basics:
        tushare_api_object().pull()  # pull条件：上次更新到n月，过了n+1月25日就每日尝试更新

    # 3.更新频率：周
    week_list = []
    # 建立一个线程池，遍历week_list
    # 设置pull条件：1、取下列表的数据日期，上次更新到第n周最后一日。2、是否过了第n+1周最后一个交易日，如果过了就更新

    ###### 二、明细数据更新：要建线程池
    # 4.更新频率：月、周、日
    logger.info(' 4.详细信息更新频率：日')
    detail_list = [IndexMemberTushare]  # 月更新
    detail_list += [DaylyTushare, DaylyBasicTushare, AdjFactorTushare]  # 日更新

    ## 多线程
    def action(param):
        try:
            param().pull()
            logger.info(f'线程{param}成功结束')
        except Exception as e:
            logger.error(f'线程{param}遇到错误{e}')

    with ThreadPoolExecutor(max_workers=cpu_count * 2) as pool:
        # with语句会调用executor.shutdown(wait=True)，在所有线程都执行完毕前阻塞当前线程
        # 返回一个生成器，遍历的结果为0,1,2,3。无论执行结果先后顺序如何，看输入的iterator顺序
        # 因为线程池为3，所以0~2进池，其中某个执行完后，3进池
        pool.map(action, detail_list)


if __name__ == "__main__":
    manual_start()
