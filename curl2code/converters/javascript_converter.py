# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :javascript_converter.py
# @Time      :2024/9/24 下午5:19
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class JavaScriptConverter(CurlConverterBase):
    def __init__(self, mode='javascript'):
        """
        初始化 JavaScriptConverter
        :param mode: str，可选的 JavaScript 代码生成器，取值为 'javascript', 'javascript-jquery', 'javascript-xhr'
        """
        language_options = ['javascript', 'javascript-jquery', 'javascript-xhr']
        if mode not in language_options:
            raise ValueError(f"无效的 JavaScript 变体 '{mode}'。有效选项为: {', '.join(language_options)}")
        super().__init__(language='javascript', mode=mode)
