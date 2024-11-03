# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    crawl_url = scrapy.Field(
        serializer=str,
    )
    """爬取链接"""
    crawl_time = scrapy.Field(
        name="crawl_time",
        serializer=lambda x: x.strftime("%Y-%m-%d %H:%M:%S"),
    )
    """爬取时间"""


class StockBoardItem(TencentItem):
    code = scrapy.Field(serializer=str)
    """股票代码"""
    name = scrapy.Field(serializer=str)
    """股票名称"""
    zxj = scrapy.Field(serializer=str)
    """最新价"""
    zdf = scrapy.Field(serializer=str)
    """涨跌幅"""
    zd = scrapy.Field(serializer=str)
    """涨跌"""
    hsl = scrapy.Field(serializer=str)
    """换手率"""
    lb = scrapy.Field(serializer=str)
    """量比"""
    zf = scrapy.Field(serializer=str)
    """振幅"""
    volume = scrapy.Field(serializer=str)
    """成交量"""
    turnover = scrapy.Field(serializer=str)
    """成交额(万元)"""
    pe_ttm = scrapy.Field(serializer=str)
    """市盈率(TTM)"""
    pn = scrapy.Field(serializer=str)
    """市净率"""
    zsz = scrapy.Field(serializer=str)
    """总市值"""
    ltsz = scrapy.Field(serializer=str)
    """流通市值"""
    state = scrapy.Field(serializer=str)
    """状态"""
    speed = scrapy.Field(serializer=str)
    """涨速"""
    zdf_y = scrapy.Field(serializer=str)
    """年涨跌幅"""
    zdf_d5 = scrapy.Field(serializer=str)
    """5日涨跌幅"""
    zdf_d10 = scrapy.Field(serializer=str)
    """10日涨跌幅"""
    zdf_d20 = scrapy.Field(serializer=str)
    """20日涨跌幅"""
    zdf_d60 = scrapy.Field(serializer=str)
    """60日涨跌幅"""
    zdf_w52 = scrapy.Field(serializer=str)
    """52周涨跌幅"""
    zljlr = scrapy.Field(serializer=str)
    """主力净流入"""
    zllr = scrapy.Field(serializer=str)
    """主力流入"""
    zllc = scrapy.Field(serializer=str)
    """主力流出"""
    zllr_d5 = scrapy.Field(serializer=str)
    """5日主力流入"""
    zllc_d5 = scrapy.Field(serializer=str)
    """5日主力流出"""
    stock_type = scrapy.Field(serializer=str)
    """股票类型"""
    payload = scrapy.Field(serializer=dict)
    """扩展剩余字段"""
