# -*- coding:utf-8 -*-
# @Project   :dir2zip
# @FileName  :config_utils.py
# @Time      :2024/8/30 上午10:28
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import logging
from configparser import ConfigParser


def load_config(config_file):
    """加载配置文件"""
    config_parser = ConfigParser()
    config_parser.read(config_file)
    return config_parser["default"]


def get_compression_format(user_input, config):
    """获取压缩格式"""
    if not user_input:
        compression_format = config.get("format", "zip")
        logging.info(f"未输入格式，使用默认格式: {compression_format}")
    else:
        compression_format = user_input
        logging.info(f"用户输入格式: {compression_format}")
    return compression_format
