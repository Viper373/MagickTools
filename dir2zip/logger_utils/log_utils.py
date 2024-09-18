# -*- coding:utf-8 -*-
# @Project   :dir2zip
# @FileName  :log_utils.py
# @Time      :2024/8/30 上午10:56
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import logging
import colorlog


def setup_logging():
    """设置日志配置，支持颜色输出"""
    log_colors = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }

    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors=log_colors
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("logs/compression.log", mode='a', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    ))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler]
    )
