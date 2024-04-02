from peewee import CharField, DateTimeField, BooleanField, BigIntegerField, IntegerField
from datetime import datetime
from playhouse.postgres_ext import BinaryJSONField

# import json

from . import conn


class RequestTask(conn._PGBaseModel):
    name = CharField(
        null=False,
        verbose_name="任务类型",
    )

    status = BooleanField(
        null=False,
        default=False,
        verbose_name="是否完成",
    )

    crawl_url = CharField(
        null=False,
        verbose_name="爬取链接",
        help_text="爬取的URL地址",
    )

    crawl_time = DateTimeField(
        null=False,
        default=datetime.now,
        verbose_name="开始爬取时间",
        help_text="爬取的时间",
    )

    reason = CharField(
        null=True,
        verbose_name="失败原因",
        help_text="失败的原因",
    )

    class Meta:
        table_name = "request_task"


class HotSearchHotGovItems(conn._PGBaseModel):
    task_id = BigIntegerField(null=False, help_text="关联RequestTask.ID")
    mid = CharField(null=False, help_text="微博ID")
    note = CharField()
    stime = BigIntegerField()
    payload = BinaryJSONField()

    class Meta:
        table_name = "hot_search_hot_gov"


class HotSearchRealTimeItems(conn._PGBaseModel):
    task_id = BigIntegerField(null=False, help_text="关联RequestTask.ID")
    mid = CharField(null=False, help_text="微博ID")
    note = CharField()
    rank = IntegerField()
    category = CharField()
    label_name = CharField()
    hot_num = BigIntegerField()
    onboard_time = BigIntegerField()
    payload = BinaryJSONField()

    class Meta:
        table_name = "hot_search_real_time"


class EntertainmentItems(conn._PGBaseModel):
    task_id = BigIntegerField(null=False, help_text="关联RequestTask.ID")
    word = CharField()
    hot_rank_position = IntegerField()
    category = CharField()
    hot_num = BigIntegerField()
    onboard_time = BigIntegerField()
    payload = BinaryJSONField()

    class Meta:
        table_name = "entertainment"


class RankNewsItems(conn._PGBaseModel):
    task_id = BigIntegerField(null=False, help_text="关联RequestTask.ID")
    topic = CharField()
    rank = IntegerField()
    read = BigIntegerField()
    category = CharField()
    summary = CharField()
    claim = CharField()
    payload = BinaryJSONField()

    class Meta:
        table_name = "news"
