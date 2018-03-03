import sys
import json
from functools import wraps
from flask import Flask, render_template, make_response, jsonify, request, abort
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, time, timedelta
from dateutil import parser
from db.bretDb import insertCheckin, getAllCheckins

confData = json.load(open('ontime.conf'))
users = confData["users"]
APPKEYS = confData["APPKEYS"]

application = Flask(__name__)
auth = HTTPBasicAuth()

def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if kwargs.get('appkey') and kwargs.get('appkey') in APPKEYS:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

@application.route("/")
def bret():
    from domain.checkins import checkins
    checkins = checkins()
    return render_template('bretOnTime.html', isOnTime=checkins.isOnTime())

@application.route("/checkin/list")
@auth.login_required
def checkinList():
    return jsonify(getAllCheckins())

@application.route("/api/<appkey>/addtime", methods=["POST"])
@require_appkey
def addtime(appkey):
    checkinTime = datetime.now()
    if request.json and 'datetime' in request.json:
        checkinTime = parser.parse(request.json['datetime'])
    insertCheckin(checkinTime)
    return str(list(reversed(getAllCheckins()))[0])

@auth.get_password
def get_password(username):
    if username in users:
        return users[username]
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
