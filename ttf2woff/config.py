# -*- coding:utf-8 -*-
# @Project   :ttf2woff
# @FileName  :config.py
# @Time      :2024/9/14 下午3:16
# @Author    :Zhangjinzhao
# @Software  :PyCharm

# 输入字体文件所在的目录
TTF_DIR = 'ttf'

# 输出字体文件保存的目录
WOFF_DIR = 'woff'

# 输出格式，支持 'woff' 或 'woff2'
OUTPUT_FORMATS = ['woff', 'woff2']

# 子集化所需的字符，包含所有数字和字母，以及指定的中文短语
SUBSET_CHARS = (
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    '不想上班丨星期一'
    '为什么要上班丨星期二'
    '什么时候下班丨星期三'
    '只要忙过今天丨星期四'
    '炸了公司大楼丨星期五'
    '原谅世界丨星期六'
    '混吃等死丨星期日'
    '仲春二月'
    '暮春三月'
    '孟夏四月'
    '仲夏五月'
    '盛夏六月'
    '孟秋七月'
    '桂秋八月'
    '晚秋九月'
    '霜华十月'
    '葭花冬月'
    '始春元月'
    '年日号'
)
