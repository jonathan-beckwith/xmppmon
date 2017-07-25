from peewee import CharField, DateTimeField

from .. import BaseModel

class Event(BaseModel):
    jid = CharField()
    status = CharField()
    timestamp = DateTimeField(index=True)