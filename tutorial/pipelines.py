# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os, csv


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
        file_name = os.path.join(self.result_dir, 'dfld.csv')
        with open(file_name, 'a+', encoding='utf-8', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow([item['url'], item['title'], item['content']])
        return item
