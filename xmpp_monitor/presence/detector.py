import ssl
import os

import logging
log = logging.getLogger(__name__)

from sleekxmpp import ClientXMPP
#from sleekxmpp.exceptions import IqError, IqTimeout

from datetime import datetime

from xmpp_monitor.database import models
from .. import database 

STATUS_TYPES = {
    'chat': 'Prefer Chat',
    'dnd': 'Do Not Disturb',
    'available': 'Available',
    'away': 'Away',
    'xa': 'Extended Away'
}

class PresenceHandler():
    def __init__(self):
        pass

    def save_event(self, event):
        if event['type'] != '':
            database.connect()
            status = event['status'].strip()
            
            if status == '':
                status = STATUS_TYPES.get(event['type'], event['type'])

            db_event = models.Event(
                jid=str(event['from'])[:4],
                status=status,
                timestamp=datetime.utcnow()
            )
            retval = str({
                'jid': db_event.jid,
                'status': db_event.status,
                'timestamp': db_event.timestamp
            })
            db_event.save()
            database.close()
            return retval 
        return False

    def on_available(self, event):
        print("AVAILABLE:", self.save_event(event))
        pass

    def on_unavailable(self, event):
        print("UNAVAILABLE:", self.save_event(event))
        pass

    def on_online(self, event):
        print("ONLINE:", self.save_event(event))

    def on_offline(self, event):
        print("OFFLINE:", self.save_event(event))

    def on_change(self, event):
        print("CHANGE:", self.save_event(event))


class PresenceBot(ClientXMPP):

    def __init__(self, jid, password):
        super().__init__(jid, password, sasl_mech='PLAIN')

        self.presence = PresenceHandler()
        self.add_event_handler("session_start", self.session_start)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        self.subscribe_to_all()

        self.add_event_handler("message", self.message)
        self.add_event_handler("changed_status", self.presence.on_change)

        self.add_event_handler("got_online", self.presence.on_online)
        self.add_event_handler("got_offline", self.presence.on_offline)

        self.add_event_handler("presence_available", self.presence.on_available)
        self.add_event_handler("presence_unavailable", self.presence.on_unavailable)

    def listen_to_user(self, _id):
        jid = _id + os.environ['XMPP_DOMAIN']
        self.sendPresenceSubscription(
            pto=jid,
            ptype="subscribe"
        )

    def subscribe_to_all(self):
        users = models.User.select()
        for user in users:
            self.listen_to_user(user.jid)

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            if msg['body'] == 'reset users':
                self.subscribe_to_all()
            if msg['body'] == '/stop scan':
                exit()


xmpp = PresenceBot(os.environ['XMPP_USER'], os.environ['XMPP_PASSWORD'])
def start():
    # Ideally use optparse or argparse to get JID,
    # password, and log level.

    logging.basicConfig(level=logging.WARNING)

    xmpp['feature_mechanisms'].unencrypted_plain = True
    xmpp.ssl_version = ssl.PROTOCOL_SSLv23
    xmpp.connect(use_ssl=False, use_tls=False)
    xmpp.process(block=True)
    xmpp.subscribe_to_all()