# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :go_converter.py
# @Time      :2024/9/24 下午5:14
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import shlex
import json
from .base_converter import BaseConverter
from curl2pro.utils.logger_util import LoggerSetup


class GoConverter(BaseConverter):
    def __init__(self):
        """
        初始化 PythonConverter，并配置日志记录器。
        """
        self.logger_setup = LoggerSetup("GoConverter")
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
                # GoConverter 不直接处理输出文件，可以选择实现或忽略
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

        # 构建 Go 代码
        self.logger.info("📝 [cyan]开始生成 Go 代码[/cyan]")
        go_code = "package main\n\nimport (\n\t\"fmt\"\n\t\"net/http\"\n\t\"bytes\"\n\t\"io/ioutil\"\n)\n\nfunc main() {\n"

        # 构建请求
        if data:
            go_code += f"\tdata := `{data}`\n"
            go_code += f"\treq, err := http.NewRequest(\"{method}\", \"{url}\", bytes.NewBuffer([]byte(data)))\n"
        elif json_data:
            json_str = json.dumps(json_data, indent=4)
            go_code += f"\tdata := `{json_str}`\n"
            go_code += f"\treq, err := http.NewRequest(\"{method}\", \"{url}\", bytes.NewBuffer([]byte(data)))\n"
        else:
            go_code += f"\treq, err := http.NewRequest(\"{method}\", \"{url}\", nil)\n"

        go_code += "\tif err != nil {\n\t\tfmt.Println(\"Error creating request:\", err)\n\t\treturn\n\t}\n\n"

        # 添加 headers
        if headers:
            for key, value in headers.items():
                go_code += f"\treq.Header.Set(\"{key}\", \"{value}\")\n"

        # 添加 cookies
        if cookies:
            for key, value in cookies.items():
                go_code += f"\treq.AddCookie(&http.Cookie{{Name: \"{key}\", Value: \"{value}\"}})\n"

        # 添加认证
        if auth:
            go_code += f"\treq.SetBasicAuth(\"{auth[0]}\", \"{auth[1]}\")\n"

        # 设置代理（简单示例，未实现复杂代理设置）
        if proxies:
            go_code += f"\tclient := &http.Client{{Transport: &http.Transport{{Proxy: http.ProxyURL({proxies})}}}}\n"
        else:
            go_code += f"\tclient := &http.Client{{}}\n"

        # 发送请求
        go_code += "\tresp, err := client.Do(req)\n"
        go_code += "\tif err != nil {\n\t\tfmt.Println(\"Error making request:\", err)\n\t\treturn\n\t}\n"
        go_code += "\tdefer resp.Body.Close()\n\n"

        # 处理响应
        go_code += "\tbody, err := ioutil.ReadAll(resp.Body)\n"
        go_code += "\tif err != nil {\n\t\tfmt.Println(\"Error reading response:\", err)\n\t\treturn\n\t}\n\n"
        go_code += "\tfmt.Println(\"Status Code:\", resp.StatusCode)\n"
        go_code += "\tfmt.Println(\"Response Body:\")\n"
        go_code += "\tfmt.Println(string(body))\n}"

        # 包装为代码块
        go_code = f"```go\n{go_code}```"

        self.logger.info("✅ [green]Go 代码生成完成[/green]")
        return go_code
