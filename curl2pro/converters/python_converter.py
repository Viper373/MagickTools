# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :python_converter.py
# @Time      :2024/9/19 下午3:55
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import shlex
import json
from .base_converter import BaseConverter
from curl2pro.utils.logger_util import LoggerSetup


class PythonConverter(BaseConverter):
    def __init__(self):
        """
        初始化 PythonConverter，并配置日志记录器。
        """
        logger_setup = LoggerSetup("PythonConverter")
        self.logger = logger_setup.get_logger()

    def convert(self, curl_command: str) -> str:
        self.logger.info("📡 [cyan]开始解析 curl 命令[/cyan]")
        tokens = shlex.split(curl_command)

        if not tokens or tokens[0] != 'curl':
            self.logger.error("❌ [bold red]命令必须以 'curl' 开头[/bold red]")
            return ""

        # 初始化默认值
        method = 'get'
        url = ''
        headers = {}
        data = None
        files = {}
        auth = None
        params = {}
        json_data = None
        verify = True
        allow_redirects = True
        proxies = {}
        cookies = {}

        # 解析参数
        i = 1
        while i < len(tokens):
            token = tokens[i]
            if token in ['-X', '--request']:
                method = tokens[i + 1].lower()
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
                # 尝试将 data 转换为字典，如果是 JSON 则保持为字典
                if data.startswith('{') and data.endswith('}'):
                    try:
                        json_data = json.loads(data)
                        data = None  # 使用 json 参数而非 data
                        self.logger.debug("检测到 JSON 数据，将其解析为字典")
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
                # PythonConverter 不直接处理输出文件，可以选择实现或忽略
                # 此处忽略 -o 参数
                self.logger.debug(f"忽略输出文件参数: {tokens[i + 1]}")
                i += 2
            elif token in ['-F', '--form']:
                form = tokens[i + 1]
                if '=' in form:
                    key, value = form.split('=', 1)
                    if value.startswith('@'):
                        file_path = value[1:]
                        files[key] = file_path  # 存储文件路径
                        self.logger.debug(f"添加文件上传: {key} = {file_path}")
                    else:
                        # 表单数据可以作为 params 或 data 处理，这里简单处理为 data
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

        # 构建 Python 代码
        self.logger.info("📝 [cyan]开始生成 Python 代码[/cyan]")
        python_code = "import requests\n\n"

        # 设置 URL
        python_code += f"url = \"{url}\"\n"

        # 设置 headers（仅在存在时）
        if headers:
            python_code += "headers = {\n"
            for key, value in headers.items():
                python_code += f"    \"{key}\": \"{value}\",\n"
            python_code += "}\n"
        # 如果没有 headers，不输出 headers

        # 设置 cookies（仅在存在时）
        if cookies:
            python_code += "cookies = {\n"
            for key, value in cookies.items():
                python_code += f"    \"{key}\": \"{value}\",\n"
            python_code += "}\n"

        # 设置 params（如果有）
        if params:
            python_code += "params = {\n"
            for key, value in params.items():
                python_code += f"    \"{key}\": \"{value}\",\n"
            python_code += "}\n"

        # 设置 data 或 json（仅在存在时）
        if json_data:
            python_code += f"json_data = {json.dumps(json_data, indent=4)}\n"
            data_param = "json=json_data"
        elif isinstance(data, dict):
            python_code += f"data = {json.dumps(data, indent=4)}\n"
            data_param = "data=data"
        elif data:
            python_code += f"data = \"{data}\"\n"
            data_param = "data=data"
        else:
            data_param = None

        # 设置 files（仅在存在时）
        if files:
            python_code += "files = {\n"
            for key, file_path in files.items():
                python_code += f"    \"{key}\": open(\"{file_path}\", \"rb\"),\n"
            python_code += "}\n"

        # 设置认证（仅在存在时）
        if auth:
            python_code += f"auth = {auth}\n"

        # 设置代理（仅在存在时）
        if proxies:
            python_code += f"proxies = {proxies}\n"

        # 设置 SSL 验证
        python_code += f"verify = {verify}\n"

        # 设置重定向
        python_code += f"allow_redirects = {allow_redirects}\n"

        # 生成请求代码
        python_code += "\nresponse = requests.{method}(url,\n".format(method=method)
        if headers:
            python_code += "    headers=headers,\n"
        if data_param:
            python_code += f"    {data_param},\n"
        if files:
            python_code += "    files=files,\n"
        if auth:
            python_code += "    auth=auth,\n"
        if proxies:
            python_code += "    proxies=proxies,\n"
        if cookies:
            python_code += "    cookies=cookies,\n"
        python_code += "    verify=verify,\n"
        python_code += "    allow_redirects=allow_redirects\n"
        python_code += ")\n"

        # 生成响应处理代码
        python_code += """
if response.status_code == 200:
    print("✅ 请求成功")
    print(response.text)
else:
    print(f"❌ 请求失败，状态码: {response.status_code}")
    print(response.text)
"""

        # 包装为代码块
        python_code = f"```python\n{python_code}```"

        self.logger.info("✅ [green]Python 代码生成完成[/green]")
        return python_code
