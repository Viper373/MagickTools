# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :nodejs_converter.py
# @Time      :2024/9/24 下午5:18
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import shlex
import json
from .base_converter import BaseConverter
from curl2pro.utils.logger_util import LoggerSetup


class NodeJSConverter(BaseConverter):
    def __init__(self):
        """
        初始化 PythonConverter，并配置日志记录器。
        """
        self.logger_setup = LoggerSetup("NodeJSConverter")
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
                # NodeJSConverter 不直接处理输出文件，可以选择实现或忽略
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

        # 构建 Node.js 代码
        self.logger.info("📝 [cyan]开始生成 Node.js 代码[/cyan]")
        nodejs_code = "const axios = require('axios');\n\n"

        # 设置配置对象
        nodejs_code += "const config = {\n"
        nodejs_code += f"    method: '{method.lower()}',\n"
        nodejs_code += f"    url: '{url}',\n"

        # 添加 headers（仅在存在时）
        if headers:
            nodejs_code += "    headers: {\n"
            for key, value in headers.items():
                nodejs_code += f"        '{key}': '{value}',\n"
            nodejs_code += "    },\n"

        # 添加 data 或 json（仅在存在时）
        if json_data:
            nodejs_code += f"    data: {json.dumps(json_data, indent=4)},\n"
        elif isinstance(data, dict):
            nodejs_code += f"    data: {json.dumps(data, indent=4)},\n"
        elif data:
            nodejs_code += f"    data: `{data}`,\n"

        # 添加认证（仅在存在时）
        if auth:
            nodejs_code += f"    auth: {{\n        username: '{auth[0]}',\n        password: '{auth[1]}'\n    }},\n"

        # 添加代理（仅在存在时）
        if proxies:
            nodejs_code += f"    proxy: {{\n        host: '{proxies['http'].split(':')[0]}',\n        port: {proxies['http'].split(':')[1]},\n    }},\n"

        # 添加 cookies（仅在存在时）
        if cookies:
            cookie_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
            nodejs_code += f"    withCredentials: true,\n    headers: {{ Cookie: '{cookie_str}' }},\n"

        # 设置 SSL 验证
        nodejs_code += f"    httpsAgent: new (require('https').Agent)({{'rejectUnauthorized': {verify}}}),\n"

        # 设置重定向
        nodejs_code += f"    maxRedirects: {'10' if allow_redirects else '0'},\n"

        nodejs_code += "};\n\n"

        # 发送请求
        nodejs_code += "axios(config)\n"
        nodejs_code += "    .then(function (response) {\n"
        nodejs_code += "        console.log('✅ 请求成功');\n"
        nodejs_code += "        console.log(response.data);\n"
        nodejs_code += "    })\n"
        nodejs_code += "    .catch(function (error) {\n"
        nodejs_code += "        console.log('❌ 请求失败');\n"
        nodejs_code += "        console.log(error);\n"
        nodejs_code += "    });\n"

        # 包装为代码块
        nodejs_code = f"```javascript\n{nodejs_code}```"

        self.logger.info("✅ [green]Node.js 代码生成完成[/green]")
        return nodejs_code
