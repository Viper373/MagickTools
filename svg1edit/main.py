# -*- coding:utf-8 -*-
# @Project   :MagickTools
# @FileName  :main.py
# @Time      :2024/4/27 下午5:45
# @Author    :ChatGPT
# @Software  :PyCharm

import os
import glob
import configparser
from rich.console import Console
from rich.logging import RichHandler
from logging.handlers import RotatingFileHandler
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.prompt import Prompt
import logging
import sys
import io
import re
import xml.etree.ElementTree as ET

# 初始化 Rich 控制台
console = Console()

# 读取配置文件
config_parser = configparser.ConfigParser()
config_file = "config.cfg"
if not os.path.exists(config_file):
    console.print(f"[red]配置文件 {config_file} 不存在，请创建并配置相应参数。[/red]")
    sys.exit(1)

with io.open(config_file, "r", encoding="utf-8") as f:
    config_parser.read_file(f)
    config = config_parser["default"]

# 获取配置项
input_directory = config.get("input_directory", "input_svgs")
output_directory = config.get("output_directory", "output_svgs")
file_pattern = config.get("file_pattern", "*.svg")
log_file = config.get("log_file", "logs/modify_svg.log")
overwrite = config.getboolean("overwrite", True)
default_new_width = config.get("new_width", "800")
default_new_height = config.get("new_height", "600")

# 确保输出目录存在
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    console.print(f"[green]已创建输出目录：{output_directory}[/green]")

# 确保日志目录存在
log_dir = os.path.dirname(log_file)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)
    console.print(f"[green]已创建日志目录：{log_dir}[/green]")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(console=console, rich_tracebacks=True),
        RotatingFileHandler(
            log_file,
            mode='w' if overwrite else 'a',
            encoding='utf-8',
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=5
        )
    ]
)

logger = logging.getLogger("main")


def get_svg_size(svg_file):
    """
    获取 SVG 文件的宽度和高度
    """
    try:
        tree = ET.parse(svg_file)
        root = tree.getroot()

        width = root.get('width')
        height = root.get('height')

        # 如果 width 和 height 包含单位（如 px），则去掉单位
        width_value = re.findall(r"[\d.]+", width)[0] if width else None
        height_value = re.findall(r"[\d.]+", height)[0] if height else None

        return float(width_value) if width_value else None, float(height_value) if height_value else None, width, height
    except ET.ParseError:
        logger.error(f"❌ 无法解析 SVG 文件：{svg_file}")
        return None, None, None, None


def set_svg_size(tree, new_width, new_height):
    """
    设置 SVG 树的新的宽度和高度
    """
    root = tree.getroot()

    # 保留原有的单位（如存在）
    width = root.get('width')
    height = root.get('height')

    width_unit = re.findall(r"[a-zA-Z%]+", width)[0] if width and re.findall(r"[a-zA-Z%]+", width) else ""
    height_unit = re.findall(r"[a-zA-Z%]+", height)[0] if height and re.findall(r"[a-zA-Z%]+", height) else ""

    # 设置新的宽度和高度
    root.set('width', f"{new_width}{width_unit}")
    root.set('height', f"{new_height}{height_unit}")


def get_next_output_file(output_dir, base_name="new_", extension=".svg"):
    """
    获取下一个输出文件的名称，例如 new_image.svg, new_image_1.svg, ...
    """
    existing_files = glob.glob(os.path.join(output_dir, f"{base_name}*{extension}"))
    if not existing_files:
        return os.path.join(output_dir, f"{base_name}0{extension}")

    max_num = 0
    for file in existing_files:
        try:
            base = os.path.splitext(os.path.basename(file))[0]
            num_part = base.replace(base_name, "")
            num = int(num_part) if num_part.isdigit() else 0
            if num > max_num:
                max_num = num
        except (ValueError, IndexError):
            continue
    next_num = max_num + 1
    return os.path.join(output_dir, f"{base_name}{next_num}{extension}")


def modify_svg_files(input_dir, pattern, output_dir, default_new_width, default_new_height):
    logger.info("📂 开始修改 SVG 文件大小...")

    # 查找匹配的文件
    search_pattern = os.path.join(input_dir, pattern)
    svg_files = glob.glob(search_pattern)

    if not svg_files:
        logger.warning("⚠️ 未找到匹配的 SVG 文件。")
        return

    logger.info(f"🔍 找到 {len(svg_files)} 个 SVG 文件。")

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
            task = progress.add_task("🔧 正在修改 SVG 文件大小...", total=len(svg_files))
            for svg_file in svg_files:
                logger.info(f"📄 处理文件：{svg_file}")
                current_width, current_height, original_width, original_height = get_svg_size(svg_file)
                if current_width is None or current_height is None:
                    logger.error(f"❌ 跳过文件（无法获取尺寸）：{svg_file}")
                    progress.advance(task)
                    continue

                # 显示当前尺寸
                logger.info(f"📐 当前尺寸：宽度={current_width}{re.findall(r'[a-zA-Z%]+', original_width)[0] if re.findall(r'[a-zA-Z%]+', original_width) else ''}, 高度={current_height}{re.findall(r'[a-zA-Z%]+', original_height)[0] if re.findall(r'[a-zA-Z%]+', original_height) else ''}")

                # 提示用户输入新的宽度和高度
                new_width_input = Prompt.ask(
                    f"请输入新的宽度（当前宽度={current_width}，按回车使用默认 [{default_new_width}]）",
                    default=str(default_new_width),
                    console=console
                )

                new_height_input = Prompt.ask(
                    f"请输入新的高度（当前高度={current_height}，按回车使用默认 [{default_new_height}]）",
                    default=str(default_new_height),
                    console=console
                )

                # 解析输入
                try:
                    nw = float(new_width_input)
                    nh = float(new_height_input)
                except ValueError:
                    logger.error(f"❌ 输入的宽度或高度无效：width={new_width_input}, height={new_height_input}，将使用默认值。")
                    nw = float(default_new_width)
                    nh = float(default_new_height)

                # 读取并修改 SVG 文件
                try:
                    tree = ET.parse(svg_file)
                    set_svg_size(tree, nw, nh)

                    # 生成新的文件名
                    base_name = os.path.basename(svg_file)
                    new_file_path = os.path.join(output_dir, f"new_{base_name}")

                    # 保存新的 SVG 文件
                    tree.write(new_file_path, encoding='utf-8', xml_declaration=True)
                    logger.info(
                        f"✅ 已保存新文件：{new_file_path}（宽度 = {nw}{re.findall(r'[a-zA-Z%]+', original_width)[0] if re.findall(r'[a-zA-Z%]+', original_width) else ''}, 高度 = {nh}{re.findall(r'[a-zA-Z%]+', original_height)[0] if re.findall(r'[a-zA-Z%]+', original_height) else ''}）")
                except Exception as e:
                    logger.error(f"💥 修改文件时出错：{svg_file}，错误：{e}")

                progress.advance(task)
        progress.update(task, description="[green]🎉 所有 SVG 文件修改完成！[/green]")
        logger.info("✅ 所有 SVG 文件已成功修改。")
    except Exception as e:
        progress.update(task, description="[red]❌ 修改过程中出错！[/red]")
        logger.error(f"💥 修改过程中出错：{e}")


if __name__ == "__main__":
    modify_svg_files(input_directory, file_pattern, output_directory, default_new_width, default_new_height)
