# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :ansible_converter.py
# @Time      :2024/9/25 下午3:34
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class AnsibleConverter(CurlConverterBase):
    def __init__(self):
        super().__init__(language='ansible')
