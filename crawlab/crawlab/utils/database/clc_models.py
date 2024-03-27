from . import conn
from peewee import BigAutoField, CharField, DateTimeField
from datetime import datetime


class ClcItems(conn.PGBaseModel):
    id = BigAutoField(primary_key=True)
    order = CharField()
    no = CharField(unique=True)
    title = CharField()
    crawl_url = CharField()
    parent_no = CharField(null=True)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = "clc_items"
