from peewee import Model
from peewee import SqliteDatabase

db = SqliteDatabase('events.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

    def json(self):
        r = {}
        for k in self._data.keys():
          try:
             r[k] = str(getattr(self, k))
          except:
             r[k] = json.dumps(getattr(self, k))
        return json.dumps(r)

from . import models

def init():
    models.create_tables(db)