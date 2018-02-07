# -*- coding: utf-8 -*-
import scrapy
import time

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from zhiyou.items import ZhiyouItem


class ZhiyoujiSpider(CrawlSpider):
    name = 'zhiyouji'
    allowed_domains = ['jobui.com']
    start_urls = ['http://www.jobui.com/cmp?area=%E5%85%A8%E5%9B%BD&sortField=sortTime']

    rules = (
        Rule(LinkExtractor(allow=r'/company/\d+/$'), callback='parse_detail_page', follow=True),
        Rule(LinkExtractor(allow=r'/cmp.*?sortTime&n=\d+'), follow=True),

    )

    def parse_detail_page(self, response):
        if response.status != 200:
            return None

        item = ZhiyouItem()

        item['url'] = response.url
        item['company_id'] = item['url'].split('/')[-2]
        item['crawl_time'] = time.ctime()

        item['company_name'] = response.xpath('//*[@id="companyH1"]/a/text()').extract_first()
        item['company_brand_url'] = response.xpath('//div[@class="company-logo"]//img/@src').extract_first()
        item['good_num'] = response.xpath('//*[@id="goodNum"]/text()').extract_first()
        item['general_num'] = response.xpath('//*[@id="generalNum"]/text()').extract_first()

        content = response.xpath('//div[@class="company-logo"]/following-sibling::div[1]//div[@class ="fl ele fs16 gray9 mr10"]/text()').extract_first()
        if content is not None:
            con_list = content.split()
            item['view_num'] = con_list[0].split('人')[0][:-1:1] if len(con_list) > 0 else None
            item['view_num'] = float(item['view_num'])
            item['evaluation_num'] = con_list[2] if len(con_list) > 2 else None
            item['attention_num'] = con_list[4] if len(con_list) > 4 else None

        item['star_rank'] = response.xpath('//div[@class="star fl"]/div/@title').extract_first()
        item['brief'] = response.xpath('//div[@class="company-head-information"]//p[@class="fs16 gray9 sbox company-short-intro"]/text()').extract_first()

        investment_and_people = response.xpath('//div[@class="intro"]/div[2]//dd[1]/text()').extract_first()
        try:
            item['company_investment_status'] = investment_and_people.split('/')[0].strip()
        except:
            print('无法获取到公司投资状态')
            item['company_investment_status'] = None
        try:
            item['company_people_num'] = investment_and_people.split('/')[1].strip()
        except:
            print('无法获取到公司人数')
            item['company_people_num'] = None

        # 采集公司行业信息
        ind_list = response.xpath('//dd[@class="comInd"]/a')
        ind_con = []
        for ind in ind_list:
            ind_con.append(ind.xpath('./text()').extract_first())
        item['company_industry'] = ind_con

        item['company_shortname'] = response.xpath('//dd[@class="gray3"]/text()').extract_first()

        # 获取公司概况 company_profile
        profile_list = response.xpath('//*[@id="textShowMore"]/text()').extract()
        profile_con = ''
        for profile in profile_list:
            profile_con += profile.strip()
        item['company_profile'] = profile_con

        # 获取公司的工商信息
        business_url = 'http://www.jobui.com/async/company_info_businessInfo/' + item['company_id'] + '.html'
        yield scrapy.Request(url=business_url, callback=self.parse_business_page, priority=1, meta={'item': item})

    def parse_business_page(self, response):
        # print(response.status, '-'*100)
        item = response.meta['item']

        item['business_info_url'] = response.url

        info_node = response.xpath('/html/body/div/div[2]/div')

        item['credit_code'] = info_node.xpath('./p[1]/span[2]/text()').extract_first()
        item['registered_capital'] = info_node.xpath('./p[6]/span[2]/text()').extract_first()
        item['manage_status'] = info_node.xpath('./p[2]/span[2]/text()').extract_first()
        item['legal_representative'] = info_node.xpath('./p[3]/span[2]/text()').extract_first()
        item['establish_date'] = info_node.xpath('./p[4]/span[2]/text()').extract_first()
        item['business_expire'] = info_node.xpath('./p[5]/span[2]/text()').extract_first()
        item['registered_address'] = info_node.xpath('./p[6]/span[2]/text()').extract_first()

        yield item






