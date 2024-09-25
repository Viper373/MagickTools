# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :httpie_converter.py
# @Time      :2024/9/25 下午4:12
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class HTTPieConverter(CurlConverterBase):
    def __init__(self):
        super().__init__(language='httpie')
