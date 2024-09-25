# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :elixir_converter.py
# @Time      :2024/9/25 下午4:11
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class ElixirConverter(CurlConverterBase):
    def __init__(self):
        super().__init__(language='elixir')
