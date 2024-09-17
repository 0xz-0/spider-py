from peewee import CharField, IntegerField, DecimalField, TextField, DateField
from playhouse.postgres_ext import ArrayField, BinaryJSONField

from . import conn


class LunarCalendarDescription(conn._PGBaseModel):
    """
    农历日历相关描述
    """

    type = CharField(help_text="类型，如宜忌、节日等")
    name = CharField(help_text="名称")
    title = CharField(help_text="标题")
    description = BinaryJSONField(help_text="描述", default=[], null=True)

    class Meta:
        table_name = "lunar_calendar_description"
        indexes = ((("type", "name"), True),)


class LunarCalendar(conn._PGBaseModel):
    """
    农历日历
    """

    date = DateField(help_text="日期")
    year = IntegerField(help_text="年")
    month = IntegerField(help_text="月")
    day = IntegerField(help_text="日")
    week = CharField(help_text="星期")
    lunar_date = CharField(help_text="农历日期")
    lunar_year = CharField(help_text="农历年")
    lunar_month = CharField(help_text="农历月")
    lunar_day = CharField(help_text="农历日")
    festivals = ArrayField(CharField, help_text="节日")
    suits = ArrayField(CharField, help_text="宜")
    avoids = ArrayField(CharField, help_text="忌")

    # 以下为附加字段
    lunar_zodiac = CharField(help_text="生肖")
    pengzu_baiji = CharField(help_text="彭祖百忌")
    year_five_elements = CharField(help_text="年五行")
    month_five_elements = CharField(help_text="月五行")
    day_five_elements = CharField(help_text="日五行")
    julian_day = DecimalField(max_digits=10, decimal_places=2, help_text="儒略日")
    clash = CharField(help_text="冲")
    six_days = CharField(help_text="六曜")
    lunar_constellation = CharField(help_text="星座")
    fetal_god = CharField(help_text="胎神占方")
    season = CharField(help_text="季节")
    lunar_mansion = CharField(help_text="星宿")
    solar_terms = CharField(help_text="节气")
    islamic_calendar = CharField(help_text="伊斯兰历")
    sha = CharField(help_text="煞")
    twelve_gods = CharField(help_text="十二神")

    payload = BinaryJSONField(help_text="剩余数据")

    class Meta:
        table_name = "lunar_calendar"
        indexes = ((("date",), True),)
