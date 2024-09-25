# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :go_converter.py
# @Time      :2024/9/24 下午5:14
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class GoConverter(CurlConverterBase):
    def __init__(self):
        super().__init__(language='go')
