# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime

from . import items
from .utils.database import DBClcItems


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
