#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""启动命令"""

__author__ = 'yp'


import os

os.system("scrapy crawl news")  # 启动爬取任务
os.chdir("newscollecter")
os.system("""scrapy shell \"https://finance.sina.com.cn/\"""")  # 交互式

import os
os.chdir('newscollecter')
os.system("start /b scrapyd")
os.system("start /b spiderkeeper")
os.system("scrapyd-deploy -p news -v 1.0 --build-egg news.egg")
