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
from converters.python_converter import PythonConverter
from converters.java_converter import JavaConverter
from converters.rust_converter import RustConverter
from converters.ruby_converter import RubyConverter
from converters.go_converter import GoConverter
from converters.javascript_converter import JavaScriptConverter
from converters.nodejs_converter import NodeJSConverter
from converters.dart_converter import DartConverter
from converters.matlab_converter import MatlabConverter
from converters.r_converter import RConverter
from converters.json_converter import JSONConverter
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
        "1": ("Python", PythonConverter()),
        "2": ("Java", JavaConverter()),
        "3": ("Rust", RustConverter()),
        "4": ("Ruby", RubyConverter()),
        "5": ("Go", GoConverter()),
        "6": ("JavaScript", JavaScriptConverter()),
        "7": ("Node.js", NodeJSConverter()),
        "8": ("Dart", DartConverter()),
        "9": ("Matlab", MatlabConverter()),
        "10": ("R", RConverter()),
        "11": ("JSON", JSONConverter()),
    }

    # 提示用户选择目标编程语言
    console.print("请选择目标编程语言：", style="bold cyan")
    for key, (name, _) in converters.items():
        console.print(f"{key}. {name}", style="cyan")

    choice = Prompt.ask("请输入数字（默认：1）", default="1", console=console)
    language, converter = converters[choice]

    if choice not in converters:
        logger.error("❌ 无效的选择。")
        return

    logger.info(f"🔧 选择的目标语言：{language}")

    # 提示用户输入 curl 命令
    curl_command = Prompt.ask("请输入您的 curl 命令", default="", console=console)

    if not curl_command.strip():
        logger.error("❌ 您没有输入任何 curl 命令。")
        return

    logger.info(f"🔍 [cyan]正在转换的 curl 命令: {truncate_string(curl_command)}[/cyan]")

    # 执行转换
    converted_code = converter.convert(curl_command)

    if converted_code:
        console.print(f"\n📝 生成的 {language} 代码如下：\n", style="bold green")
        console.print(converted_code, style="bold")
    else:
        logger.error("❌ 未生成任何代码。")


if __name__ == "__main__":
    main()
