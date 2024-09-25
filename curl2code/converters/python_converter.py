# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :python_converter.py
# @Time      :2024/9/19 下午3:55
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class PythonConverter(CurlConverterBase):
    def __init__(self, mode='python'):
        """
        初始化 PythonConverter
        :param mode: str，可选的 Python 代码生成器，取值为 'python', 'python-http'
        """
        language_options = ['python', 'python-http']
        if mode not in language_options:
            raise ValueError(f"无效的 Python 变体 '{mode}'。有效选项为: {', '.join(language_options)}")
        super().__init__(language='python', mode=mode)
