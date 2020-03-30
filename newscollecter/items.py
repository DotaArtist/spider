# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()  # 标题
    content = scrapy.Field()  # 内容

    link = scrapy.Field()  # 点击链接
    page_url = scrapy.Field()  # 文章地址

    publish_time = scrapy.Field()  # 发布时间
    crawl_time = scrapy.Field()  # 爬取时间

    source = scrapy.Field()  # 信息来源
    page_type = scrapy.Field()  # 页面类型
