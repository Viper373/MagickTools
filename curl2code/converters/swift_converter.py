# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :swift_converter.py
# @Time      :2024/9/25 下午4:20
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class SwiftConverter(CurlConverterBase):
    def __init__(self):
        super().__init__(language='swift')
