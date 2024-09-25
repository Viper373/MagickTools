# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :r_converter.py
# @Time      :2024/9/24 下午5:25
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class RConverter(CurlConverterBase):
    def __init__(self, mode='r'):
        """
        初始化 RConverter
        :param mode: str，可选的 R 代码生成器，取值为 'r', 'r-httr2'
        """
        language_options = ['r', 'r-httr2']
        if mode not in language_options:
            raise ValueError(f"无效的 R 变体 '{mode}'。有效选项为: {', '.join(language_options)}")
        super().__init__(language='r', mode=mode)
