# -*- coding:utf-8 -*-
# 封装log方法
import logging
import os.path
import time


class LoggerTushare(object):
    def __init__(self, logger_name):
        """
        logger_name 为tushare数据下载包的类名
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        :param logger:
        """
        # 拼接日志文件夹，如果不存在则自动创建
        cur_path = os.path.dirname(os.path.realpath(__file__))
        log_path = os.path.join(os.path.dirname(cur_path), 'logs')
        table_log_path = os.path.join(log_path, 'table_logs')
        date_log_path = os.path.join(log_path, 'date_logs')
        if not os.path.exists(table_log_path):
            os.mkdir(table_log_path)
        if not os.path.exists(date_log_path):
            os.mkdir(date_log_path)

        # 创建一个logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件。日志文件按照日期
        datetime_string = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        log_name = os.path.join(date_log_path, '%s.log ' % datetime_string)
        file_handler_by_datetime = logging.FileHandler(log_name)
        file_handler_by_datetime.setLevel(logging.INFO)

        # 创建一个handler，用于写入日志文件。日志文件按照logger_name
        log_name = os.path.join(table_log_path, '%s.log ' % logger_name)
        file_handler_by_class = logging.FileHandler(log_name)
        file_handler_by_class.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler_by_datetime.setFormatter(formatter)
        file_handler_by_class.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(file_handler_by_datetime)
        self.logger.addHandler(file_handler_by_class)
        # self.logger.addHandler(console_handler)


if __name__ == '__main__':
    logger = LoggerTushare('log_name').logger
    logger.info('test')
