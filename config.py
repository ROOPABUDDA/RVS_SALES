
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/postgres'

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'postgres',
    'host': 'localhost',
    'port': '5432',
}
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

"""

MYSQL_DATABASE_USER = 'roopa'
MYSQL_DATABASE_PASSWORD = 'password'
MYSQL_DATABASE_DB = 'dbtest2'
MYSQL_DATABASE_HOST = 'localhost'

"""