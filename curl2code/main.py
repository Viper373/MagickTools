# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :main.py
# @Time      :2024/9/24 下午5:09
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.prompt import Prompt
from rich.table import Table
from converters.ansible_converter import AnsibleConverter
from converters.c_converter import CConverter
from converters.cfml_converter import CFMLConverter
from converters.clojure_converter import ClojureConverter
from converters.csharp_converter import CSharpConverter
from converters.dart_converter import DartConverter
from converters.elixir_converter import ElixirConverter
from converters.go_converter import GoConverter
from converters.har_converter import HARConverter
from converters.http_converter import HTTPConverter
from converters.httpie_converter import HTTPieConverter
from converters.java_converter import JavaConverter
from converters.javascript_converter import JavaScriptConverter
from converters.json_converter import JSONConverter
from converters.julia_converter import JuliaConverter
from converters.kotlin_converter import KotlinConverter
from converters.lua_converter import LuaConverter
from converters.matlab_converter import MATLABConverter
from converters.nodejs_converter import NodeJSConverter
from converters.objc_converter import ObjectiveCConverter
from converters.ocaml_converter import OCamlConverter
from converters.perl_converter import PerlConverter
from converters.php_converter import PHPConverter
from converters.powershell_converter import PowerShellConverter
from converters.python_converter import PythonConverter
from converters.r_converter import RConverter
from converters.ruby_converter import RubyConverter
from converters.rust_converter import RustConverter
from converters.swift_converter import SwiftConverter
from converters.wget_converter import WgetConverter
from utils.format import truncate_string

# 配置控制台
console = Console()

# 设置根日志器，仅显示 WARNING 级别以上的日志，避免其他库的日志干扰
logging.getLogger().setLevel(logging.WARNING)

# 创建自定义的日志器
logger = logging.getLogger("CurlConverter")
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


def main():
    # 支持的转换器字典
    converters = {
        "1": ("Ansible", AnsibleConverter),
        "2": ("C", CConverter),
        "3": ("CFML", CFMLConverter),
        "4": ("Clojure", ClojureConverter),
        "5": ("C#", CSharpConverter),
        "6": ("Dart", DartConverter),
        "7": ("Elixir", ElixirConverter),
        "8": ("Go", GoConverter),
        "9": ("HAR", HARConverter),
        "10": ("HTTP", HTTPConverter),
        "11": ("HTTPie", HTTPieConverter),
        "12": ("Java", JavaConverter),
        "13": ("JavaScript", JavaScriptConverter),
        "14": ("JSON", JSONConverter),
        "15": ("Julia", JuliaConverter),
        "16": ("Kotlin", KotlinConverter),
        "17": ("Lua", LuaConverter),
        "18": ("MATLAB", MATLABConverter),
        "19": ("Node.js", NodeJSConverter),
        "20": ("Objective-C", ObjectiveCConverter),
        "21": ("OCaml", OCamlConverter),
        "22": ("Perl", PerlConverter),
        "23": ("PHP", PHPConverter),
        "24": ("PowerShell", PowerShellConverter),
        "25": ("Python", PythonConverter),
        "26": ("R", RConverter),
        "27": ("Ruby", RubyConverter),
        "28": ("Rust", RustConverter),
        "29": ("Swift", SwiftConverter),
        "30": ("Wget", WgetConverter),
    }

    # 提示用户选择目标编程语言
    console.print("请选择目标编程语言：", style="bold cyan")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("编号", style="dim", width=6)
    table.add_column("语言")

    for key, (name, _) in converters.items():
        table.add_row(key, name)

    console.print(table)

    choice = Prompt.ask("请输入数字（默认：25）", default="25", console=console)
    if choice not in converters:
        logger.error("❌ 无效的选择。")
        return

    language_name, converter_class = converters[choice]

    # 处理具有多个变体的语言
    variant = None
    if language_name in ["Java", "JavaScript", "Node.js", "PHP", "PowerShell", "Python", "R", "Ruby"]:
        # 定义每种语言的可用变体
        variants = {
            "Java": ['java', 'java-httpurlconnection', 'java-jsoup', 'java-okhttp'],
            "JavaScript": ['javascript', 'javascript-jquery', 'javascript-xhr'],
            "Node.js": ['node', 'node-http', 'node-axios', 'node-got', 'node-ky', 'node-request', 'node-superagent'],
            "PHP": ['php', 'php-guzzle', 'php-requests'],
            "PowerShell": ['powershell', 'powershell-webrequest'],
            "Python": ['python', 'python-http'],
            "R": ['r', 'r-httr2'],
            "Ruby": ['ruby', 'ruby-httparty'],
        }
        language_variants = variants[language_name]
        console.print(f"\n{language_name} 有以下可选变体：", style="bold cyan")
        for idx, var in enumerate(language_variants, 1):
            console.print(f"{idx}. {var}", style="cyan")
        variant_choice = Prompt.ask("请选择变体编号（默认：1）", default="1", console=console)
        try:
            variant_index = int(variant_choice) - 1
            variant = language_variants[variant_index]
        except (ValueError, IndexError):
            logger.error("❌ 无效的选择，使用默认变体。")
            variant = language_variants[0]
        logger.info(f"🔧 选择的 {language_name} 变体：{variant}")
        # 使用变体初始化转换器
        converter = converter_class(variant=variant)
    else:
        # 无变体，直接初始化转换器
        converter = converter_class()

    logger.info(f"🔧 选择的目标语言：{language_name}")

    # 提示用户输入 curl 命令
    curl_command = Prompt.ask("\n请输入您的 curl 命令", default="", console=console)

    if not curl_command.strip():
        logger.error("❌ 您没有输入任何 curl 命令。")
        return

    logger.info(f"🔍 [cyan]正在转换的 curl 命令: {truncate_string(curl_command)}[/cyan]")

    # 执行转换
    converted_code = converter.convert(curl_command)

    if converted_code:
        console.print(f"\n📝 生成的 {language_name} 代码如下：\n", style="bold green")
        console.print(converted_code, style="bold")
    else:
        logger.error("❌ 未生成任何代码。")


if __name__ == "__main__":
    main()
