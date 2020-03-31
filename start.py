#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""启动命令"""

__author__ = 'yp'


import os

# 启动单次爬取任务
os.system("scrapy crawl news")


# 交互式调试
# os.system("""scrapy shell \"https://finance.sina.com.cn/\"""")

# spiderkeeper 爬虫监控
# os.chdir('newscollecter')
# os.system("start /b scrapyd")
# os.system("start /b spiderkeeper")
# os.system("scrapyd-deploy -p news -v 1.0 --build-egg news.egg")

# 动态页面环境配置
# os.system("docker pull scrapinghub/splash")
# os.system("docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash")
# os.system("pip install scrapy-splash")
