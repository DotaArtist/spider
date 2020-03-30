#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""启动命令"""

__author__ = 'yp'


import os

os.system("scrapy crawl news")  # 启动爬取任务
os.chdir("tutorial")
os.system("""scrapy shell \"https://finance.sina.com.cn/\"""")  # 交互式
