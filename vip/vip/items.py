# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field,Item

class VipItem(scrapy.Item):
    time = Field()
    brand = Field()
    url = Field()
    cate_id = Field()
    cate_type = Field()
    cate_name = Field()
    product_id = Field()
    product_info = Field()
    total_num = Field()
    third_category_id = Field()
    second_category = Field()
    price_json_list = Field()
    comment_json = Field()
    comment_id = Field()
    detail_information = Field()
    cat_name = Field()
    cat_id = Field()
    level = Field()
    id = Field()
    page_num = Field()
    item_num = Field()
    parent_id = Field()
    price = Field()
    num = Field()
    price_json = Field()
    html_str = Field()
    fail_url = Field()
    total_comment = Field()
    title = Field()
    category = Field()
    shop = Field()
    detail = Field()
    specification = Field()
    images = Field()
    name = Field()
    pass
