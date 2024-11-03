from peewee import Model, CharField, TextField, SqliteDatabase
from playhouse.postgres_ext import ArrayField, BinaryJSONField
from . import conn


class StockBoard(conn._PGBaseModel):
    """
    股票面板数据
    """

    code = CharField()
    name = CharField()
    zxj = CharField()
    zdf = CharField()
    zd = CharField()
    hsl = CharField()
    lb = CharField()
    zf = CharField()
    volume = CharField()
    turnover = CharField()
    pe_ttm = CharField()
    pn = CharField()
    zsz = CharField()
    ltsz = CharField()
    state = CharField()
    speed = CharField()
    zdf_y = CharField()
    zdf_d5 = CharField()
    zdf_d10 = CharField()
    zdf_d20 = CharField()
    zdf_d60 = CharField()
    zdf_w52 = CharField()
    zljlr = CharField()
    zllr = CharField()
    zllc = CharField()
    zllr_d5 = CharField()
    zllc_d5 = CharField()
    stock_type = CharField()

    payload = BinaryJSONField()

    class Meta:
        table_name = "stock_board"
