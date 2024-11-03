"""腾讯股票"""

from typing import Dict, List, Optional, Set
import scrapy
from ..items import StockBoardItem


class StockBoardSpider(scrapy.Spider):
    name = "stock_board"
    allowed_domains = ["proxy.finance.qq.com"]
    _board_code_set: Set[str] = {
        "aStock",  # 沪深京
        "cyb",  # 创业板
        "ksh",  # 科创板
    }
    _board_code: str = _board_code_set.pop()  # 当前板块
    _page_size: int = 200  # 每页数据量，最大200
    _page_number: int = 0  # 页码
    _url_template: str = (
        "https://proxy.finance.qq.com/cgi/cgi-bin/rank/hs/getBoardRankList?board_code={board_code}&sort_type=price&direct=down&offset={offset}&count={count}"
    )

    def start_requests(self):
        first_url = self._url_template.format(
            board_code=self._board_code,
            offset=self._page_number * self._page_size,
            count=self._page_size,
        )
        yield scrapy.Request(url=first_url, callback=self.parse)

    def parse(self, response):
        try:
            data: Dict = response.json()
        except Exception as e:
            self.logger.error(f"response.json error: {e}")
            return
        else:
            item_list: List[dict] = data.get("data", dict()).get("rank_list", [])
            for item in item_list:
                yield StockBoardItem(
                    code=item.pop("code", ""),
                    name=item.pop("name", ""),
                    zxj=item.pop("zxj", ""),
                    zdf=item.pop("zdf", ""),
                    zd=item.pop("zd", ""),
                    hsl=item.pop("hsl", ""),
                    lb=item.pop("lb", ""),
                    zf=item.pop("zf", ""),
                    volume=item.pop("volume", ""),
                    turnover=item.pop("turnover", ""),
                    pe_ttm=item.pop("pe_ttm", ""),
                    pn=item.pop("pn", ""),
                    zsz=item.pop("zsz", ""),
                    ltsz=item.pop("ltsz", ""),
                    state=item.pop("state", ""),
                    speed=item.pop("speed", ""),
                    zdf_y=item.pop("zdf_y", ""),
                    zdf_d5=item.pop("zdf_d5", ""),
                    zdf_d10=item.pop("zdf_d10", ""),
                    zdf_d20=item.pop("zdf_d20", ""),
                    zdf_d60=item.pop("zdf_d60", ""),
                    zdf_w52=item.pop("zdf_w52", ""),
                    zljlr=item.pop("zljlr", ""),
                    zllr=item.pop("zllr", ""),
                    zllc=item.pop("zllc", ""),
                    zllr_d5=item.pop("zllr_d5", ""),
                    zllc_d5=item.pop("zllc_d5", ""),
                    stock_type=item.pop("stock_type", ""),
                    payload=item,
                    crawl_url=response.url,
                )

        next_url: Optional[str] = self._get_next_url(len(item_list))
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)

    def _get_next_url(self, item_length: int) -> Optional[str]:
        """get next url"""
        if item_length < self._page_size:
            try:
                self._board_code = self._board_code_set.pop()
                self._page_number = 0
                return self._url_template.format(
                    board_code=self._board_code,
                    offset=self._page_number * self._page_size,
                    count=self._page_size,
                )
            except KeyError:
                return None
        else:
            self._page_number += 1
            return self._url_template.format(
                board_code=self._board_code,
                offset=self._page_number * self._page_size,
                count=self._page_size,
            )
