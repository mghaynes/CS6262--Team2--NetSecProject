# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Alexa1MItem(scrapy.Item):
    # define the fields for your item here like:
    rank = scrapy.Field()
    url = scrapy.Field()
    encoding = scrapy.Field()
    content = scrapy.Field()
