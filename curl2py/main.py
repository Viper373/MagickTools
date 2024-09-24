# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :main.py
# @Time      :2024/9/19 下午3:55
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import shlex
import json
import logging
from rich.console import Console
from rich.logging import RichHandler
import argparse

# 配置控制台
console = Console()

# 设置根日志器，仅显示 WARNING 级别以上的日志，避免其他库的日志干扰
logging.getLogger().setLevel(logging.WARNING)

# 创建自定义的日志器
logger = logging.getLogger("CurlToPythonConverter")
logger.setLevel(logging.INFO)  # 设置为 INFO 或 DEBUG

# 创建并配置 RichHandler
rich_handler = RichHandler(console=console, markup=True, show_path=False)
rich_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s", datefmt="[%X]")
rich_handler.setFormatter(formatter)

# 清除自定义日志器的默认处理器（如果有）
if logger.hasHandlers():
    logger.handlers.clear()

# 将 RichHandler 添加到自定义日志器
logger.addHandler(rich_handler)

# 确保自定义日志器不将日志传播到根日志器，避免重复输出
logger.propagate = False


def truncate_string(s, max_length=30):
    """
    截断字符串到指定长度，超过部分用省略号代替。
    """
    if len(s) > max_length:
        return f"{s[:max_length // 2]}...{s[-max_length // 2:]}"
    return s


def curl_to_python(curl_command):
    """
    将 curl 命令转换为等效的 Python requests 代码。

    :param curl_command: str，完整的 curl 命令字符串
    :return: str，生成的 Python 代码
    """
    logger.info("📡 [cyan]开始解析 curl 命令[/cyan]")
    tokens = shlex.split(curl_command)

    if not tokens or tokens[0] != 'curl':
        logger.error("❌ [bold red]命令必须以 'curl' 开头[/bold red]")
        return ""

    # 初始化默认值
    method = 'get'
    url = ''
    headers = {}
    data = None
    files = {}
    auth = None
    output = None
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
            logger.debug(f"设置 HTTP 方法为: {method}")
            i += 2
        elif token in ['-H', '--header']:
            header = tokens[i + 1]
            if ':' in header:
                key, value = header.split(':', 1)
                headers[key.strip()] = value.strip()
                logger.debug(f"添加请求头: {key.strip()} = {value.strip()}")
            else:
                logger.warning(f"无法解析的头部格式: {header}")
            i += 2
        elif token in ['-d', '--data', '--data-raw', '--data-binary', '--data-urlencode']:
            data = tokens[i + 1]
            if data.startswith('@'):
                file_path = data[1:]
                try:
                    with open(file_path, 'r') as f:
                        data = f.read()
                    logger.debug(f"从文件 {file_path} 读取数据")
                except Exception as e:
                    logger.error(f"读取数据文件时出错: {e}")
            # 尝试将 data 转换为字典，如果是 JSON 则保持为字典
            if data.startswith('{') and data.endswith('}'):
                try:
                    json_data = json.loads(data)
                    data = None  # 使用 json 参数而非 data
                    logger.debug("检测到 JSON 数据，将其解析为字典")
                except json.JSONDecodeError:
                    pass
            i += 2
        elif token in ['-u', '--user']:
            auth = tokens[i + 1]
            if ':' in auth:
                user, passwd = auth.split(':', 1)
                auth = (user, passwd)
                logger.debug(f"设置基本认证: {user} / {'*' * len(passwd)}")
            else:
                logger.warning(f"无法解析的认证格式: {auth}")
            i += 2
        elif token in ['-o', '--output']:
            output = tokens[i + 1]
            logger.debug(f"设置输出文件为: {output}")
            i += 2
        elif token in ['-F', '--form']:
            form = tokens[i + 1]
            if '=' in form:
                key, value = form.split('=', 1)
                if value.startswith('@'):
                    file_path = value[1:]
                    files[key] = open(file_path, 'rb')
                    logger.debug(f"添加文件上传: {key} = {file_path}")
                else:
                    data[key] = value
                    logger.debug(f"添加表单数据: {key} = {value}")
            else:
                logger.warning(f"无法解析的表单格式: {form}")
            i += 2
        elif token in ['-L', '--location']:
            allow_redirects = True
            logger.debug("允许重定向")
            i += 1
        elif token in ['--insecure', '-k']:
            verify = False
            logger.debug("禁用 SSL 证书验证")
            i += 1
        elif token in ['-x', '--proxy']:
            proxy = tokens[i + 1]
            proxies = {
                "http": proxy,
                "https": proxy
            }
            logger.debug(f"设置代理为: {proxy}")
            i += 2
        elif token in ['--cookie']:
            cookie = tokens[i + 1]
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
                logger.debug(f"添加 cookie: {key.strip()} = {value.strip()}")
            else:
                logger.warning(f"无法解析的 cookie 格式: {cookie}")
            i += 2
        elif not token.startswith('-'):
            url = token
            logger.debug(f"设置 URL 为: {url}")
            i += 1
        else:
            logger.warning(f"未处理的选项: {token}")
            i += 1

    # 构建 Python 代码
    logger.info("📝 [cyan]开始生成 Python 代码[/cyan]")
    python_code = "import requests\n\n"

    # 设置 URL
    python_code += f"url = \"{url}\"\n"

    # 设置 headers
    if headers:
        python_code += "headers = {\n"
        for key, value in headers.items():
            python_code += f"    \"{key}\": \"{value}\",\n"
        python_code += "}\n"
    else:
        python_code += "headers = {}\n"

    # 设置 cookies
    if cookies:
        python_code += "cookies = {\n"
        for key, value in cookies.items():
            python_code += f"    \"{key}\": \"{value}\",\n"
        python_code += "}\n"
    else:
        python_code += "cookies = {}\n"

    # 设置 params（如果有）
    if params:
        python_code += "params = {\n"
        for key, value in params.items():
            python_code += f"    \"{key}\": \"{value}\",\n"
        python_code += "}\n"
    else:
        python_code += "params = {}\n"

    # 设置 data 或 json
    if json_data:
        python_code += f"json_data = {json.dumps(json_data, indent=4)}\n"
        data_param = "json=json_data"
    elif data:
        python_code += f"data = \"{data}\"\n"
        data_param = "data=data"
    else:
        data_param = "data=None"

    # 设置 files
    if files:
        python_code += "files = {\n"
        for key, file in files.items():
            python_code += f"    \"{key}\": open(\"{file.name}\", \"rb\"),\n"
        python_code += "}\n"
    else:
        python_code += "files = {}\n"

    # 设置认证
    if auth:
        python_code += f"auth = {auth}\n"
    else:
        python_code += "auth = None\n"

    # 设置代理
    if proxies:
        python_code += f"proxies = {proxies}\n"
    else:
        python_code += "proxies = {}\n"

    # 设置 SSL 验证
    python_code += f"verify = {verify}\n"

    # 设置重定向
    python_code += f"allow_redirects = {allow_redirects}\n"

    # 生成请求代码
    python_code += "\nresponse = requests.{method}(url,\n".format(method=method)
    python_code += "    headers=headers,\n"
    if json_data:
        python_code += "    json=json_data,\n"
    elif data:
        python_code += "    data=data,\n"
    if files:
        python_code += "    files=files,\n"
    if auth:
        python_code += "    auth=auth,\n"
    if proxies:
        python_code += "    proxies=proxies,\n"
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

    logger.info("✅ [green]Python 代码生成完成[/green]")
    return python_code


def main():
    parser = argparse.ArgumentParser(description="将 curl 命令转换为 Python requests 代码的工具")
    parser.add_argument('--curl', type=str, help='要转换的 curl 命令', required=True)
    args = parser.parse_args()

    curl_command = args.curl
    logger.info(f"🔍 [cyan]正在转换的 curl 命令: {truncate_string(curl_command)}[/cyan]")

    python_code = curl_to_python(curl_command)

    if python_code:
        print("\n📝 生成的 Python 代码如下：\n")
        print(python_code)


if __name__ == "__main__":
    main()

