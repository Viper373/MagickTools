# -*- coding:utf-8 -*-
# @Project   :dir2zip
# @FileName  :main.py
# @Time      :2024/8/30 上午10:18
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import os
import sys
import logging
from configparser import ConfigParser
from concurrent.futures import ProcessPoolExecutor, as_completed

from rich.logging import RichHandler
from rich.table import Column
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
    SpinnerColumn,
    TimeElapsedColumn
)

from compression_methods import get_compression_method


def compress_directory(directory_path, output_path, method):
    compress_method = get_compression_method(method)
    if compress_method:
        compress_method(directory_path, output_path)
    else:
        logger.error(f"未找到压缩方法: {method}")


def main():
    # 配置日志记录
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()]
    )
    global logger
    logger = logging.getLogger("Dir2Zip")

    # 读取配置文件
    config_parser = ConfigParser()
    with open("config.cfg", "r", encoding="utf-8") as config_file:
        config_parser.read_file(config_file)
    config = config_parser

    input_folder = config["default"]["input_folder"]
    output_folder = config["default"]["output_folder"]
    max_workers = int(config["default"]["max_worker"])

    # 获取用户输入的压缩格式，如果未输入，则使用默认格式
    user_input_format = input("请输入压缩格式（现支持 zip, 7z, rar, tar, gz, gztar, bz2, bztar, xztar ，回车默认zip）：").strip()
    if not user_input_format:
        compression_format = config["default"]["format"]
        logger.info(f"未输入格式，使用默认格式: {compression_format}")
    else:
        compression_format = user_input_format
        logger.info(f"用户输入格式: {compression_format}")

    # 获取待处理的目录列表
    directories = [d for d in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, d))]
    total_tasks = len(directories)
    if total_tasks == 0:
        logger.error(f"😞 在目录 {input_folder} 中未找到任何子目录。")
        sys.exit(1)

    # 确保输出目录存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 设置Rich进度条的列
    progress_column = TextColumn("[progress.description]", table_column=Column(ratio=1))
    task_column = TextColumn("{task.description}", table_column=Column(ratio=2))
    completed_column = TextColumn(" | ({task.completed:>.2f}/{task.total:>.2f})", table_column=Column(ratio=1))
    spinner_column = SpinnerColumn(finished_text="[green]✅ ", table_column=Column(ratio=1))
    bar_column = BarColumn(table_column=Column(ratio=2))
    percentage_column = TextColumn("{task.percentage:>3.1f}%", table_column=Column(ratio=1))
    download_column = DownloadColumn(table_column=Column(ratio=1))
    transfer_speed_column = TransferSpeedColumn(table_column=Column(ratio=1))
    time_remaining_column = TimeRemainingColumn(table_column=Column(ratio=1))
    time_elapsed_column = TimeElapsedColumn(table_column=Column(ratio=1))

    progress = Progress(
        progress_column,
        task_column,
        completed_column,
        spinner_column,
        bar_column,
        percentage_column,
        "🌐 ",
        download_column,
        "🚀 ",
        transfer_speed_column,
        "⏳ ",
        time_remaining_column,
        "🕝 ",
        time_elapsed_column,
        # expand=True,
    )

    with progress:
        task_id = progress.add_task("🚀 正在压缩目录...", total=total_tasks)
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for directory in directories:
                dir_path = os.path.join(input_folder, directory)
                output_path = os.path.join(output_folder, directory)
                logger.info(f"📥 提交任务: {dir_path} ➡️ {output_path}.{compression_format}")
                future = executor.submit(compress_directory, dir_path, output_path, compression_format)
                futures[future] = (dir_path, output_path)

            for future in as_completed(futures):
                dir_path, output_path = futures[future]
                try:
                    future.result()
                    logger.info(f"✅ 完成压缩: {dir_path} ➡️ {output_path}.{compression_format}")
                except Exception as e:
                    logger.error(f"❌ 处理目录 {dir_path} 时发生错误: {e}")
                finally:
                    progress.advance(task_id)

        progress.update(task_id, description="[green]🎉 压缩完成[/green]")
        progress.stop()

    logger.info("🎉 所有任务已完成")


if __name__ == "__main__":
    main()
