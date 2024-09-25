# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :dart_converter.py
# @Time      :2024/9/24 下午5:18
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class DartConverter(CurlConverterBase):
    def __init__(self):
        super().__init__(language='dart')
