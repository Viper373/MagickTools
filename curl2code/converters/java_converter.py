# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :java_converter.py
# @Time      :2024/9/24 下午5:17
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class JavaConverter(CurlConverterBase):
    def __init__(self, mode='java'):
        """
        初始化 JavaConverter
        :param mode: str，可选的 Java 代码生成器，取值为 'java', 'java-httpurlconnection', 'java-jsoup', 'java-okhttp'
        """
        language_options = ['java', 'java-httpurlconnection', 'java-jsoup', 'java-okhttp']
        if mode not in language_options:
            raise ValueError(f"无效的 Java 变体 '{mode}'。有效选项为: {', '.join(language_options)}")
        super().__init__(language='java', mode=mode)
