# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :main.py
# @Time      :2024/9/18 下午2:06
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import os
import glob
import configparser
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
import logging
import sys
import io

# 初始化 Rich 控制台
console = Console()

# 读取配置文件
config_parser = configparser.ConfigParser()
with io.open("config.cfg", "r", encoding="utf-8") as f:
    config_parser.read_file(f)
    config = config_parser["default"]

# 获取配置项
input_directory = config.get("pdf_folder", "input")  # 根据您的代码示例，这里假设您有 pdf_folder
output_directory = config.get("output_directory", "output")
file_pattern = config.get("file_pattern", "*.txt")
log_file = config.get("log_file", "logs/merge.log")
overwrite = config.getboolean("overwrite", True)

# 确保输出目录存在
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 确保日志目录存在
log_dir = os.path.dirname(log_file)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(console=console, rich_tracebacks=True),
        logging.FileHandler(log_file,
                            mode='w',
                            encoding='utf-8',
                            maxBytes=10 * 1024 * 1024, backupCount=5) if overwrite else logging.FileHandler(log_file,
                                                                                                            mode='a',
                                                                                                            encoding='utf-8',
                                                                                                            maxBytes=10 * 1024 * 1024,
                                                                                                            backupCount=5)
    ]
)

logger = logging.getLogger("merge_txt")


def get_next_output_file(output_dir, base_name="merged", extension=".txt"):
    """
    获取下一个合并文件的名称，例如 merged_1.txt, merged_2.txt, ...
    """
    existing_files = glob.glob(os.path.join(output_dir, f"{base_name}_*{extension}"))
    max_num = 0
    for file in existing_files:
        try:
            num = int(os.path.splitext(os.path.basename(file))[0].split('_')[-1])
            if num > max_num:
                max_num = num
        except (ValueError, IndexError):
            continue
    next_num = max_num + 1
    return os.path.join(output_dir, f"{base_name}_{next_num}{extension}")


def merge_txt_files(input_dir, pattern, output_dir, overwrite_output=True):
    logger.info("📂 开始合并 .txt 文件...")

    # 查找匹配的文件
    search_pattern = os.path.join(input_dir, pattern)
    txt_files = glob.glob(search_pattern)

    if not txt_files:
        logger.warning("⚠️ 未找到匹配的 .txt 文件。")
        return

    logger.info(f"🔍 找到 {len(txt_files)} 个文件。")

    # 获取下一个输出文件名
    output_path = get_next_output_file(output_dir)

    # 检查输出文件是否存在
    if os.path.exists(output_path):
        if overwrite_output:
            logger.info(f"🗑️ 输出文件已存在，将覆盖：{output_path}")
        else:
            logger.error(f"❌ 输出文件已存在，且不允许覆盖：{output_path}")
            return
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=None, style="green"),
        TextColumn("{task.percentage:>3.0f}%", style="bold"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
        refresh_per_second=2,
    )

    try:
        with progress:
            task = progress.add_task("🍃 开始合并 TXT 文件...", total=len(txt_files))
            with open(output_path, 'w', encoding='utf-8') as outfile:
                for file in txt_files:
                    logger.info(f"📄 处理文件：{file}")
                    with open(file, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content)
                        outfile.write("\n")  # 添加换行符以分隔文件内容
                    progress.advance(task)
        progress.update(task, description="[green]🎉 所有 TXT 文件合并完成！[/green]")
        logger.info(f"✅ 成功合并文件到：{output_path}")
    except Exception as e:
        progress.update(task, description="[red]❌ 合并过程中出错！[/red]")
        logger.error(f"💥 合并过程中出错：{e}")


if __name__ == "__main__":
    merge_txt_files(input_directory, file_pattern, output_directory, overwrite)
