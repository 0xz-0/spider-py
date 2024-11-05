import time
import scrapy
from typing import List, Optional, Set
from scrapy.http import Response
import logging

from ..items import BaiduHistoryTodayItem


class BaiduHistoryTodaySpider(scrapy.Spider):
    name = "baidu_history_today"
    allowed_domains = ["baidu.com"]
    custom_settings = {
        "ITEM_PIPELINES": {"crawlab.pipelines.BaiduHistoryTodayPipeline2Postgres": 300},
        "ROBOTSTXT_OBEY": False,
    }
    url_template = "https://baike.baidu.com/cms/home/eventsOnHistory/{month:02d}.json?_={timestamp}"

    def start_requests(self):
        yield scrapy.Request(
            url=self.url_template.format(month=1, timestamp=int(time.time())),
            callback=self.parse,
            meta={"month": 1},
        )

    def parse(self, response: Response):
        self.logger.info(msg="开始解析: %s" % response.url)
        data: dict[str, any] = response.json()
        for day, contents in data.get(f"{response.meta['month']:02d}", {}).items():
            day: str  # 形如 "0101"
            for content in contents:
                content: dict[str, any]
                item = BaiduHistoryTodayItem(
                    date=day,
                    year=content.pop("year"),  # 年份
                    title=content.pop("title"),  # 标题
                    desc=content.pop("desc"),  # 描述
                    festival=content.pop("festival"),  # 节日
                    link=content.pop("link"),  # 链接
                    type=content.pop("type"),  # 类型
                    cover=bool(content.pop("cover")),  # 封面
                    recommend=bool(content.pop("recommend")),  # 推荐
                    payload=content,
                    crawl_url=response.url,
                )
                yield item

        if response.meta["month"] < 12:
            next_month: int = response.meta["month"] + 1
            yield scrapy.Request(
                url=self.url_template.format(
                    month=next_month, timestamp=int(time.time())
                ),
                callback=self.parse,
                meta={"month": next_month},
            )
