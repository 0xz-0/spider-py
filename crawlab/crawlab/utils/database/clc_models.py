from peewee import CharField

from . import conn


class ClcItems(conn._PGBaseModel):
    order = CharField()
    no = CharField(unique=True)
    title = CharField()
    parent_no = CharField(null=True)

    class Meta:
        table_name = "clc_items"
