from flask.views import MethodView
from flask.json import jsonify

from flask import request

from xmpp_monitor import database
from xmpp_monitor.database import models

class User(MethodView):

    def get(self, id=None):
        data = { "users": [] }

        if id == None:
            user_list = models.User.select()
        else:
            user_list = models.User.select().where(
                models.User.jid==id
            )
        
        for user in user_list:
            data["users"].append({
                "name": user.name,
                "jid": user.jid
            })
        return jsonify(data)
        pass

    def post(self):
        data = request.get_json()
        #create a new user
        if data:
            user = models.User(
                name=data['name'],
                jid=data['jid']
            )
            user.save()
            return jsonify({
                "name": user.name,
                "jid": user.jid
            });

        return jsonify({ "error": "No Data Provided" })
        pass

    def delete(self, id):
        #delete a single user
        pass

    def put(self, id):
        #update a single user
        pass
