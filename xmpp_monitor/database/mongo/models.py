from pymongo import MongoClient

URI = 'mongodb://localhost:27017'
DATABASE = 'xmpp_monitor'

mongo = MongoClient(URI)

db = mongo[DATABASE]

def save(collection, document):
    db[collection].insert(document)
    return document

class BaseModel:
    def __init__(self, **kwargs):
        for k,v in self.__dict__:
            print(k,v)
            self[k] = kwargs[k]

    def save(self):
        save(self.__class__.__name__.lower() + "s", self.__dict__)

    @classmethod
    def select(cls, *selection):
        collection = cls.__name__.lower() + "s"
        return [cls(**x) for x in db[collection].find()]
        pass

class Event(BaseModel):
    jid = ""
    status = ""
    timestamp = ""
    pass

class User(BaseModel):
    jid = ""
    name = ""
    pass