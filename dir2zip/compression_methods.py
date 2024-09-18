# -*- coding:utf-8 -*-
# @Project   :dir2zip
# @FileName  :compression_methods.py
# @Time      :2024/8/30 上午10:17
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import shutil
import subprocess
import logging


def is_tool_available(tool_name):
    """检查命令行工具是否可用"""
    try:
        subprocess.run([tool_name, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        logging.error(f"工具 {tool_name} 未安装或不可用，请安装后重试。")
        return False


def dir2zip(directory_path, output_path):
    try:
        shutil.make_archive(output_path, 'zip', directory_path)
        logging.info(f"成功压缩 {directory_path} 为 {output_path}.zip")
    except Exception as e:
        logging.error(f"压缩 {directory_path} 时发生错误: {e}")


def dir27z(directory_path, output_path):
    if not is_tool_available('7z'):
        return  # 工具不可用时跳过此任务
    try:
        subprocess.run(['7z', 'a', f'{output_path}.7z', directory_path], check=True)
        logging.info(f"成功压缩 {directory_path} 为 {output_path}.7z")
    except subprocess.CalledProcessError as e:
        logging.error(f"7z 压缩 {directory_path} 时发生错误: {e}")


def dir2rar(directory_path, output_path):
    if not is_tool_available('rar'):
        return  # 工具不可用时跳过此任务
    try:
        subprocess.run(['rar', 'a', f'{output_path}.rar', directory_path], check=True)
        logging.info(f"成功压缩 {directory_path} 为 {output_path}.rar")
    except subprocess.CalledProcessError as e:
        logging.error(f"rar 压缩 {directory_path} 时发生错误: {e}")


def dir2tar(directory_path, output_path):
    try:
        shutil.make_archive(output_path, 'tar', directory_path)
        logging.info(f"成功压缩 {directory_path} 为 {output_path}.tar")
    except Exception as e:
        logging.error(f"压缩 {directory_path} 时发生错误: {e}")


def dir2gztar(directory_path, output_path):
    try:
        shutil.make_archive(output_path, 'gztar', directory_path)
        logging.info(f"成功压缩 {directory_path} 为 {output_path}.tar.gz")
    except Exception as e:
        logging.error(f"压缩 {directory_path} 时发生错误: {e}")


def dir2bz2(directory_path, output_path):
    try:
        shutil.make_archive(output_path, 'bz2', directory_path)
        logging.info(f"成功压缩 {directory_path} 为 {output_path}.tar.bz2")
    except Exception as e:
        logging.error(f"压缩 {directory_path} 时发生错误: {e}")


def dir2bztar(directory_path, output_path):
    try:
        shutil.make_archive(output_path, 'bztar', directory_path)
        logging.info(f"成功压缩 {directory_path} 为 {output_path}.tar.bz2")
    except Exception as e:
        logging.error(f"压缩 {directory_path} 时发生错误: {e}")


def dir2xztar(directory_path, output_path):
    try:
        shutil.make_archive(output_path, 'xztar', directory_path)
        logging.info(f"成功压缩 {directory_path} 为 {output_path}.tar.xz")
    except Exception as e:
        logging.error(f"压缩 {directory_path} 时发生错误: {e}")


def get_compression_method(method):
    """根据用户输入返回对应的压缩方法"""
    method_map = {
        'zip': dir2zip,
        '7z': dir27z,
        'rar': dir2rar,
        'tar': dir2tar,
        'gz': dir2gztar,
        'gztar': dir2gztar,
        'bz2': dir2bztar,
        'bztar': dir2bztar,
    }
    return method_map.get(method.lower())
