import re
import scrapy
from typing import List, Set
from scrapy.http import Response
import logging

from ..items import IntelCpuRankItem


class IntelCpuRankSpider(scrapy.Spider):
    name = "intel_cpu_rank"
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "ITEM_PIPELINES": {"crawlab.pipelines.IntelCpuRankPipeline2Csv": 300},
        "DOWNLOADER_MIDDLEWARES": {},
    }
    allowed_domains = ["cpu-compare.com"]
    url = "https://cpu-compare.com/zh-CN/benchmark/intel?page={page}"
    logger = logging.getLogger(name=__name__)
    current_page: int = 1

    def _get_url(self, page: int) -> str:
        return self.url.format(page=page)

    def start_requests(self):
        yield scrapy.Request(url=self._get_url(page=1), callback=self.parse)

    def parse(self, response: Response):
        next_url: None | str = None
        self.logger.info(msg="开始解析: %s" % response.url)
        div_list: List[any] = response.xpath('//div[@class="rating-table-body"]/div')
        for div in div_list:
            try:
                rank: int = int(
                    div.xpath('./div[@class="rating-table-number"]/text()')
                    .getall()[-1]
                    .strip()
                )
            except ValueError:
                continue
            item: IntelCpuRankItem = IntelCpuRankItem(
                rank=rank,
                processor="",
                points=-1,
                cores="",
                hertz="",
                tdp="",
                release_date="",
                crawl_url=response.url,
            )
            item_names: List[str] = [
                "processor",
                "points",
                "cores",
                "hertz",
                "tdp",
                "release_date",
            ]
            content_div: List[scrapy.Selector] = div.xpath(
                './div[@class="rating-table-content"]/div'
            )
            for i, c_div in enumerate(content_div):
                match i:
                    case 0 | 5:
                        item[item_names[i]] = str(
                            c_div.xpath(".//span/text()").extract_first().strip()
                        )
                    case 1:
                        try:
                            item[item_names[i]] = int(
                                c_div.xpath(f"./text()").extract()[-1].strip()
                            )
                        except ValueError:
                            continue
                    case 2 | 3 | 4:
                        item[item_names[i]] = str(
                            c_div.xpath("./text()").extract()[-1].strip()
                        )
                    case _:
                        pass
            yield item

        try:
            current_page: int = int(
                response.xpath('//li[@class="active"]/a/text()').extract_first().strip()
            )
        except ValueError:
            current_page = -1
        next_url: str | None = self._get_next_url(current_page)
        if next_url:
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
            )

    def _get_next_url(self, current_page: int) -> str | None:
        """get and delete next url"""
        if current_page == self.current_page:
            self.current_page += 1
            return self._get_url(page=self.current_page)

    def closed(self, reason):
        print("爬虫结束,共爬取%d页,原因是:" % self.current_page, reason)
