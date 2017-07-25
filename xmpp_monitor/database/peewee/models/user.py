from peewee import CharField

from .. import BaseModel

class User(BaseModel):
    jid = CharField()
    name = CharField()
