# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BcsdbookingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    inmate = scrapy.Field()
    bookingdate = scrapy.Field()
    totalbondamount = scrapy.Field()
    chargedescrption = scrapy.Field()
    offensedate = scrapy.Field()
    sourceurl = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass