# -*- coding:utf-8 -*-
# @Project   :pdf2docx
# @FileName  :main.py
# @Time      :2024/9/14 下午3:30
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import os
from configparser import ConfigParser
from concurrent.futures import ProcessPoolExecutor, as_completed
from pdf2docx import Converter
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn, SpinnerColumn
from rich.logging import RichHandler
from rich.console import Console
import logging


def truncate_filename(file_path, max_length=10):
    """截断文件路径中的文件名"""
    file_name = os.path.basename(file_path)
    if len(file_name) > max_length:
        # 截取前7个字符和后7个字符
        return f"{file_name[:7]}...{file_name[-7:]}"
    return file_name


def pdf_to_word(pdf_file_path, word_file_path):
    """将PDF文件转换为Word文件，返回转换结果"""
    try:
        # 禁用所有日志输出
        logging.disable(logging.CRITICAL)

        # 禁用 'pdf2docx' 库的日志输出
        pdf_logger = logging.getLogger('pdf2docx')
        pdf_logger.setLevel(logging.ERROR)
        pdf_logger.propagate = False  # 防止日志传播到根日志器

        cv = Converter(pdf_file_path)
        cv.convert(word_file_path)
        cv.close()
        return True, f"✅ 转换成功: {truncate_filename(pdf_file_path)} ➡️ {truncate_filename(word_file_path)}"
    except Exception as e:
        return False, f"❌ 转换失败: {truncate_filename(pdf_file_path)}，错误信息: {e}"


def main():
    # 配置控制台
    console = Console()

    # 配置日志器，只在主进程中进行配置
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )
    logger = logging.getLogger("PDFConverter")

    # 禁用 'pdf2docx' 库在主进程中的日志输出
    logging.getLogger('pdf2docx').setLevel(logging.ERROR)
    logging.getLogger('pdf2docx').propagate = False  # 防止日志传播到根日志器

    # 读取配置文件
    config_parser = ConfigParser()
    config_parser.read("config.cfg")
    config = config_parser["default"]

    pdf_folder = config["pdf_folder"]
    word_folder = config["word_folder"]
    max_workers = int(config["max_worker"])

    # 检查输出文件夹是否存在，不存在则创建
    if not os.path.exists(word_folder):
        os.makedirs(word_folder)

    # 获取所有PDF文件
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]
    if not pdf_files:
        logger.error(f"❌ 未在目录 {pdf_folder} 中找到任何 PDF 文件。")
        return

    total_files = len(pdf_files)

    # 使用Rich进度条
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

    with progress:
        task_id = progress.add_task("🚀 开始转换 PDF 文件...", total=total_files)
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for pdf_file in pdf_files:
                pdf_file_path = os.path.join(pdf_folder, pdf_file)
                word_file_path = os.path.join(word_folder, os.path.splitext(pdf_file)[0] + ".docx")

                # 提交任务并记录future对象
                future = executor.submit(pdf_to_word, pdf_file_path, word_file_path)
                futures[future] = pdf_file_path

                # 日志记录任务提交
                logger.info(f"📥 提交任务: {truncate_filename(pdf_file_path)} ➡️ {truncate_filename(word_file_path)}")

            # 处理任务完成后的进度更新和日志记录
            for future in as_completed(futures):
                pdf_file_path = futures[future]
                success, message = future.result()
                if success:
                    logger.info(message)
                else:
                    logger.error(message)
                progress.advance(task_id)

    progress.update(task_id, description="[green]🎉 所有 PDF 文件转换完成！[/green]")
    logger.info("🎉 所有文件已转换完成。")


if __name__ == "__main__":
    main()
