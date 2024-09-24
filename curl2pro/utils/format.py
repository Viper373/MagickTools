# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :format.py
# @Time      :2024/9/24 下午5:39
# @Author    :Zhangjinzhao
# @Software  :PyCharm

def truncate_string(s, max_length=30):
    if len(s) > max_length:
        return f"{s[:max_length // 2]}...{s[-max_length // 2:]}"
    return s
