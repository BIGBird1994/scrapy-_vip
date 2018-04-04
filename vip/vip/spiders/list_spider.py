import scrapy
import pymongo
import re
import json
import logging
from urllib import request
from ..items import VipItem
from scrapy import Request


class spider(scrapy.Spider):
      name = 'list_spider'
      start_urls = ['https://category.vip.com/ajax/getCategory.php?callback=getCategory&tree_id=117']
      logger = logging.getLogger(__name__)

      def parse(self, response):
          conn = pymongo.MongoClient(host='localhost', port=27017)
          db = conn['vip']
          col = db['category_info_2']
          for data in col.find({'cate_type':'3'}):
              item = VipItem()
              item['cat_id'] = data['cate_id']
              url = 'https://category.vip.com/{}'.format(data['url'])
              yield Request(url,meta={"item":item},callback=self.parse_next)

      def parse_next(self,response):
          try:
              item = response.meta['item']
              ids = re.search(r'"productIds":(.*),"cateName"',response.text).group(1)
              str = ids.replace('[','').replace(']','').strip()
              a = str.split(',')
              list_1 = a[0:49]
              list_2 = a[50:-1]
              param_1 = ','.join(list_1)
              param_2 = ','.join(list_2)
              param_1 = request.quote(param_1)
              param_2 = request.quote(param_2)
              url_1 = 'https://category.vip.com/ajax/mapi.php?service=product_info&callback=categoryMerchandiseInfo1&productIds={}&functions=brandShowName%2CsurprisePrice%2CpcExtra&warehouse=VIP_BJ&mobile_platform=1&app_name=shop_pc&app_version=4.0'.format(param_1)
              url_2 = 'https://category.vip.com/ajax/mapi.php?service=product_info&callback=categoryMerchandiseInfo2&productIds={}&functions=brandShowName%2CsurprisePrice%2CpcExtra&warehouse=VIP_BJ&mobile_platform=1&app_name=shop_pc&app_version=4.0'.format(param_2)
              yield Request(url_1,meta={"item":item},callback=self.parse_detail)
              yield Request(url_2,meta={"item":item},callback=self.parse_detail)
              next_page = response.xpath('//a[@mars_sead="te_onsale_filterlist_nextpage_btn"]/@href').extract()
              if next_page:
                  print(next_page)
                  self.logger.info("<-------- fetch next page %s --------->" % next_page[0])
                  url = 'https://category.vip.com{}'.format(next_page[0])
                  yield Request(url,meta={"item":item},callback=self.parse_next)
          except Exception as e:
              self.logger.info("%s" % e)

      def parse_detail(self,response):
          try:
              item = response.meta['item']
              resp = str(response.text).replace('categoryMerchandiseInfo2(','').replace(')','').replace('categoryMerchandiseInfo1(','')
              datas = json.loads(resp)
              count = 0
              for data in datas['data'].get('products'):
                  count += 1
                  item['product_info'] = data
                  self.logger.info("%s %s" %(item,count))
                  yield item
          except Exception as e:
              self.logger.info("%s" % e)