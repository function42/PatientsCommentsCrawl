# -*- coding: utf-8 -*-
import scrapy
import os
from ..items import CommentItem

# =============================================================================
# 获取疾病 [胆结石] 下所有医生的评论
# =============================================================================
class Example1Spider(scrapy.Spider):
    name = 'haodaifu_example1'

    if(not(os.path.exists('./intermediary'))):
        os.mkdir('./intermediary')
        
    def start_requests(self):
        example_urls = [
                'https://www.haodf.com/jibing/danjieshi.htm'
                ]
        for li in example_urls:
            url = li[:-4] + '/daifu_all_all_all_all_all.htm'
            yield scrapy.Request(url, callback=self.parseDoctors, dont_filter=False)\
       
    def parseDoctors(self, response):
        print(response.url.split('/')[-1])
        doctors = response.css('#disease > div > div.fl.left_con1.self_typeface1 > div.pr25 > ul > li > div > div.doctor_photo_serviceStar')
        for doctor in doctors:
            mainpage_link = doctor.css('div.doctor_photo_serviceStar > div.oh.zoom.lh180 > p > a.blue_a3::attr(href)').extract_first()
            url = response.urljoin(mainpage_link[:-4] + '/jingyan.htm')
            yield scrapy.Request(url, callback=self.parseComment, dont_filter=False)
        
        pages = response.css('div.page_main > div.page_turn > a.page_turn_a')
        if(pages[-2].css('a.page_turn_a::text').extract_first()=='下一页'):
            url = response.urljoin(pages[-2].css('a.page_turn_a::attr(href)').extract_first())
            yield scrapy.Request(url, callback=self.parseDoctors, dont_filter=False)

    def parseComment(self, response):
        print(response.url[30:])
        doctor_id=response.url.split('/')[4].split('.')[0][4:]
        comments = response.css('#comment_content > table.doctorjy')
        for c in comments:
            content = c.css('table > tr > td > table > tr > td.spacejy::text').extract()
            if(content):
                content = ''.join(content).strip()
            if(not(content) or content=='暂无文字分享。'):
                continue
            comment = CommentItem()
            comment['content'] = content
            comment['doctor_id'] = doctor_id
            infos = c.css('table > tr > td.dlemd > table > tbody > tr > td.gray')

            for info in infos:
                if(info.css('td.gray::text').extract_first() == '疗效：'):
                    comment['cure'] = info.css('td > span::text').extract_first()
                elif(info.css('td.gray::text').extract_first() == '态度：'):
                    comment['attitude'] = info.css('td > span::text').extract_first()
                else:
                    pass              
            
            if('cure' not in comment.keys()):
                comment['cure'] = ''

            if('attitude' not in comment.keys()):
                comment['attitude'] = ''
            yield comment
            
        pages = response.css('div.p_bar > a.p_num')
        for page in pages:
            if(page.css('a.p_num::text').extract_first()=='下一页'):
                url = response.urljoin(page.css('a.p_num::attr(href)').extract_first())
                yield scrapy.Request(url, callback=self.parseComment, dont_filter=False)
            