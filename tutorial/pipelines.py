# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sqlite3
from scrapy.utils.serialize import ScrapyJSONEncoder


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class CsvWritePipeline(object):
    '''
    结果存储：.csv文件，每一行的数据是[url, title, content]
    '''

    def __init__(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.result_dir = os.path.join(cur_dir, '..', 'result')
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

    def process_item(self, item, spider):
        _encoder = ScrapyJSONEncoder()
        file_name = os.path.join(self.result_dir, 'news_data.csv')
        with open(file_name, 'a+', encoding='utf-8', newline='') as f:
            f.writelines("{}\n".format(_encoder.encode(item)))
        return item


class UrlSavePipeline(object):
    '''
    结果存储：.csv文件，每一行的数据是[url, title, content]
    '''

    def __init__(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.result_dir = os.path.join(cur_dir, '..', 'result')
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

    def process_item(self, item, spider):
        _encoder = ScrapyJSONEncoder()
        file_name = os.path.join(self.result_dir, 'news_data_url.csv')
        with open(file_name, 'a+', encoding='utf-8', newline='') as f:
            f.writelines("{}\n".format(_encoder.encode(item['page_url'])))
        return item


class SQLitePipeline(object):
    '''写入sqlite'''

    def __init__(self):
        self.conn = sqlite3.connect('news.db')

    def process_item(self, item, spider):
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS news_info(
            data_id integer PRIMARY KEY autoincrement,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            link TEXT NOT NULL,
            page_url TEXT NOT NULL,
            publish_time TEXT NOT NULL,
            crawl_time TEXT NOT NULL,
            source TEXT NOT NULL,
            page_type TEXT NOT NULL)"""
        )
        self.conn.execute("""INSERT INTO news_info VALUES ({}, {}, {}, {}, {}, {}, {}, {});""".format(
            item['title'], item['content'], item['link'], item['page_url'], item['publish_time'],
            item['crawl_time'], item['source'], item['page_type'])
        )
        self.conn.commit()
        self.conn.close()
        return item


class DefaultValuesPipeline(object):
    """默认值填充"""
    def process_item(self, item, spider):
        item.setdefault('title', '')
        item.setdefault('content', '')
        item.setdefault('link', '')
        item.setdefault('page_url', '')
        item.setdefault('publish_time', '')
        # item.setdefault('crawl_time', '')
        item.setdefault('source', '')
        item.setdefault('page_type', '')
        return item
