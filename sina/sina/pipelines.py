# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from datetime import datetime

from . import items
from .utils.database import (
    DBRankHotSearchRealTimeItems,
    DBRankHotSearchHotGovItems,
    DBRankEntertainmentItems,
    DBRankNewsItems,
)


class SinaPipeline:
    def process_item(self, item, spider):
        return item


class HotSearchPipeline2Postgres:
    def open_spider(self, spider):
        if not DBRankHotSearchRealTimeItems.table_exists():
            DBRankHotSearchRealTimeItems.create_table()

        if not DBRankHotSearchHotGovItems.table_exists():
            DBRankHotSearchHotGovItems.create_table()

    def close_spider(self, spider):
        pass

    def process_item(
        self, item: items.HotSearchRealTimeItem | items.HotSearchHotGovItem, spider
    ):
        if isinstance(item, items.HotSearchRealTimeItem):
            self._write_real_time_row(item)
        elif isinstance(item, items.HotSearchHotGovItem):
            self._write_hot_gov_row(item)
        return item

    def _write_real_time_row(self, item: items.HotSearchRealTimeItem):
        _: int = DBRankHotSearchRealTimeItems.insert(
            task_id=item.get("task_id", 0),
            mid=item.get("mid", ""),
            note=item.get("note", ""),
            rank=item.get("rank", 0),
            category=item.get("category", ""),
            label_name=item.get("label_name", ""),
            hot_num=item.get("hot_num", ""),
            onboard_time=item.get("onboard_time", datetime.now().timestamp()),
            payload=item.get("payload", "{}"),
        ).execute()
        return item

    def _write_hot_gov_row(self, item: items.HotSearchHotGovItem):
        _: int = DBRankHotSearchHotGovItems.insert(
            task_id=item.get("task_id", 0),
            mid=item.get("mid", ""),
            note=item.get("note", ""),
            stime=item.get("stime", datetime.now().timestamp()),
            payload=item.get("payload", "{}"),
        ).execute()
        return item


class EntertainmentPipeline2Postgres:
    def open_spider(self, spider):
        if not DBRankEntertainmentItems.table_exists():
            DBRankEntertainmentItems.create_table()

    def close_spider(self, spider):
        pass

    def process_item(self, item: items.EntertainmentItem, spider):
        self._write_row(item)
        return item

    def _write_row(self, item: items.EntertainmentItem):
        _: int = DBRankEntertainmentItems.insert(
            task_id=item.get("task_id", 0),
            word=item.get("word", ""),
            hot_rank_position=item.get("hot_rank_position", 0),
            category=item.get("category", ""),
            hot_num=item.get("hot_num", ""),
            onboard_time=item.get("onboard_time", datetime.now().timestamp()),
            payload=item.get("payload", "{}"),
        ).execute()
        return item


class NewsPipeline2Postgres:
    def open_spider(self, spider):
        if not DBRankNewsItems.table_exists():
            DBRankNewsItems.create_table()

    def close_spider(self, spider):
        pass

    def process_item(self, item: items.NewsItem, spider):
        self._write_row(item)
        return item

    def _write_row(self, item: items.NewsItem):
        _: int = DBRankNewsItems.insert(
            task_id=item.get("task_id", 0),
            topic=item.get("topic", ""),
            rank=item.get("rank", 0),
            read=item.get("read", 0),
            category=item.get("category", ""),
            summary=item.get("summary", ""),
            claim=item.get("claim", default=""),
            payload=item.get("payload", "{}"),
        ).execute()
        return item
