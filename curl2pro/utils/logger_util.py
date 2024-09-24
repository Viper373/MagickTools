# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :logger_util.py
# @Time      :2024/9/24 下午5:44
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import logging
from rich.console import Console
from rich.logging import RichHandler


class LoggerSetup:
    """
    日志配置类，用于统一配置和获取日志记录器。
    """

    def __init__(self, logger_name: str):
        """
        初始化日志记录器。

        :param logger_name: 日志记录器的名称
        """
        self.console = Console()
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)  # 设置为 INFO 或 DEBUG

        # 创建并配置 RichHandler
        self.rich_handler = RichHandler(console=self.console, markup=True, show_path=False)
        self.rich_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s", datefmt="[%X]")
        self.rich_handler.setFormatter(formatter)

        # 清除自定义日志器的默认处理器（如果有）
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 将 RichHandler 添加到自定义日志器
        self.logger.addHandler(self.rich_handler)

        # 确保自定义日志器不将日志传播到根日志器，避免重复输出
        self.logger.propagate = False

    def get_logger(self) -> logging.Logger:
        """
        获取配置好的日志记录器。

        :return: 配置好的日志记录器
        """
        return self.logger
