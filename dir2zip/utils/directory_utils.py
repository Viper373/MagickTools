# -*- coding:utf-8 -*-
# @Project   :dir2zip
# @FileName  :directory_utils.py
# @Time      :2024/8/30 上午10:28
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import os
import logging


def create_directory_if_not_exists(directory_path):
    """检查并创建目录，如果不存在则创建"""
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            logging.info(f"目录 {directory_path} 不存在，已创建。")
        except OSError as e:
            logging.error(f"创建目录 {directory_path} 时发生错误: {e}")
            raise
