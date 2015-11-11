from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
aggregate = Table('aggregate', post_meta,
    Column('type', String(length=50)),
    Column('id', Integer, primary_key=True, nullable=False),
    Column('month', String(length=50)),
    Column('month_number', Integer),
    Column('average_buy', Numeric(precision=2)),
    Column('average_sell', Numeric(precision=2)),
    Column('month_id', Integer),
    Column('day_number', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['aggregate'].columns['month_number'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['aggregate'].columns['month_number'].drop()
