# -*- coding: utf-8 -*-
import scrapy
import os

class Example1Spider(scrapy.Spider):
    name = 'haodaifu_example1'

    if(not(os.path.exists('./intermediary'))):
        os.mkdir('./intermediary')
        
    def start_requests(self):
        pass
    
    def parse(self, response):
        pass
