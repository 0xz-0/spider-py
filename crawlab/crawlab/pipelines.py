# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
import os
from scrapy.exporters import CsvItemExporter

from . import items
from .utils.database import (
    DBClcItems,
    DBQhdmItems,
    DBLunarCalendar,
    DBLunarCalendarDescription,
)


class CrawlabPipeline:
    def process_item(self, item, spider):
        return item


class ClcPipeline2Postgres:
    """CLC 数据入PG库"""

    def open_spider(self, spider):
        if not DBClcItems.table_exists():
            DBClcItems.create_table()

    def close_spider(self, spider):
        pass

    def process_item(self, item: items.ClcItem, spider):
        self._write_row(item)
        return item

    def _write_row(self, item: items.ClcItem):
        _: int = (
            DBClcItems.insert(
                order=item.get("order", ""),
                no=item.get("no", ""),
                title=item.get("title", ""),
                parent_no=item.get("parent_no"),
                crawl_url=item.get("crawl_url", ""),
                crawl_time=item.get("crawl_time", default=datetime.now()),
            )
            .on_conflict(
                conflict_target=[DBClcItems.no],
                preserve=[
                    DBClcItems.order,
                    DBClcItems.title,
                    DBClcItems.parent_no,
                    DBClcItems.crawl_url,
                ],
                update={DBClcItems.update_time: datetime.now()},
            )
            .execute()
        )
        return item


class QhdmPipeline2Postgres:
    """QHDM 数据入PG库"""

    def open_spider(self, spider):
        if not DBQhdmItems.table_exists():
            DBQhdmItems.create_table()

    def close_spider(self, spider):
        pass

    def process_item(self, item: items.QhdmItem, spider):
        self._write_row(item)
        return item

    def _write_row(self, item: items.QhdmItem):
        _: int = (
            DBQhdmItems.insert(
                code=item.get("code", ""),
                name=item.get("name", ""),
                level=item.get("level", 0),
                classification_code=item.get("classification_code"),
                parent_code=item.get("parent_code"),
                crawl_url=item.get("crawl_url", ""),
                crawl_time=item.get("crawl_time", default=datetime.now()),
            )
            .on_conflict(
                conflict_target=[DBQhdmItems.code],
                preserve=[
                    DBQhdmItems.name,
                    DBQhdmItems.level,
                    DBQhdmItems.classification_code,
                    DBQhdmItems.parent_code,
                    DBQhdmItems.crawl_url,
                ],
                update={DBQhdmItems.update_time: datetime.now()},
            )
            .execute()
        )
        return item


class IntelCpuRankPipeline2Csv:
    """英特尔处理器性能排行 数据入CSV"""

    def open_spider(self, spider):
        now: str = datetime.now().strftime("%Y%m%d%H%M%S")
        directory = "./data"
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.file = open(
            file=f"{directory}/英特尔处理器性能排名_{now}.csv",
            mode="wb",
        )
        self.exporter = CsvItemExporter(
            self.file,
            include_headers_line=True,
            encoding="utf-8",
            fields_to_export=[  # 指定导出的字段，目前全部导出，此处主要是保证顺序
                "rank",
                "processor",
                "points",
                "cores",
                "hertz",
                "tdp",
                "release_date",
                "crawl_url",
                "crawl_time",
            ],
        )
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item: items.IntelCpuRankItem, spider):
        self.exporter.export_item(item)
        return item


class LunarCalendarPipeline2Postgres:
    """日历 数据入PG库"""

    def open_spider(self, spider):
        if not DBLunarCalendar.table_exists():
            DBLunarCalendar.create_table()

        if not DBLunarCalendarDescription.table_exists():
            DBLunarCalendarDescription.create_table()

    def close_spider(self, spider):
        pass

    def process_item(
        self,
        item: items.LunarCalendarDailyItem | items.LunarCalendarDescriptionItem,
        spider,
    ):
        match item:
            case items.LunarCalendarDailyItem():
                self._write_daily_row(item)
            case items.LunarCalendarDescriptionItem():
                self._write_desc_row(item)
            case _:
                pass
        return item

    def _write_daily_row(self, item: items.LunarCalendarDailyItem):
        _: int = (
            DBLunarCalendar.insert(
                date=item.get("date", ""),
                year=item.get("year", 0),
                month=item.get("month", 0),
                day=item.get("day", 0),
                week=item.get("week", ""),
                lunar_date=item.get("lunar_date", ""),
                lunar_year=item.get("lunar_year", 0),
                lunar_month=item.get("lunar_month", 0),
                lunar_day=item.get("lunar_day", 0),
                festivals=item.get("festivals", default="[]"),
                suits=item.get("suits", default="[]"),
                avoids=item.get("avoids", default="[]"),
                lunar_zodiac=item.get("lunar_zodiac", ""),
                pengzu_baiji=item.get("pengzu_baiji", ""),
                year_five_elements=item.get("year_five_elements", ""),
                month_five_elements=item.get("month_five_elements", ""),
                day_five_elements=item.get("day_five_elements", ""),
                julian_day=item.get("julian_day", 0.0),
                clash=item.get("clash", ""),
                six_days=item.get("six_days", ""),
                lunar_constellation=item.get("lunar_constellation", ""),
                fetal_god=item.get("fetal_god", ""),
                season=item.get("season", ""),
                lunar_mansion=item.get("lunar_mansion", ""),
                solar_terms=item.get("solar_terms", ""),
                islamic_calendar=item.get("islamic_calendar", ""),
                sha=item.get("sha", ""),
                twelve_gods=item.get("twelve_gods", ""),
                payload=item.get("payload", "{}"),
                crawl_url=item.get("crawl_url", ""),
                crawl_time=item.get("crawl_time", default=datetime.now()),
            )
            .on_conflict_ignore()
            .execute()
        )

    def _write_desc_row(self, item: items.LunarCalendarDescriptionItem):
        _: int = (
            DBLunarCalendarDescription.insert(
                type=item.get("type", ""),
                name=item.get("name", ""),
                title=item.get("title", ""),
                crawl_url=item.get("crawl_url", ""),
                crawl_time=item.get("crawl_time", default=datetime.now()),
            )
            .on_conflict_ignore()
            .execute()
        )
        return item


class LunarCalendarDescriptionPipeline2Postgres:
    """日历描述 数据入PG库"""

    def open_spider(self, spider):
        if not DBLunarCalendarDescription.table_exists():
            DBLunarCalendarDescription.create_table()

    def close_spider(self, spider):
        pass

    def process_item(self, item: items.LunarCalendarDescriptionItem, spider):
        DBLunarCalendarDescription.update(
            {
                DBLunarCalendarDescription.description: item.get("description", ""),
                DBLunarCalendarDescription.update_time: datetime.now(),
            }
        ).where(DBLunarCalendarDescription.id == item["item_id"]).execute()
        return item
