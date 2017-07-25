from peewee import CharField, IntegerField, DateField

from .. import BaseModel

class Summary(BaseModel):
    jid = CharField(index=True)
    status = CharField()
    day = DateField()
    total = IntegerField()