# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhiyouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    url = scrapy.Field()
    crawl_time = scrapy.Field()
    # 公司名称
    company_name = scrapy.Field()
    # 公司在该网站的id
    company_id = scrapy.Field()
    # 公司图标
    company_brand_url = scrapy.Field()
    # 浏览人数
    view_num = scrapy.Field()
    # 评价人数
    evaluation_num = scrapy.Field()
    # 关注人数
    attention_num = scrapy.Field()
    # 星级
    star_rank = scrapy.Field()
    # 简介
    brief = scrapy.Field()
    # 点赞数
    good_num = scrapy.Field()
    # 一般数
    general_num = scrapy.Field()

    # ##### 概况页面
    # 公司投资情况
    company_investment_status = scrapy.Field()
    # 公司人数
    company_people_num = scrapy.Field()
    # 公司行业
    company_industry = scrapy.Field()
    # 公司简称
    company_shortname = scrapy.Field()
    # 公司概况文字描述
    company_profile = scrapy.Field()

    # ##### 公司的工商信息
    business_info_url = scrapy.Field()
    # 统一信用代码
    credit_code = scrapy.Field()
    # 注册资本
    registered_capital = scrapy.Field()
    # 经营状态
    manage_status = scrapy.Field()
    # 法定代表
    legal_representative = scrapy.Field()
    # 成立日期
    establish_date = scrapy.Field()
    # 营业期限
    business_expire = scrapy.Field()
    # 注册地址
    registered_address = scrapy.Field()
