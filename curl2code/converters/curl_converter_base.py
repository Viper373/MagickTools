# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :curl_converter_base.py
# @Time      :2024/9/25 上午11:53
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import subprocess
from .base_converter import BaseConverter
from curl2code.utils.logger_util import LoggerSetup


class CurlConverterBase(BaseConverter):
    def __init__(self, language: str, mode: str = None):
        """
        初始化 CurlConverterBase，并配置日志记录器。

        :param language: str，目标编程语言（用于日志记录）
        :param mode: str，curlconverter 的 --language 参数值，如果与 language 不同
        """
        logger_setup = LoggerSetup(f"{language.capitalize()}Converter")
        self.logger = logger_setup.get_logger()
        self.language = language
        self.code_language = mode if mode else language

    def convert(self, curl_command: str) -> str:
        """
        使用 curlconverter 将 curl 命令转换为目标语言代码。

        :param curl_command: str，完整的 curl 命令字符串
        :return: str，生成的目标语言代码
        """
        self.logger.info(f"📡 [cyan]开始解析 curl 命令为 {self.language} 代码[/cyan]")
        try:
            process = subprocess.Popen(
                ['curlconverter', '--language', self.code_language, '-'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate(input=curl_command.encode('utf-8'))
            if process.returncode != 0:
                error_message = stderr.decode('utf-8')
                self.logger.error(f"❌ [bold red]curlconverter 错误:[/bold red] {error_message}")
                return ""
            code = stdout.decode('utf-8')
            self.logger.info(f"✅ [green]{self.language.capitalize()} 代码生成完成[/green]")
            return f"```{self.language}\n{code}```"
        except Exception as e:
            self.logger.error(f"❌ [bold red]发生异常:[/bold red] {str(e)}")
            return ""
