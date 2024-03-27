from enum import Enum
import scrapy
from typing import List, Set
from scrapy.http import Response
import logging

from ..items import QhdmItem


class QhdmMetaKeyEnum(Enum):
    parent_code: int = 1
    level: int = 2


class QhdmSpider(scrapy.Spider):
    name = "qhdm"
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "ITEM_PIPELINES": {"crawlab.pipelines.QhdmPipeline2Postgres": 300},
        "DOWNLOADER_MIDDLEWARES": {},
    }
    allowed_domains: List[str] = ["www.stats.gov.cn"]
    start_urls: Set[str] = set()
    finished_urls: Set[str] = set()
    counter: int = 1  # 计数器
    logger = logging.getLogger(name=__name__)
    url_meta_map: dict[str, dict[str, any]] = dict()

    def start_requests(self):
        first_url: str = (
            "https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html"
        )
        yield scrapy.Request(url=first_url, callback=self.parse_province)

    def parse_province(self, response: Response):
        for row in response.xpath('//tr[@class="provincetr"]'):
            for province in row.xpath(".//td"):
                name: str = str(province.xpath(".//a/text()").extract_first()).strip()
                sub_url: str = str(province.xpath(".//a/@href").extract_first()).strip()
                code: str = sub_url.replace(".html", "").ljust(12, "0")
                level: int = 1
                self._add_next_url(
                    url=response.urljoin(url=sub_url),
                    **{
                        QhdmMetaKeyEnum.level.name: level,
                        QhdmMetaKeyEnum.parent_code.name: code,
                    },
                )
                item = QhdmItem(
                    code=code,
                    name=name,
                    level=level,
                    crawl_url=response.url,
                )
                yield item

        next_url: str | None = self._get_next_url()
        if next_url:
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                meta=self.url_meta_map.get(next_url),
            )

    def parse(self, response: Response):
        header_list: List[str] = response.xpath(
            '//tr[contains(@class,"head")]/td/text()'
        ).extract()
        tr_list: List[any] = response.xpath('//tr[contains(@class,"tr")]')
        level: int = response.meta.get(QhdmMetaKeyEnum.level.name, 0) + 1
        for tr in tr_list:
            item = QhdmItem(
                code="",
                name="",
                level=level,
                classification_code=None,
                parent_code=response.meta.get(QhdmMetaKeyEnum.parent_code.name),
                crawl_url=response.url,
            )
            sub_url: str = ""
            for col, td in enumerate(iterable=tr.xpath("./td")):
                if col > len(header_list):
                    break
                else:
                    a = td.xpath("./a")
                    if a:
                        href = a.xpath("./@href").extract_first()
                        text = a.xpath("./text()").extract_first()
                    else:
                        href = None
                        text = td.xpath("./text()").extract_first()
                    match header_list[col]:
                        case "统计用区划代码":
                            item["code"] = text
                            if href:
                                sub_url = href
                        case "名称":
                            item["name"] = text
                        case "城乡分类代码":
                            item["classification_code"] = text
                        case _:
                            pass

            if sub_url.endswith(".html"):
                new_url: str = response.urljoin(url=sub_url)
                if new_url not in self.finished_urls:
                    self._add_next_url(
                        new_url,
                        **{
                            QhdmMetaKeyEnum.level.name: item["level"],
                            QhdmMetaKeyEnum.parent_code.name: item["code"],
                        },
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
