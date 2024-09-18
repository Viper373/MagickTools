# -*- coding:utf-8 -*-
# @Project   :ttf2woff
# @FileName  :main.py
# @Time      :2024/9/14 下午3:30
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import os
import time
import logging
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter
from config import TTF_DIR, WOFF_DIR, OUTPUT_FORMATS, SUBSET_CHARS

from rich.console import Console
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    TimeElapsedColumn,
    SpinnerColumn
)
from rich.logging import RichHandler

# 配置控制台
console = Console()

# 设置根日志器，仅显示 WARNING 级别以上的日志，避免其他库的日志干扰
logging.getLogger().setLevel(logging.WARNING)

# 创建自定义的日志器
logger = logging.getLogger("FontConverter")
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


def truncate_filename(file_path, max_length=10):
    """截断文件路径中的文件名"""
    file_name = os.path.basename(file_path)
    if len(file_name) > max_length:
        return f"{file_name[:7]}...{file_name[-7:]}"  # 截取前8个字符和后5个字符
    return file_name


def convert_font(input_path, output_path, output_format):
    # 检查文件是否存在以及文件大小
    if not os.path.isfile(input_path):
        logger.error(f"❌ [bold red]文件不存在: {truncate_filename(input_path)}[/bold red]")
        return

    file_size = os.path.getsize(input_path)
    if file_size == 0:
        logger.error(f"📂 [bold red]文件为空: {truncate_filename(input_path)}[/bold red]")
        return

    try:
        start_time = time.time()
        # 加载 TTF 文件
        logger.info(f"🔍 [cyan]尝试加载字体文件: {truncate_filename(input_path)}[/cyan]")
        font = TTFont(input_path)

        if output_format == 'woff':
            font.flavor = 'woff'
        elif output_format == 'woff2':
            font.flavor = 'woff2'
        else:
            raise ValueError(f"⚠️ 不支持的格式: {output_format}")

        # 子集化处理
        logger.info("✂️ [cyan]开始子集化处理[/cyan]")
        subsetter = Subsetter()
        subsetter.populate(text=SUBSET_CHARS)
        subsetter.subset(font)

        # 保存转换后的字体文件
        font.save(output_path)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"✅ [green]成功将 {truncate_filename(input_path)} 转换为 {truncate_filename(output_path)}，用时 {elapsed_time:.2f} 秒[/green]")

    except Exception as e:
        logger.error(f"❌ [bold red]转换 {truncate_filename(input_path)} 时发生错误: {e}[/bold red]")


def main():
    if not os.path.exists(WOFF_DIR):
        os.makedirs(WOFF_DIR)

    ttf_files = [f for f in os.listdir(TTF_DIR) if f.lower().endswith('.ttf')]

    if not ttf_files:
        logger.error(f"😞 [bold red]在目录 {TTF_DIR} 中未找到任何 TTF 文件。[/bold red]")
        return

    total_tasks = len(ttf_files) * len(OUTPUT_FORMATS)

    # 设置Rich进度条的列
    progress = Progress(
        SpinnerColumn(spinner_name='dots'),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=None, style="green"),
        TextColumn("{task.percentage:>3.0f}%", style="bold"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
        refresh_per_second=2,
    )

    with progress:
        task_id = progress.add_task("🚀 准备开始转换...", total=total_tasks)

        for file_name in ttf_files:
            input_path = os.path.join(TTF_DIR, file_name)
            for output_format in OUTPUT_FORMATS:
                output_file_name = f"{os.path.splitext(file_name)[0]}.{output_format}"
                output_path = os.path.join(WOFF_DIR, output_file_name)
                description = f"转换: {truncate_filename(file_name)} ➡️ {output_format.upper()}"
                progress.update(task_id, description=description)
                convert_font(input_path, output_path, output_format)
                progress.advance(task_id)

        progress.update(task_id, description="[green]🎉 所有字体转换完成！[/green]")
        logger.info("🎉 [bold green]所有文件已处理完毕。[/bold green]")


if __name__ == "__main__":
    main()
