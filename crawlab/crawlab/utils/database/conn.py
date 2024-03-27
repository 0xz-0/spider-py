from peewee import Model  # pip install peewee
from playhouse.pool import PooledPostgresqlExtDatabase

from ...settings import POSTGRES_CONFIG


class PGBaseModel(Model):
    class Meta:
        # PooledPostgresqlExtDatabase replace PostgresqlDatabase
        database = PooledPostgresqlExtDatabase(
            **POSTGRES_CONFIG,
            autocommit=True,
            autoconnect=True,
            max_connections=8,
            stale_timeout=300,
        )
        schema = "crawlab"  # 不设置默认为public
