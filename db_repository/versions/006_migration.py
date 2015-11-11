from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
aggregate = Table('aggregate', pre_meta,
    Column('type', VARCHAR(length=50)),
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('month', VARCHAR(length=50)),
    Column('average_buy', NUMERIC(precision=2)),
    Column('average_sell', NUMERIC(precision=2)),
    Column('day_number', INTEGER),
    Column('month_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['aggregate'].columns['month_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['aggregate'].columns['month_id'].create()
