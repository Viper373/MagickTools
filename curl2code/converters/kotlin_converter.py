# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :kotlin_converter.py
# @Time      :2024/9/25 下午4:14
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class KotlinConverter(CurlConverterBase):
    def __init__(self):
        super().__init__(language='kotlin')
