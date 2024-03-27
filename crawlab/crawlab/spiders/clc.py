import scrapy
from typing import List, Set
from scrapy.http import Response
import logging

from ..items import ClcItem


class ClcSpider(scrapy.Spider):
    name = "clc"
    custom_settings = {
        "ITEM_PIPELINES": {"crawlab.pipelines.ClcPipeline2Postgres": 300},
        "DOWNLOADER_MIDDLEWARES": {},
    }

    allowed_domains: List[str] = ["www.clcindex.com"]
    start_urls: Set[str] = set()
    finished_urls: Set[str] = set()
    counter: int = 1  # 计数器
    logger = logging.getLogger(name=__name__)
    url_meta_map: dict[str, dict[str, any]] = dict()

    def start_requests(self):
        first_url: str = "https://www.clcindex.com"
        yield scrapy.Request(url=first_url, callback=self.parse)

    def parse(self, response: Response):
        self.logger.info(msg="开始解析: %s" % response.url)
        meta_parent_no_key: str = "parent_no"
        div_list: List[any] = response.xpath('//*[@id="catTable"]/tbody/tr')
        for div in div_list:
            order: str = str(div.xpath("./td[1]/text()").extract_first()).strip(
                " \t\n\r"
            )
            if not order.isdigit():
                # 序号非数字时，不要此数据
                continue
            no: str = str(div.xpath("./td[2]/text()").extract_first()).strip()
            title: str = str(div.xpath("./td[3]/a/text()").extract_first()).strip()
            sub_url: str = str(div.xpath("./td[3]/a/@href").extract_first()).strip()
            if sub_url.startswith("/category"):
                new_url: str = response.urljoin(url=sub_url)
                if new_url not in self.finished_urls:
                    self._add_next_url(new_url, **{meta_parent_no_key: no})
            item = ClcItem(
                order=order,
                no=no,
                title=title,
                parent_no=response.meta.get(meta_parent_no_key),
                crawl_url=response.url,
            )
            yield item

        self._add_finished_url(response.url)
        next_url: str | None = self._get_next_url()
        if next_url:
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                meta=self.url_meta_map.get(next_url),
            )

    def closed(self, reason):
        print("爬虫结束,共爬取%d条连接,原因是:" % self.counter, reason)

    def _get_next_url(self) -> str | None:
        """get and delete next url"""
        if len(self.start_urls) > 0:
            return self.start_urls.pop()
        else:
            return None

    def _add_next_url(self, url: str, **meta) -> None:
        if url not in self.finished_urls:
            self.start_urls.add(url)
            self.url_meta_map[url] = dict()
            for meta_key, meta_value in meta.items():
                self.url_meta_map[url].update({meta_key: meta_value})
        return

    def _add_finished_url(self, url: str) -> None:
        self.finished_urls.add(url)
        return None

    def _counter_url(self) -> int:
        self.counter += 1
        return self.counter
