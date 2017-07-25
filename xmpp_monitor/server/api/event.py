from flask.views import MethodView
from flask.json import jsonify

from flask import request

from xmpp_monitor import database
from xmpp_monitor.database import models

from dateutil.parser import parse as dateparse
from dateutil import tz

import datetime

class Event(MethodView):

    class QueryArguments:
        def __init__(self, args):
            self.jid = args.get('jid', '')
            if self.jid.strip() == '':
                self.jid = None

            # Start Date
            self.startdate = args.get('startdate', '')
            if self.startdate == '':
                self.startdate = datetime.datetime.now()
                self.startdate.replace(hour=0, minute=0, second=0)
            else:
                self.startdate = dateparse(self.startdate)
            if self.startdate.tzinfo == None:
                self.startdate = self.startdate.replace(tzinfo=tz.tzutc())

            # End Date
            self.enddate = args.get('enddate', '')
            if self.enddate == '':
                self.enddate = self.startdate
                self.enddate = self.enddate.replace(hour=23, minute=0, second=0)
            else:
                self.enddate = dateparse(self.enddate)
            if self.enddate.tzinfo == None:
                self.enddate = self.enddate.replace(tzinfo=tz.tzutc())

    def get(self, id):
        args = self.QueryArguments(request.args)
        data = { 
            "events": database.get_events(
                jid=args.jid,
                startdate=args.startdate,
                enddate=args.enddate
            )
        }

        return jsonify(data)
        pass

    def post(self):
        data = request.get_json()
        #create a new event
        if data:
            event = models.Event(
                jid=data['jid'],
                status=data['status'],
                timestamp=data['timestamp']
            )
            event.save()
            return jsonify({
                "jid": event.jid,
                "status": event.status,
                "timestamp": dateparse(event.timestamp)
            });

        return jsonify({ "error": "No Data Provided" })
        pass

    def delete(self, id):
        #delete a single event
        event = models.Event.get(models.Event.jid == id)
        event.delete_instance()
        pass

    def put(self, id):
        #update a single event
        pass
