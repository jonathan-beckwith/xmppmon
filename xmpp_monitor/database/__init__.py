from .peewee import models, init

from dateutil.parser import parse as dateparse
from dateutil import tz

def initialize():
    init()
    
from .peewee import db
def connect():
    db.connect()
def close():
    if not db.is_closed():
        db.close()

def get_events(jid=None,startdate=None,enddate=None):
    events = []
    event_list = models.Event.select()

    #Set Defaults
    if jid is not None and jid.strip() != '':
        event_list = event_list.where(
            models.Event.jid == jid
        )
    
    event_list = event_list.where(
        (models.Event.timestamp >= startdate) &
        (models.Event.timestamp <= enddate)
    )

    last_status = {}
    aggregate_event = {}

    for event in event_list:

        if event.timestamp.tzinfo == None:
            event.timestamp = event.timestamp.replace(tzinfo=tz.tzutc())

        if event.timestamp <= startdate or event.timestamp >= enddate :
            continue

        if event.status.lower() != last_status.get(event.jid, None):
            last_status[event.jid] = event.status.lower()

            if event.jid in aggregate_event:
                aggregate_event[event.jid]["id"] += ":" + str(event.id)
                aggregate_event[event.jid]["end"] = dateparse(str(event.timestamp))

            if event.jid in aggregate_event:
                events.append(aggregate_event[event.jid])
                del aggregate_event[event.jid]
                aggregate_event[event.jid] = {
                    "id": str(event.id),
                    "jid": event.jid,
                    "status": event.status,
                    "start": dateparse(str(event.timestamp))
                }
        else:
            aggregate_event[event.jid] = {
                "id": str(event.id),
                "jid": event.jid,
                "status": event.status,
                "start": dateparse(str(event.timestamp))
            }

    events.sort(key=lambda event: event["start"])
    return events