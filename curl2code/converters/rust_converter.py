# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :rust_converter.py
# @Time      :2024/9/24 下午5:26
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class RustConverter(CurlConverterBase):
    def __init__(self):
        super().__init__(language='rust')
