import sys
import json
from functools import wraps
from flask import Flask, render_template, make_response, jsonify, request, abort
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, time, timedelta
from dateutil import parser
from db.bretDb import insertCheckin, getAllCheckins

confData = json.load(open('ontime.conf'))

application = Flask(__name__)
auth = HTTPBasicAuth()

users = confData["users"]

APPKEYS = confData["APPKEYS"]

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
    from db.bretDb import insertCheckin, getAllCheckins
    checkins = getAllCheckins()
    checkinTime = getFirstCheckinForDay(checkins)
    prevCheckinTime = getFirstCheckinForPrevDay(checkins)
    isOnTime = False
    wasOnTimeYesterday = False
    if prevCheckinTime is not None and datetime.now().time() < time(hour=9, minute=45):
        isOnTime = prevCheckinTime.time() < time(hour=9, minute=45)
    elif checkinTime is not None:
        isOnTime = checkinTime.time() < time(hour=9,minute=45)
    return render_template('bretOnTime.html', isOnTime=isOnTime)

def getFirstCheckinForDay(checkins):
    filteredCheckins = []
    if datetime.now().weekday() == 5:
        filteredCheckins = [checkin for checkin in checkins if checkin.date() == (datetime.now() - timedelta(days=1)).date()]
    elif datetime.now().weekday() == 6:
        filteredCheckins = [checkin for checkin in checkins if checkin.date() == (datetime.now() - timedelta(days=2)).date()]
    else:
        filteredCheckins = [checkin for checkin in checkins if checkin.date() == datetime.now().date()]
    if len(filteredCheckins) > 0:
        return filteredCheckins[0]
    else:
        return None

def getFirstCheckinForPrevDay(checkins):
    filteredCheckins = []
    if (datetime.now() - timedelta(days=1)).weekday() == 5:
        filteredCheckins = [checkin for checkin in checkins if checkin.date() == ((datetime.now() - timedelta(days=1)) - timedelta(days=1)).date()]
    elif (datetime.now() - timedelta(days=1)).weekday() == 6:
        filteredCheckins = [checkin for checkin in checkins if checkin.date() == ((datetime.now() - timedelta(days=1)) - timedelta(days=2)).date()]
    else:
        filteredCheckins = [checkin for checkin in checkins if checkin.date() == (datetime.now() - timedelta(days=1)).date()]
    if len(filteredCheckins) > 0:
        return filteredCheckins[0]
    else:
        return None

@application.route("/checkin/<appkey>/test", methods=["POST"])
@require_appkey
def test(appkey):
    checkinTime = datetime.now()
    if request.json and 'datetime' in request.json:
        checkinTime = parser.parse(request.json['datetime'])
    return jsonify(checkinTime) 

@application.route("/checkin/list")
@auth.login_required
def checkinList():
    return jsonify(getAllCheckins())

@application.route("/checkin", methods=["POST"])
@auth.login_required
def checkin():
    insertCheckin(datetime.now())
    return str(list(reversed(getAllCheckins()))[0])

@application.route("/addtime", methods=["POST"])
@auth.login_required
def addtime():
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
