# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :php_converter.py
# @Time      :2024/9/25 下午4:17
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class PHPConverter(CurlConverterBase):
    def __init__(self, mode='php'):
        """
        初始化 PHPConverter
        :param mode: str，可选的 PHP 代码生成器，取值为 'php', 'php-guzzle', 'php-requests'
        """
        language_options = ['php', 'php-guzzle', 'php-requests']
        if mode not in language_options:
            raise ValueError(f"无效的 PHP 变体 '{mode}'。有效选项为: {', '.join(language_options)}")
        super().__init__(language='php', mode=mode)
