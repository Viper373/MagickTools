# -*- coding:utf-8 -*-
# @Project   :png2ico
# @FileName  :main.py
# @Time      :2024/8/29 下午3:14
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import os
import sys
import logging
from configparser import ConfigParser
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image

from rich.logging import RichHandler
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn, SpinnerColumn


def png_to_ico(png_file_path, ico_file_path):
    img = Image.open(png_file_path)
    # 确保图像为 RGBA 模式
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    # 定义需要包含的图标尺寸
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (24, 24), (16, 16)]
    # 调整原始图像到最大尺寸
    max_size = max(icon_sizes)
    img = img.resize(max_size, Image.LANCZOS)
    # 保存 ICO 文件，包含多个尺寸
    img.save(ico_file_path, format='ICO', sizes=icon_sizes)


def main():
    # 配置日志记录
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()]
    )
    logger = logging.getLogger("PNG2ICO")

    # 读取配置文件
    config_parser = ConfigParser()
    with open("config.cfg", "r", encoding="utf-8") as config_file:
        config_parser.read_file(config_file)
    config = config_parser["default"]

    png_folder = config["png_folder"]
    ico_folder = config["ico_folder"]
    max_workers = int(config["max_worker"])

    # 获取所有待处理的 PNG 文件
    png_files = [f for f in os.listdir(png_folder) if f.lower().endswith('.png')]
    total_tasks = len(png_files)
    if total_tasks == 0:
        logger.error(f"😞 在目录 {png_folder} 中未找到任何 PNG 文件。")
        sys.exit(1)

    # 确保输出目录存在
    if not os.path.exists(ico_folder):
        os.makedirs(ico_folder)

    # 设置进度条
    progress = Progress(
        SpinnerColumn(spinner_name='earth'),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=None),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    )

    with progress:
        task_id = progress.add_task("🚀 正在将 PNG 转换为 ICO...", total=total_tasks)
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for file in png_files:
                file_name = os.path.splitext(file)[0]
                png_file = os.path.join(png_folder, file)
                ico_file = os.path.join(ico_folder, file_name + ".ico")
                logger.info(f"📥 提交任务: {png_file} ➡️ {ico_file}")
                future = executor.submit(png_to_ico, png_file, ico_file)
                futures[future] = (png_file, ico_file)

            for future in as_completed(futures):
                png_file, ico_file = futures[future]
                try:
                    future.result()
                    logger.info(f"✅ 完成转换: {png_file} ➡️ {ico_file}")
                except Exception as e:
                    logger.error(f"❌ 处理文件 {png_file} 时发生错误: {e}")
                finally:
                    progress.advance(task_id)

        progress.update(task_id, description="[green]🎉 转换完成[/green]")
        progress.stop()

    logger.info("🎉 所有文件已处理完毕。")


if __name__ == "__main__":
    main()
