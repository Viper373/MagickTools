# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :powershell_converter.py
# @Time      :2024/9/25 下午4:18
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class PowerShellConverter(CurlConverterBase):
    def __init__(self, mode='powershell'):
        """
        初始化 PowerShellConverter
        :param mode: str，可选的 PowerShell 代码生成器，取值为 'powershell', 'powershell-webrequest'
        """
        language_options = ['powershell', 'powershell-webrequest']
        if mode not in language_options:
            raise ValueError(f"无效的 PowerShell 变体 '{mode}'。有效选项为: {', '.join(language_options)}")
        super().__init__(language='powershell', mode=mode)
