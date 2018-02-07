# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json

from scrapy.exporters import CsvItemExporter
from scrapy import signals


class ZhiyouCsvPipeline(object):
    def __init__(self):
        self.file = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        # print('我要开始了'*10)
        # print(hash(spider))
        file = open('zhiyouinfo.csv', 'wb')
        self.file[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        # print('我要结束了'*10)
        self.exporter.finish_exporting()
        file = self.file.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
