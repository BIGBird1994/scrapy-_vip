import scrapy
import re
import json
from ..items import VipItem
from scrapy import Request

class spider(scrapy.Spider):
    name = 'category_spider'
    start_urls = ['https://category.vip.com/ajax/getCategory.php?callback=getCategory&tree_id=117']

    def parse(self, response):
        resp = str(response.text).replace('getCategory(','').replace(')','')
        datas = json.loads(resp)
        for data_1 in datas['data']:
            item = VipItem()
            item['cate_id'] = data_1['cate_id']
            item['cate_type'] = data_1['cate_type']
            item['cate_name'] = data_1['cate_name']
            item['url'] = data_1['url']
            print(item)
            yield item
            for data_2 in data_1['children']:
                item['cate_id'] = data_2['cate_id']
                item['cate_type'] = data_2['cate_type']
                item['cate_name'] = data_2['cate_name']
                item['url'] = data_2['url']
                print(item)
                yield item
                for data_3 in data_2['children']:
                    item['cate_id'] = data_3['cate_id']
                    item['cate_type'] = data_3['cate_type']
                    item['cate_name'] = data_3['cate_name']
                    item['url'] = data_3['url']
                    print(item)
                    yield item