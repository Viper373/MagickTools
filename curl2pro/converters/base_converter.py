# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :base_converter.py
# @Time      :2024/9/24 下午5:02
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import abc


class BaseConverter(abc.ABC):
    @abc.abstractmethod
    def convert(self, curl_command: str) -> str:
        """
        将 curl 命令转换为目标语言的请求代码。

        :param curl_command: str，完整的 curl 命令字符串
        :return: str，生成的目标语言代码
        """
        pass
