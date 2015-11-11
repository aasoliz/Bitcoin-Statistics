import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

bitcoin_key = 'HXieJjOkGemshiw8hzl3Iq0Cgd8Ip1gT7JYjsn5myB8JJQ6rBl'
