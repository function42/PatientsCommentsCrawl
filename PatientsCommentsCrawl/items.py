# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PatientscommentscrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CommentItem(scrapy.Item):
    doctor_id = scrapy.Field()
    cure = scrapy.Field()
    attitude = scrapy.Field()
    content = scrapy.Field()