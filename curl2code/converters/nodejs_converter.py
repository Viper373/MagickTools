# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :nodejs_converter.py
# @Time      :2024/9/24 下午5:18
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from .curl_converter_base import CurlConverterBase


class NodeJSConverter(CurlConverterBase):
    def __init__(self, mode='node'):
        """
        初始化 NodeJSConverter
        :param mode: str，可选的 Node.js 代码生成器，取值为 'node', 'node-http', 'node-axios', 'node-got', 'node-ky', 'node-request', 'node-superagent'
        """
        language_options = ['node', 'node-http', 'node-axios', 'node-got', 'node-ky', 'node-request', 'node-superagent']
        if mode not in language_options:
            raise ValueError(f"无效的 Node.js 变体 '{mode}'。有效选项为: {', '.join(language_options)}")
        super().__init__(language='nodejs', mode=mode)
