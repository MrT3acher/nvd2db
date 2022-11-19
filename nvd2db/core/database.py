from peewee import *


from nvd2db.core.config import DB_PATH


db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


def init():
    from nvd2db.core.models import CVE
    
    models = [CVE]
    with db:
        db.create_tables(models)