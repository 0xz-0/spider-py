# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime

# from scrapy.loader.processors import MapCompose, TakeFirst, Join


class _CrawlabItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    crawl_url = scrapy.Field(
        # 指定任意函数对值进行处理
        # 指定 lambda
        # input_processor=MapCompose(lambda x: 'Question:' + x ),
        # 指定处理函数
        # input_processor=MapCompose(lambda x: x.strip()),
        # 使用 TakeFirst 来取到第一个值进行返回
        # output_processor=TakeFirst(),
        serializer=str,
    )
    """爬取链接"""
    crawl_time = scrapy.Field(
        name="crawl_time",
        # default_value=datetime.now(),# 此行无效！！！
        serializer=lambda x: x.strftime("%Y-%m-%d %H:%M:%S"),
    )
    """爬取时间"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['crawl_time'] = datetime.now()


class ClcItem(_CrawlabItem):
    order = scrapy.Field(serializer=str)
    """当页序号"""
    no = scrapy.Field(serializer=str)
    """分类号"""
    title = scrapy.Field(serializer=str)
    """标题"""
    parent_no = scrapy.Field(serializer=str)
    """父分类号"""


class QhdmItem(_CrawlabItem):
    code = scrapy.Field(serializer=str)
    """统计用区划代码"""
    name = scrapy.Field(serializer=str)
    """名称"""
    level = scrapy.Field(serializer=str)
    """级别"""
    classification_code = scrapy.Field(serializer=str)
    """城乡分类代码"""
    parent_code = scrapy.Field(serializer=str)
    """上级代码"""


class IntelCpuRankItem(_CrawlabItem):
    rank = scrapy.Field(serializer=int)
    """当前排名"""
    processor = scrapy.Field(serializer=str)
    """处理器名称"""
    points = scrapy.Field(serializer=int)
    """评分"""
    cores = scrapy.Field(serializer=str)
    """核心数"""
    hertz = scrapy.Field(serializer=str)
    """主频"""
    tdp = scrapy.Field(serializer=str)
    """热设计功耗"""
    release_date = scrapy.Field(serializer=str)
    """发布日期"""
