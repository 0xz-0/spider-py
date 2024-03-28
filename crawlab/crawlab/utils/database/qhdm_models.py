from peewee import CharField, IntegerField, FixedCharField

from . import conn


class QhdmItems(conn._PGBaseModel):
    code = FixedCharField(unique=True, max_length=12)
    name = CharField()
    level = IntegerField()
    classification_code = FixedCharField(null=True, max_length=3)
    parent_code = CharField(null=True)

    class Meta:
        table_name = "qhdm_items"
