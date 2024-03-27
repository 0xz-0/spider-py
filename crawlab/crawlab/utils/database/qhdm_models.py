from . import conn
from peewee import BigAutoField, CharField, DateTimeField, IntegerField, FixedCharField
from datetime import datetime


class QhdmItems(conn.PGBaseModel):
    id = BigAutoField(primary_key=True)
    code = FixedCharField(unique=True, max_length=12)
    name = CharField()
    level = IntegerField()
    classification_code = FixedCharField(null=True, max_length=3)
    parent_code = CharField(null=True)
    crawl_url = CharField()
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = "qhdm_items"
