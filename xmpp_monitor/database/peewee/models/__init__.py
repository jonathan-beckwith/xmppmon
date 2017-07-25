from .user import User
from .event import Event

def create_tables(db):
    db.create_tables([
    	User, Event
    ])
