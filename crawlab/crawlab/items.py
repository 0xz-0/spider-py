# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# from scrapy.loader.processors import MapCompose, TakeFirst, Join


class CrawlabItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ClcItem(scrapy.Item):
    order = scrapy.Field(serializer=str)
    """当页序号"""
    no = scrapy.Field(
        # 指定任意函数对值进行处理
        # 指定 lambda
        # input_processor=MapCompose(lambda x: 'Question:' + x ),
        # 指定处理函数
        # input_processor=MapCompose(lambda x: x.strip()),
        # 使用 TakeFirst 来取到第一个值进行返回
        # output_processor=TakeFirst(),
        serializer=str,
    )
    """分类号"""
    title = scrapy.Field(serializer=str)
    """标题"""
    parent_no = scrapy.Field(serializer=str)
    """父分类号"""
    crawl_url = scrapy.Field(serializer=str)
    """爬取链接"""
