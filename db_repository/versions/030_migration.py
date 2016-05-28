from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
aggregate = Table('aggregate', pre_meta,
    Column('type', VARCHAR(length=50)),
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('year', INTEGER),
    Column('month', VARCHAR(length=50)),
    Column('month_number', INTEGER),
    Column('average_buy', NUMERIC(precision=2)),
    Column('average_sell', NUMERIC(precision=2)),
    Column('month_id', INTEGER),
    Column('stats_id', INTEGER),
    Column('day_number', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['aggregate'].columns['stats_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['aggregate'].columns['stats_id'].create()
