# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :cfml_converter.py
# @Time      :2024/9/25 下午3:45
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class CFMLConverter(CurlConverterBase):
    def __init__(self):
        super().__init__(language='cfml')
