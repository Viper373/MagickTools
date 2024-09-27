# -*- coding:utf-8 -*-
# @Project   :dp_project
# @FileName  :test.py
# @Time      :2024/9/27 下午3:19
# @Author    :Zhangjinzhao
# @Software  :PyCharm
# 创建一个全局的 RichLogger 实例
from decorator_utils import RichLogger

rich_logger = RichLogger()


# 示例用法
@rich_logger
def loasa(x, y):
    """
    加法函数
    """
    rich_logger.info("这是一个除法")  # 记录加法日志
    return f"加法结果: {x / y}"  # 返回加法结果


# 测试装饰器
if __name__ == "__main__":
    try:
        result = loasa(5, 0)
    except Exception as e:
        pass
