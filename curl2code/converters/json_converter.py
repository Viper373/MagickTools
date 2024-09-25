# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :json_converter.py
# @Time      :2024/9/24 下午5:28
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class JSONConverter(CurlConverterBase):
    def __init__(self):
        super().__init__(language='json')
