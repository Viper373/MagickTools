# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :har_converter.py
# @Time      :2024/9/25 下午4:11
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class HARConverter(CurlConverterBase):
    def __init__(self):
        super().__init__(language='har')
