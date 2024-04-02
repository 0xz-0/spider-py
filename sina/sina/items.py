# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HotSearchHotGovItem(scrapy.Item):
    task_id = scrapy.Field(serializer=int)
    """任务ID"""
    mid = scrapy.Field(serializer=str)
    """微博ID"""
    note = scrapy.Field(serializer=str)
    """标题"""
    stime = scrapy.Field(serializer=int)
    """发布时间"""
    payload = scrapy.Field(serializer=dict)
    """剩余数据"""


class HotSearchRealTimeItem(scrapy.Item):
    task_id = scrapy.Field(serializer=int)
    """任务ID"""
    mid = scrapy.Field(serializer=str)
    """微博ID"""
    note = scrapy.Field(serializer=str)
    """标题"""
    rank = scrapy.Field(serializer=int)
    """排序"""
    category = scrapy.Field(serializer=str)
    """类别"""
    label_name = scrapy.Field(serializer=str)
    """标签"""
    hot_num = scrapy.Field(serializer=int)
    """热度"""
    onboard_time = scrapy.Field(serializer=int)
    """上榜时间"""
    payload = scrapy.Field(serializer=dict)
    """剩余数据"""


class EntertainmentItem(scrapy.Item):
    task_id = scrapy.Field(serializer=int)
    """任务ID"""
    word = scrapy.Field(serializer=str)
    """标题"""
    hot_rank_position = scrapy.Field(serialize=int)
    """当前榜单排位"""
    category = scrapy.Field(serializer=str)
    """类别"""
    hot_num = scrapy.Field(serializer=int)
    """热度"""
    onboard_time = scrapy.Field(serializer=int)
    """上榜时间"""
    payload = scrapy.Field(serializer=dict)
    """剩余数据"""


class NewsItem(scrapy.Item):
    task_id = scrapy.Field(serializer=int)
    """任务ID"""
    topic = scrapy.Field(serializer=str)
    """话题"""
    rank = scrapy.Field(serialize=int)
    """当前榜单排位"""
    read = scrapy.Field(serializer=int)
    """阅读量"""
    category = scrapy.Field(serializer=str)
    """类别"""
    summary = scrapy.Field(serializer=str)
    """简要"""
    claim = scrapy.Field(serializer=str)
    """宣发"""
    payload = scrapy.Field(serializer=dict)
    """剩余数据"""
