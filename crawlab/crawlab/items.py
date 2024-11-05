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
        self["crawl_time"] = datetime.now()


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


class LunarCalendarDescriptionItem(_CrawlabItem):
    item_id = scrapy.Field(serializer=int)
    """ID"""
    type = scrapy.Field(serializer=str)
    """类型"""
    name = scrapy.Field(serializer=str)
    """名称"""
    title = scrapy.Field(serializer=str)
    """标题"""
    description = scrapy.Field(serializer=list)
    """描述"""


class LunarCalendarDailyItem(_CrawlabItem):
    date = scrapy.Field(serializer=str)
    """日期"""
    year = scrapy.Field(serializer=int)
    """年"""
    month = scrapy.Field(serializer=int)
    """月"""
    day = scrapy.Field(serializer=int)
    """日"""
    week = scrapy.Field(serializer=str)
    """星期"""
    lunar_date = scrapy.Field(serializer=str)
    """农历日期"""
    lunar_year = scrapy.Field(serializer=str)
    """农历年"""
    lunar_month = scrapy.Field(serializer=str)
    """农历月"""
    lunar_day = scrapy.Field(serializer=str)
    """农历日"""
    festivals = scrapy.Field(serializer=list)
    """节日"""
    suits = scrapy.Field(serializer=list)
    """宜"""
    avoids = scrapy.Field(serializer=list)
    """忌"""

    # 以下为附加字段
    lunar_zodiac = scrapy.Field(serializer=str)
    """生肖"""
    pengzu_baiji = scrapy.Field(serializer=str)
    """彭祖百忌"""
    year_five_elements = scrapy.Field(serializer=str)
    """年五行"""
    month_five_elements = scrapy.Field(serializer=str)
    """月五行"""
    day_five_elements = scrapy.Field(serializer=str)
    """日五行"""
    julian_day = scrapy.Field(serializer=float)
    """儒略日"""
    clash = scrapy.Field(serializer=str)
    """冲"""
    six_days = scrapy.Field(serializer=str)
    """六曜"""
    lunar_constellation = scrapy.Field(serializer=str)
    """星座"""
    fetal_god = scrapy.Field(serializer=str)
    """胎神占方"""
    season = scrapy.Field(serializer=str)
    """季节"""
    lunar_mansion = scrapy.Field(serializer=str)
    """星宿"""
    solar_terms = scrapy.Field(serializer=str)
    """节气"""
    islamic_calendar = scrapy.Field(serializer=str)
    """伊斯兰历"""
    sha = scrapy.Field(serializer=str)
    """煞"""
    twelve_gods = scrapy.Field(serializer=str)
    """十二神"""
    payload = scrapy.Field(serializer=dict)
    """剩余数据"""


class BaiduHistoryTodayItem(_CrawlabItem):
    date = scrapy.Field(serializer=str)
    """日期"""
    year = scrapy.Field(serializer=int)
    """年"""
    title = scrapy.Field(serializer=str)
    """标题"""
    desc = scrapy.Field(serializer=str)
    """描述"""
    festival = scrapy.Field(serializer=str)
    """节日"""
    link = scrapy.Field(serializer=str)
    """链接"""
    type = scrapy.Field(serializer=str)
    """类型"""
    cover = scrapy.Field(serializer=bool)
    """封面"""
    recommend = scrapy.Field(serializer=bool)
    """推荐"""
    payload = scrapy.Field(serializer=dict)
    """剩余数据"""
