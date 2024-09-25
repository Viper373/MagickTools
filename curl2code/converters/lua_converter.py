# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :lua_converter.py
# @Time      :2024/9/25 下午4:15
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class LuaConverter(CurlConverterBase):
    def __init__(self):
        super().__init__(language='lua')
