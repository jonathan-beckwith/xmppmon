import site
site.addsitedir('/home/jonathan/.virtualenvs/xmpp-monitor/lib/python3.4/site-packages')

import logging, sys
logging.basicConfig(stream=sys.stderr)

from xmpp_monitor.server import app as application