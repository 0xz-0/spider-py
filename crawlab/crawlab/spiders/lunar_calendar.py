from copy import deepcopy
from datetime import datetime
from enum import Enum
import re
import scrapy
from typing import Dict, List, Set, Union
from scrapy.http import Response
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from ..items import LunarCalendarDailyItem, LunarCalendarDescriptionItem
from ..utils.database import DBLunarCalendarDescription


class LunarCalendarDescriptionTypeEnum(Enum):
    yi_ji: str = "宜忌"
    festival: str = "节日"
    other: str = "其他"


class LunarCalendarSpider(scrapy.Spider):
    name = "lunar_calendar"
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "ITEM_PIPELINES": {"crawlab.pipelines.LunarCalendarPipeline2Postgres": 300},
        "DOWNLOADER_MIDDLEWARES": {},
    }
    allowed_domains: List[str] = ["wannianrili.bmcx.com"]
    url: str = "https://wannianrili.bmcx.com/ajax/?q={year}-{month}"
    logger = logging.getLogger(name=__name__)

    def _get_url(self, year: int, month: int) -> str:
        # month: 1-12(可不用填充)
        return self.url.format(year=year, month=month)

    def start_requests(self):
        year = int(getattr(self, "year", 2024))
        month = int(getattr(self, "month", 10))
        yield scrapy.Request(
            url=self._get_url(year=year, month=month),
            callback=self.parse,
            meta=dict(year=year, month=month),
        )

    def parse(self, response: Response):
        self.logger.info(msg="开始解析: %s" % response.url)
        soup = BeautifulSoup(response.text, "html.parser")
        date_dict = dict()
        festival_set: set = set()
        yi_ji_set: set = set()
        for div in soup.find_all("div", class_="wnrl_k_you", recursive=True):
            date, data = self._parse_base_info(div)
            festivals: List = self._parse_festivals(div)
            data["festivals"] = list()
            for festival in festivals:
                festival_name = festival.get("text")
                if festival_name:
                    data["festivals"].append(festival["text"])
                else:
                    continue
                if festival_name not in festival_set:
                    festival_set.add(festival_name)
                    yield LunarCalendarDescriptionItem(
                        type=LunarCalendarDescriptionTypeEnum.festival.value,
                        name=festival_name,
                        crawl_url=urljoin(self.url, festival.get("href", "")),
                    )
            yis: List = self._parse_yi(div)
            data["suits"] = list()
            for yi in yis:
                yi_name = yi.get("text")
                if yi_name:
                    data["suits"].append(yi_name)
                else:
                    continue
                if yi_name not in yi_ji_set:
                    yi_ji_set.add(yi_name)
                    yield LunarCalendarDescriptionItem(
                        type=LunarCalendarDescriptionTypeEnum.yi_ji.value,
                        name=yi_name,
                        title=yi.get("title", ""),
                        crawl_url=urljoin(self.url, yi.get("href", "")),
                    )
            jis: List = self._parse_ji(div)
            data["avoids"] = list()
            for ji in jis:
                ji_name = ji.get("text")
                if ji_name:
                    data["avoids"].append(ji_name)
                else:
                    continue
                if ji_name not in yi_ji_set:
                    yi_ji_set.add(ji_name)
                    yield LunarCalendarDescriptionItem(
                        type=LunarCalendarDescriptionTypeEnum.yi_ji.value,
                        name=ji_name,
                        title=ji.get("title", ""),
                        crawl_url=urljoin(self.url, ji.get("href", "")),
                    )

            date_dict[date] = deepcopy(data)

        for div in soup.find_all("div", class_="wnrl_k_xia_id", recursive=False):
            header: str = div.find(
                "div", class_="wnrl_k_xia_top", recursive=False
            ).span.text.strip()
            date: str = datetime.strptime(
                re.search(r"\d{4}月\d{2}月\d{2}日", header).group(), "%Y月%m月%d日"
            ).strftime("%Y-%m-%d")
            ext: Dict = self._parse_detail_info(div)
            yield LunarCalendarDailyItem(
                date=date,
                year=date_dict.get(date, dict()).get("year", response.meta["year"]),
                month=date_dict.get(date, dict()).get("month", response.meta["month"]),
                day=date_dict.get(date, dict()).get("day", 0),
                week=date_dict.get(date, dict()).get("week", ""),
                lunar_date=date_dict.get(date, dict()).get("lunar_date", ""),
                lunar_year=date_dict.get(date, dict()).get("lunar_year", ""),
                lunar_month=date_dict.get(date, dict()).get("lunar_month", ""),
                lunar_day=date_dict.get(date, dict()).get("lunar_day", ""),
                festivals=date_dict.get(date, dict()).get("festivals", []),
                suits=date_dict.get(date, dict()).get("suits", []),
                avoids=date_dict.get(date, dict()).get("avoids", []),
                lunar_zodiac=ext.pop("生肖", ""),
                pengzu_baiji=ext.pop("彭祖百忌", ""),
                year_five_elements=ext.pop("年五行", ""),
                month_five_elements=ext.pop("月五行", ""),
                day_five_elements=ext.pop("日五行", ""),
                julian_day=ext.pop("儒略日", 0.0),
                clash=ext.pop("冲", ""),
                six_days=ext.pop("六曜", ""),
                lunar_constellation=ext.pop("星座", ""),
                fetal_god=ext.pop("胎神占方", ""),
                season=ext.pop("季节", ""),
                lunar_mansion=ext.pop("星宿", ""),
                solar_terms=ext.pop("节气", ""),
                islamic_calendar=ext.pop("伊斯兰历", ""),
                sha=ext.pop("煞", ""),
                twelve_gods=ext.pop("十二神", ""),
                payload=ext,
                crawl_url=response.url,
            )

        return

    def _parse_base_info(self, div: BeautifulSoup) -> Union[str, Dict[str, str]]:
        # eg: 2024年 10月 (大) 星期二
        title: str = div.find("div", class_="wnrl_k_you_id_biaoti").text.strip()
        # eg: 01
        day: str = div.find(name="div", class_="wnrl_k_you_id_wnrl_riqi").text.strip()
        # eg: 八月廿九
        lunar_date: str = div.find(
            "div", class_="wnrl_k_you_id_wnrl_nongli"
        ).text.strip()
        # eg: 甲辰年 【龙年】 癸酉月 戊戌日
        lunar_list: List = (
            div.find("div", class_="wnrl_k_you_id_wnrl_nongli_ganzhi")
            .text.strip()
            .split(" ")
        )

        # 解析
        year_month_day: List[str] = re.findall(r"\d+", string=title) + [day]
        return "-".join(year_month_day), dict(
            date="-".join(year_month_day),
            year=int(year_month_day[0]),
            month=int(year_month_day[1]),
            day=int(year_month_day[2]),
            week=title.split(" ")[-1].strip(),
            # week=re.findall(r"星期(.)", title)[0],
            lunar_date=lunar_date,
            lunar_year=lunar_list[0],
            # lunar_zodiac=lunar_list[1],
            lunar_month=lunar_list[2],
            lunar_day=lunar_list[3],
        )

    def _parse_festivals(self, div: BeautifulSoup) -> List[str]:
        jieri = div.find("div", class_="wnrl_k_you_id_wnrl_jieri")
        # eg:  [{'text': '国庆节', 'href': '/guoqingjie__jieri/', 'target': '_blank'}, {'text': '国际音乐日', 'href': '/yinyueri__jieri/', 'target': '_blank'}, {'text': '国际老人节', 'href': '/laorenjie__jieri/', 'target': '_blank'}]
        if jieri:
            return list(
                map(
                    lambda x: dict(text=x.text, **x.attrs),
                    jieri.find(
                        "span", class_="wnrl_k_you_id_wnrl_jieri_neirong"
                    ).find_all("a"),
                )
            )
        return []

    def __parse_yi_ji(self, div: BeautifulSoup, name: str) -> List[str]:
        yi_ji = div.find("div", class_="wnrl_k_you_id_wnrl_%s" % name)
        # eg: [{'text': '嫁娶', 'href': '//laohuangli.bmcx.com/24__yijijieshao/', 'target': '_blank', 'title': '男娶女嫁，举行结婚大典的吉日。跟另自己的伴侣一起生活。'}, {'text': '纳采', 'href': '//laohuangli.bmcx.com/1__yijijieshao/', 'target': '_blank', 'title': '男方向女方送求婚礼物。'}]
        if yi_ji:
            return list(
                map(
                    lambda x: dict(text=x.text, **x.attrs),
                    yi_ji.find(
                        "span", class_="wnrl_k_you_id_wnrl_%s_neirong" % name
                    ).find_all("a"),
                )
            )
        return []

    def _parse_yi(self, div: BeautifulSoup) -> List[str]:
        return self.__parse_yi_ji(div, "yi")

    def _parse_ji(self, div: BeautifulSoup) -> List[str]:
        return self.__parse_yi_ji(div, "ji")

    def _parse_detail_info(self, div: BeautifulSoup) -> Dict[str, str]:
        attr_list: List[BeautifulSoup] = div.find_all(
            "div", class_="wnrl_k_xia_nr_wnrl_beizhu", recursive=True
        )
        attr_dict = {}
        for attr in attr_list:
            key: str = attr.find(
                "span", class_="wnrl_k_xia_nr_wnrl_beizhu_biaoti"
            ).text.strip()
            value: str = attr.find(
                "span", class_="wnrl_k_xia_nr_wnrl_beizhu_neirong"
            ).text.strip()
            attr_dict[key] = value
        return attr_dict

    def closed(self, reason):
        print("爬虫结束,共爬取1页,原因是:", reason)


class LunarCalendarDescriptionSpider(scrapy.Spider):
    name = "lunar_calendar_description"
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "ITEM_PIPELINES": {
            "crawlab.pipelines.LunarCalendarDescriptionPipeline2Postgres": 300
        },
        "DOWNLOADER_MIDDLEWARES": {},
    }
    allowed_domains: List[str] = [
        "wannianrili.bmcx.com",
        "laohuangli.bmcx.com",
        "jieqi.bmcx.com",
    ]
    logger = logging.getLogger(name=__name__)
    counter: int = 0

    def start_requests(self):
        for record in DBLunarCalendarDescription.select(
            DBLunarCalendarDescription.crawl_url,
            DBLunarCalendarDescription.id,
            DBLunarCalendarDescription.type,
        ).where(
            DBLunarCalendarDescription.update_time == None,
            DBLunarCalendarDescription.description == None,
        ):
            yield scrapy.Request(
                url=record.crawl_url,
                callback=self.parse,
                meta=dict(id=record.id, type=record.type),
            )

    def parse(self, response: Response):
        self.logger.info(msg="开始解析: %s" % response.url)
        self.counter += 1
        soup = BeautifulSoup(response.text, "html.parser")
        if response.meta["type"] == LunarCalendarDescriptionTypeEnum.festival.value:
            yield self._parse_wannianrili(soup, response.meta["id"])
        elif response.meta["type"] == LunarCalendarDescriptionTypeEnum.yi_ji.value:
            yield self._parse_laohuangli(soup, response.meta["id"])

    def _parse_wannianrili(
        self, soup: BeautifulSoup, id: int
    ) -> LunarCalendarDescriptionItem:
        title: List[str] = soup.find_all("div", class_="jieqi_neirong_x_biaoti")
        content: List[str] = soup.find_all("div", class_="jieqi_neirong_x_beizhu")
        description: List = list()
        for idx in range(min(len(title), len(content))):
            description.append(
                {
                    "title": title[idx].text.strip(),
                    "content": list(
                        filter(lambda x: x != "", content[idx].text.strip().split("\n"))
                    ),
                }
            )
        return LunarCalendarDescriptionItem(
            item_id=id,
            type=LunarCalendarDescriptionTypeEnum.festival.value,
            description=description,
        )

    def _parse_laohuangli(
        self, soup: BeautifulSoup, id: int
    ) -> LunarCalendarDescriptionItem:
        description: List = list(
            map(
                lambda x: x.text.strip(),
                soup.find(name="div", class_="neirong").find_all("p"),
            )
        )
        return LunarCalendarDescriptionItem(
            item_id=id,
            type=LunarCalendarDescriptionTypeEnum.yi_ji.value,
            description=description,
        )

    def closed(self, reason):
        print("爬虫结束,共爬取%d页,原因是:" % self.counter, reason)
