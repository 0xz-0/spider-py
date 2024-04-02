from peewee import Model, BigAutoField, DateTimeField  # pip install peewee
from playhouse.pool import PooledPostgresqlExtDatabase
from datetime import datetime

from ...settings import POSTGRES_CONFIG


class _PGBaseModel(Model):
    """
    Base model for PostgreSQL database
    With Common Fields
    """

    id = BigAutoField(
        null=False,
        primary_key=True,
        column_name="id",
        verbose_name="自增ID",
        help_text="主键自增序列",
    )

    create_time = DateTimeField(
        null=False,
        default=datetime.now,
        verbose_name="创建时间",
    )
    update_time = DateTimeField(
        null=True,
        verbose_name="最近更新时间",
    )

    class Meta:
        # PooledPostgresqlExtDatabase replace PostgresqlDatabase
        database = PooledPostgresqlExtDatabase(
            **POSTGRES_CONFIG,
            autocommit=True,
            autoconnect=True,
            max_connections=8,
            stale_timeout=300,
        )
        schema = "sina"  # 如果不存在此schema会报错并退出
