# 新浪搜索榜单

from enum import Enum
import scrapy
from typing import List
from scrapy.http import Response
import logging
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json

from ..utils.database import DBRequestTask
from ..utils.webdriver import driver_executable_path, SeleniumRequest
from ..items import (
    HotSearchRealTimeItem,
    HotSearchHotGovItem,
    EntertainmentItem,
    NewsItem,
)


class _TaskType(Enum):
    rank_hot_search: str = "热搜榜"
    rank_entertainment: str = "文娱榜"
    rank_news: str = "要闻榜"


class RankHotSearchSpider(scrapy.Spider):
    """
    热搜榜
    """

    name = "RankHotSearch"
    custom_settings = {
        "ITEM_PIPELINES": {"sina.pipelines.HotSearchPipeline2Postgres": 300},
        "DOWNLOADER_MIDDLEWARES": {},
        "ROBOTSTXT_OBEY": False,
    }

    allowed_domains: List[str] = ["weibo.com"]
    logger = logging.getLogger(name=__name__)
    task_id = 0

    def start_requests(self):
        req_url: str = "https://weibo.com/ajax/side/hotSearch"
        if not DBRequestTask.table_exists():
            DBRequestTask.create_table()
        self.task_id: int = DBRequestTask.insert(
            name=_TaskType.rank_hot_search.value,
            status=False,
            crawl_url=req_url,
            crawl_time=datetime.now(),
        ).execute()
        yield scrapy.Request(
            url=req_url,
            callback=self.parse,
        )

    def parse(self, response: Response):
        data: dict = response.json().get("data", dict())

        for item in data.get("hotgovs"):
            yield self._parse_hot_gov(item=item)

        for item in data.get("realtime"):
            yield self._parse_realtime(item=item)

    def closed(self, reason):
        DBRequestTask.update(
            status=True,
            reason=str(reason),
        ).where(DBRequestTask.id == self.task_id).execute()
        return

    def _parse_hot_gov(self, item: dict) -> HotSearchHotGovItem:
        return HotSearchHotGovItem(
            task_id=self.task_id,
            mid=item.pop("mid", ""),
            note=item.pop("note", ""),
            stime=item.pop("stime", datetime.now().timestamp()),
            payload=item,
        )

    def _parse_realtime(self, item: dict) -> HotSearchRealTimeItem:
        return HotSearchRealTimeItem(
            task_id=self.task_id,
            mid=item.pop("mid", ""),
            note=item.pop("note", ""),
            rank=item.pop("rank", 0),
            category=item.pop("category", ""),
            label_name=item.pop("label_name", ""),
            hot_num=item.pop("num", 0),
            onboard_time=item.pop("onboard_time", datetime.now().timestamp()),
            payload=item,
        )


class RankEntertainmentSpider(scrapy.Spider):
    """
    文娱榜
    """

    name = "RankEntertainment"
    custom_settings = {
        "ITEM_PIPELINES": {"sina.pipelines.EntertainmentPipeline2Postgres": 300},
        "SELENIUM_DRIVER_EXECUTABLE_PATH": driver_executable_path,
        "SELENIUM_DRIVER_ARGUMENTS": ["--headless"],
        "DOWNLOADER_MIDDLEWARES": {
            "sina.middlewares.SeleniumMiddleware": 800,
        },
        "ROBOTSTXT_OBEY": False,
    }

    allowed_domains: List[str] = ["weibo.com"]
    logger = logging.getLogger(name=__name__)
    task_id = 0

    def start_requests(self):
        req_url: str = "https://weibo.com/ajax/statuses/entertainment"

        if not DBRequestTask.table_exists():
            DBRequestTask.create_table()

        self.task_id: int = DBRequestTask.insert(
            name=_TaskType.rank_entertainment.value,
            status=False,
            crawl_url=req_url,
            crawl_time=datetime.now(),
        ).execute()

        yield SeleniumRequest(
            url=req_url,
            callback=self.parse,
            wait_time=3,
            wait_until=EC.url_matches(req_url)
            and EC.presence_of_element_located((By.TAG_NAME, "pre")),
        )

    def parse(self, response: Response):
        data_json: str = response.xpath("//pre/text()").extract_first().strip()
        data: dict = json.loads(data_json).get("data", dict())
        for item in data.get("band_list", list()):
            yield self._parse_item(item=item)

    def closed(self, reason):
        DBRequestTask.update(
            status=True,
            reason=str(reason),
        ).where(DBRequestTask.id == self.task_id).execute()
        return

    def _parse_item(self, item: dict) -> EntertainmentItem:
        return EntertainmentItem(
            task_id=self.task_id,
            word=item.pop("word", ""),
            hot_rank_position=item.pop("hot_rank_position", 0),
            category=item.pop("category", ""),
            hot_num=item.pop("num", 0),
            onboard_time=item.pop("onboard_time", datetime.now().timestamp()),
            payload=item,
        )


class RankNewsSpider(scrapy.Spider):
    """
    要闻榜
    """

    name = "RankNews"
    custom_settings = {
        "ITEM_PIPELINES": {"sina.pipelines.NewsPipeline2Postgres": 300},
        "SELENIUM_DRIVER_EXECUTABLE_PATH": driver_executable_path,
        "SELENIUM_DRIVER_ARGUMENTS": ["--headless"],
        "DOWNLOADER_MIDDLEWARES": {
            "sina.middlewares.SeleniumMiddleware": 800,
        },
        "ROBOTSTXT_OBEY": False,
    }

    allowed_domains: List[str] = ["weibo.com"]
    logger = logging.getLogger(name=__name__)
    task_id = 0

    def start_requests(self):
        req_url: str = "https://weibo.com/ajax/statuses/news"

        if not DBRequestTask.table_exists():
            DBRequestTask.create_table()

        self.task_id: int = DBRequestTask.insert(
            name=_TaskType.rank_news.value,
            status=False,
            crawl_url=req_url,
            crawl_time=datetime.now(),
        ).execute()

        yield SeleniumRequest(
            url=req_url,
            callback=self.parse,
            wait_time=3,
            wait_until=EC.url_matches(req_url)
            and EC.presence_of_element_located((By.TAG_NAME, "pre")),
        )

    def parse(self, response: Response):
        data_json: str = response.xpath("//pre/text()").extract_first().strip()
        data: dict = json.loads(data_json).get("data", dict())
        for item in data.get("band_list", list()):
            yield self._parse_item(item=item)

    def closed(self, reason):
        DBRequestTask.update(
            status=True,
            reason=str(reason),
        ).where(DBRequestTask.id == self.task_id).execute()
        return

    def _parse_item(self, item: dict) -> NewsItem:
        return NewsItem(
            task_id=self.task_id,
            topic=item.pop("topic", ""),
            rank=item.pop("rank", 0),
            read=item.pop("read", 0),
            category=item.pop("category", ""),
            summary=item.pop("summary", ""),
            claim=item.pop("claim", ""),
            payload=item,
        )
