from peewee import CharField, IntegerField, BooleanField, TextField, DateField
from playhouse.postgres_ext import BinaryJSONField

from . import conn


class BaiduHistoryToday(conn._PGBaseModel):
    date = CharField(help_text="日期，格式为MM-DD")
    year = IntegerField(help_text="年")
    title = TextField(help_text="标题")
    desc = TextField(help_text="描述")
    festival = CharField(help_text="节日")
    link = TextField(help_text="链接")
    type = CharField(help_text="类型")
    cover = BooleanField(help_text="封面")
    recommend = BooleanField(help_text="推荐")
    payload = BinaryJSONField(help_text="剩余数据")

    class Meta:
        table_name = "baidu_history_today"
