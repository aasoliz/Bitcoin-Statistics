from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
predictions = Table('predictions', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('right', BOOLEAN),
    Column('prediction', VARCHAR(length=50)),
    Column('prediction_type', VARCHAR(length=5)),
)

predictions = Table('predictions', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('right', Boolean, default=ColumnDefault(False)),
    Column('buy_prediction', Boolean, default=ColumnDefault(False)),
    Column('sell_prediction', Boolean, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['predictions'].columns['prediction'].drop()
    pre_meta.tables['predictions'].columns['prediction_type'].drop()
    post_meta.tables['predictions'].columns['buy_prediction'].create()
    post_meta.tables['predictions'].columns['sell_prediction'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['predictions'].columns['prediction'].create()
    pre_meta.tables['predictions'].columns['prediction_type'].create()
    post_meta.tables['predictions'].columns['buy_prediction'].drop()
    post_meta.tables['predictions'].columns['sell_prediction'].drop()
