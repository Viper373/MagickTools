# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :clojure_converter.py
# @Time      :2024/9/25 下午3:46
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class ClojureConverter(CurlConverterBase):
    def __init__(self):
        super().__init__(language='clojure')
