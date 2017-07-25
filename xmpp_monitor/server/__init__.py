from flask import Flask
from flask import request

from .api import User, Event

from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

from ..database import models
from .. import presence
from .. import database

# Create Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = '478641g2sdfgdegwerg5v1s23etgK^*%#&($*'

admin = Admin(app, name='xmpp_monitor', template_mode='bootstrap3')
admin.add_view(ModelView(models.User))
admin.add_view(ModelView(models.Event))

def start():
    #Run the server
    app.run(debug=True)

# This hook ensures that a connection is opened to handle any queries
# generated by the request.
@app.before_request
def _db_connect():
    database.connect()

# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(exc):
    database.close()

@app.route('/exit')
def stop():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/')
def index():
    return app.send_static_file('index.html')
    
def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(
        url,
        defaults={ pk: None },
        view_func=view_func,
        methods=['GET',]
    )
    app.add_url_rule(
        url,
        view_func=view_func,
        methods=['POST',]
    )
    app.add_url_rule(
        '%s<%s:%s>' % (url, pk_type, pk),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE']
    )

# Register Views (REST)
register_api(User, 'user_api', '/users.json')
register_api(Event, 'event_api', '/events.json')
