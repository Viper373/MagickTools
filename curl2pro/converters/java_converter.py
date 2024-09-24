# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :java_converter.py
# @Time      :2024/9/24 下午5:17
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import shlex
import json
import base64
from .base_converter import BaseConverter
from curl2pro.utils.logger_util import LoggerSetup


class JavaConverter(BaseConverter):
    def __init__(self):
        """
        初始化 PythonConverter，并配置日志记录器。
        """
        self.logger_setup = LoggerSetup("JavaConverter")
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
                # JavaConverter 不直接处理输出文件，可以选择实现或忽略
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

        # 构建 Java 代码
        self.logger.info("📝 [cyan]开始生成 Java 代码[/cyan]")
        java_code = "import java.io.*;\nimport java.net.*;\nimport java.util.*;\n\npublic class CurlToJava {\n    public static void main(String[] args) throws Exception {\n"

        # 构建 URL
        java_code += f"        URL url = new URL(\"{url}\");\n"
        java_code += f"        HttpURLConnection conn = (HttpURLConnection) url.openConnection();\n"
        java_code += f"        conn.setRequestMethod(\"{method}\");\n"

        # 添加 headers
        if headers:
            for key, value in headers.items():
                java_code += f"        conn.setRequestProperty(\"{key}\", \"{value}\");\n"

        # 添加认证
        if auth:
            encoded_auth = base64.b64encode(f"{auth[0]}:{auth[1]}".encode()).decode()
            java_code += f"        conn.setRequestProperty(\"Authorization\", \"Basic {encoded_auth}\");\n"

        # 添加 cookies
        if cookies:
            cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
            java_code += f"        conn.setRequestProperty(\"Cookie\", \"{cookie_str}\");\n"

        # 设置代理（简单示例，未实现复杂代理设置）
        if proxies:
            java_code += f"        // 代理设置需要在 URL 连接前配置\n"

        # 设置 SSL 验证（简单示例，未实现复杂 SSL 验证设置）
        if not verify:
            java_code += f"        // 禁用 SSL 验证需要额外的信任管理器设置\n"

        # 处理数据
        if data or json_data:
            java_code += f"        conn.setDoOutput(true);\n"
            java_code += f"        try(OutputStream os = conn.getOutputStream()) {{\n"
            if json_data:
                json_str = json.dumps(json_data)
                java_code += f"            byte[] input = \"{json_str}\".getBytes(\"utf-8\");\n"
            else:
                java_code += f"            byte[] input = \"{data}\".getBytes(\"utf-8\");\n"
            java_code += f"            os.write(input, 0, input.length);\n"
            java_code += f"        }}\n"

        # 发送请求并获取响应
        java_code += f"\n        int status = conn.getResponseCode();\n"
        java_code += f"        BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));\n"
        java_code += f"        String inputLine;\n"
        java_code += f"        StringBuffer content = new StringBuffer();\n"
        java_code += f"        while ((inputLine = in.readLine()) != null) {{\n"
        java_code += f"            content.append(inputLine);\n"
        java_code += f"        }}\n"
        java_code += f"        in.close();\n"
        java_code += f"        conn.disconnect();\n\n"

        # 处理输出
        java_code += f"        if (status == 200) {{\n"
        java_code += f"            System.out.println(\"✅ 请求成功\");\n"
        java_code += f"            System.out.println(content.toString());\n"
        java_code += f"        }} else {{\n"
        java_code += f"            System.out.println(\"❌ 请求失败，状态码: \" + status);\n"
        java_code += f"            System.out.println(content.toString());\n"
        java_code += f"        }}\n    }}\n}}"

        # 包装为代码块
        java_code = f"```java\n{java_code}```"

        self.logger.info("✅ [green]Java 代码生成完成[/green]")
        return java_code
