import scrapy
import re
import redis
import time
import logging
from ..items import VipItem
from scrapy import Request
from pymongo import MongoClient
from ..fetch_proxy import FetchProxy
from scrapy.exceptions import CloseSpider

class spider(scrapy.Spider):
    name = 'vip_detail_spider_2'
    start_urls = ['https://www.vip.com/']
    detail_url = 'https://detail.vip.com/detail-{brandId}-{productId}.html'
    logger = logging.getLogger(__name__)
    # f = FetchProxy()

    def __init__(self):
        conn = MongoClient(host='localhost', port=27017)
        db = conn['vip']
        self.col = db['detail_info']

    def parse(self, response):
        try:
            cursor = self.col.find({"images.url":"//s2.vipstatic.com/img/share/blank.png"},no_cursor_timeout=True)
            for data in cursor.batch_size(10):
                print(data)
                item = VipItem()
                item['cat_id'] = data['cat_id']
                yield Request(data['url'],meta={"item":item},callback=self.parse_detail)
        except Exception as e:
            self.logger.info("%s" % e)

    def parse_detail(self,response):
        # proxy = response.meta['proxy']
        item = response.meta['item']
        if not response.status == 200:
            print(response.status)
            raise CloseSpider("<------- baned!!! ------->")
        else:
            try:
                item['name'] = response.xpath('//span[@class="pro-title-name"]/text()').extract_first(default=response.xpath('//p[@class="pib-title-detail"]/@title').extract_first()).replace("\r\n","").strip()
                brand = {}
                brand['name'] = response.xpath('//span[@class="pro-title-brand"]/text()').extract_first(default=response.xpath('//p[@class="pib-title-class"]/text()').extract_first()).replace("\r\n","").strip()
                brand['id'] = re.findall('detail-(\d+)-',response.url)[0]
                item['brand'] = brand
                images = []
                for data in response.xpath('//div[@class="pic-slider-wrap"]/div'):
                    img = {}
                    img['url'] = data.xpath('img/@data-original').extract_first()
                    img['md5'] = '********************************'
                    images.append(img)
                if not images:
                    img = {}
                    img['url'] = response.xpath('//div[@class="slideshow-img-box"]/img/@data-original').extract_first()
                    img['md5'] = '********************************'
                    images.append(img)
                item['images'] = images
                item['price'] = response.xpath('//span[@id="J-sale-price"]/text()').extract_first(default=response.xpath('//em[@class="J-price"]/text()').extract_first())
                specification = []
                for data in response.xpath('//ul[@class="g-parameter-table g-parameter-table-add"]/li'):
                    k = data.xpath('span[1]/text()').extract()
                    v = data.xpath('span[2]/text()').extract()
                    for i in range(len(k)):
                        spec = {}
                        spec['key'] = str(k[i]).replace('：','').strip()
                        spec['value'] = str(v[i]).replace('：','').replace('\n','').strip()
                        specification.append(spec)
                item['specification'] = specification
                if not item['specification']:
                    for data in response.xpath('//table[@class="dc-table fst"]/tbody/tr'):
                        k = data.xpath('th/text()').extract()
                        v = data.xpath('td/text()').extract()
                        for i in range(len(k)):
                            spec = {}
                            spec['key'] = str(k[i]).replace('：', '').strip()
                            spec['value'] = str(v[i]).replace('：', '').replace('\n', '').strip()
                            specification.append(spec)
                    item['specification'] = specification
                item['product_id'] = re.search(r'-(\d+).html',response.url).group(1)
                item['time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                item['url'] = response.url
                self.logger.info("%s" % item)
                # self.f.save_proxy(proxy=proxy)
                # self.logger.info("<--------- save proxy %s to redis -------->" % proxy)
                yield item
            except Exception as e:
                self.logger.error("%s",e)









