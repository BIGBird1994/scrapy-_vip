# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import logging


class VipPipeline(object):
    logger = logging.getLogger(__name__)

    def __init__(self):
        try:
            url = 'localhost'
            port = 27017
            connection = MongoClient(url, port)
            self.db = 'vip'
            self.col = 'detail_info'
            db = connection[self.db]
            self.collection = db[self.col]
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            self.collection.update({"product_id":item['product_id']},dict(item),True)
            # self.collection.insert(dict(item))
            return item
        except Exception as e:
            self.logger.info("%s" % e)
