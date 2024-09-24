# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :r_converter.py
# @Time      :2024/9/24 下午5:25
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import shlex
import json
from .base_converter import BaseConverter
from curl2pro.utils.logger_util import LoggerSetup


class RConverter(BaseConverter):
    def __init__(self):
        """
        初始化 PythonConverter，并配置日志记录器。
        """
        self.logger_setup = LoggerSetup("RConverter")
        self.logger = self.logger_setup.get_logger()

    def convert(self, curl_command: str) -> str:
        self.logger.info("📡 [cyan]开始解析 curl 命令[/cyan]")
        tokens = shlex.split(curl_command)

        if not tokens or tokens[0] != 'curl':
            self.logger.error("❌ [bold red]命令必须以 'curl' 开头[/bold red]")
            return ""

        # 初始化默认值
        method = 'GET'
        url = ''
        headers = {}
        data = None
        files = {}
        auth = None
        params = {}
        verify = True
        allow_redirects = True
        proxies = {}
        cookies = {}

        # 解析参数
        i = 1
        while i < len(tokens):
            token = tokens[i]
            if token in ['-X', '--request']:
                method = tokens[i + 1].upper()
                self.logger.debug(f"设置 HTTP 方法为: {method}")
                i += 2
            elif token in ['-H', '--header']:
                header = tokens[i + 1]
                if ':' in header:
                    key, value = header.split(':', 1)
                    headers[key.strip()] = value.strip()
                    self.logger.debug(f"添加请求头: {key.strip()} = {value.strip()}")
                else:
                    self.logger.warning(f"无法解析的头部格式: {header}")
                i += 2
            elif token in ['-d', '--data', '--data-raw', '--data-binary', '--data-urlencode']:
                data = tokens[i + 1]
                if data.startswith('@'):
                    file_path = data[1:]
                    try:
                        with open(file_path, 'r') as f:
                            data = f.read()
                        self.logger.debug(f"从文件 {file_path} 读取数据")
                    except Exception as e:
                        self.logger.error(f"读取数据文件时出错: {e}")
                # 尝试解析 JSON 数据
                if data.startswith('{') and data.endswith('}'):
                    try:
                        json_data = json.loads(data)
                        data = json.dumps(json_data)
                        self.logger.debug("检测到 JSON 数据，将其解析为字符串")
                    except json.JSONDecodeError:
                        pass
                i += 2
            elif token in ['-u', '--user']:
                auth = tokens[i + 1]
                if ':' in auth:
                    user, passwd = auth.split(':', 1)
                    auth = (user, passwd)
                    self.logger.debug(f"设置基本认证: {user} / {'*' * len(passwd)}")
                else:
                    self.logger.warning(f"无法解析的认证格式: {auth}")
                i += 2
            elif token in ['-o', '--output']:
                self.logger.debug(f"忽略输出文件参数: {tokens[i + 1]}")
                i += 2
            elif token in ['-F', '--form']:
                form = tokens[i + 1]
                if '=' in form:
                    key, value = form.split('=', 1)
                    if value.startswith('@'):
                        file_path = value[1:]
                        files[key] = file_path
                        self.logger.debug(f"添加文件上传: {key} = {file_path}")
                    else:
                        data = {key: value}
                        self.logger.debug(f"添加表单数据: {key} = {value}")
                else:
                    self.logger.warning(f"无法解析的表单格式: {form}")
                i += 2
            elif token in ['-L', '--location']:
                allow_redirects = True
                self.logger.debug("允许重定向")
                i += 1
            elif token in ['--insecure', '-k']:
                verify = False
                self.logger.debug("禁用 SSL 证书验证")
                i += 1
            elif token in ['-x', '--proxy']:
                proxy = tokens[i + 1]
                proxies = {
                    "http": proxy,
                    "https": proxy
                }
                self.logger.debug(f"设置代理为: {proxy}")
                i += 2
            elif token in ['--cookie']:
                cookie = tokens[i + 1]
                if '=' in cookie:
                    key, value = cookie.split('=', 1)
                    cookies[key.strip()] = value.strip()
                    self.logger.debug(f"添加 cookie: {key.strip()} = {value.strip()}")
                else:
                    self.logger.warning(f"无法解析的 cookie 格式: {cookie}")
                i += 2
            elif not token.startswith('-'):
                url = token
                self.logger.debug(f"设置 URL 为: {url}")
                i += 1
            else:
                self.logger.warning(f"未处理的选项: {token}")
                i += 1

        # 构建 R 代码
        self.logger.info("📝 [cyan]开始生成 R 代码[/cyan]")
        r_code = "library(httr)\n\n"

        # 设置 URL
        r_code += f"url <- \"{url}\"\n"

        # 设置 headers（仅在存在时）
        if headers:
            r_code += "headers <- c(\n"
            for key, value in headers.items():
                r_code += f"    \"{key}\" = \"{value}\",\n"
            r_code += ")\n"
        # 如果没有 headers，不输出 headers

        # 设置 cookies（仅在存在时）
        if cookies:
            r_code += "cookies <- c(\n"
            for key, value in cookies.items():
                r_code += f"    \"{key}\" = \"{value}\",\n"
            r_code += ")\n"

        # 设置参数（如果有）
        if params:
            r_code += "params <- list(\n"
            for key, value in params.items():
                r_code += f"    {key} = \"{value}\",\n"
            r_code += ")\n"

        # 设置 data 或 json（仅在存在时）
        if data:
            r_code += f"data <- \"{data}\"\n"

        # 设置文件（仅在存在时）
        if files:
            for key, file_path in files.items():
                r_code += f"{key}_file <- upload_file(\"{file_path}\")\n"

        # 设置认证（仅在存在时）
        if auth:
            r_code += f"auth <- authenticate(\"{auth[0]}\", \"{auth[1]}\")\n"

        # 设置代理（仅在存在时）
        if proxies:
            r_code += f"proxies <- \"{proxies['http']}\"\n"

        # 设置 SSL 验证
        r_code += f"verify <- {str(verify).upper()}\n"

        # 生成请求代码
        r_code += "\nresponse <- VERB(\n"
        r_code += f"    \"{method}\",\n"
        r_code += "    url,\n"
        if headers:
            r_code += "    add_headers(.headers = headers),\n"
        if data:
            r_code += "    body = data,\n"
        if files:
            for key in files.keys():
                r_code += f"    {key}_file,\n"
        if auth:
            r_code += "    auth,\n"
        if proxies:
            r_code += "    use_proxy(proxies),\n"
        r_code += "    config = list(verify = verify),\n"
        r_code += f"    followlocation = {str(allow_redirects).upper()}\n"
        r_code += ")\n"

        # 生成响应处理代码
        r_code += """
if (status_code(response) == 200) {
    print("✅ 请求成功")
    print(content(response, "text"))
} else {
    print(paste("❌ 请求失败，状态码:", status_code(response)))
    print(content(response, "text"))
}
"""

        # 包装为代码块
        r_code = f"```R\n{r_code}```"

        self.logger.info("✅ [green]R 代码生成完成[/green]")
        return r_code
