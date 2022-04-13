import sqlalchemy as sa

mod2_engine = sa.create_engine("postgresql://admin:admin@127.0.0.1:5432/module2")
db = mod2_engine.connect()
