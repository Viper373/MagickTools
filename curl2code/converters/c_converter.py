# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :c_converter.py
# @Time      :2024/9/25 下午3:45
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class CConverter(CurlConverterBase):
    def __init__(self):
        super().__init__(language='c')
