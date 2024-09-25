# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :ruby_converter.py
# @Time      :2024/9/24 下午5:31
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class RubyConverter(CurlConverterBase):
    def __init__(self, mode='ruby'):
        """
        初始化 RubyConverter
        :param mode: str，可选的 Ruby 代码生成器，取值为 'ruby', 'ruby-httparty'
        """
        language_options = ['ruby', 'ruby-httparty']
        if mode not in language_options:
            raise ValueError(f"无效的 Ruby 变体 '{mode}'。有效选项为: {', '.join(language_options)}")
        super().__init__(language='ruby', mode=mode)
