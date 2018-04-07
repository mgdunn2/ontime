from db.bretDb import insertCheckin, getAllCheckins
from datetime import datetime, timedelta, time

class checkins():
    def __init__(self, onTimeTime):
        self.checkins = getAllCheckins()
        self.onTimeTime = onTimeTime

    def getFirstCheckinForDay(self):
        checkins = self.checkins
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

    def getFirstCheckinForPrevDay(self):
        checkins = self.checkins
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

    def getMostRecent(self):
        return list(reversed(self.checkins))[0]

    def isOnTime(self):
        checkinTime = self.getFirstCheckinForDay()
        prevCheckinTime = self.getFirstCheckinForPrevDay()
        if prevCheckinTime is not None and datetime.now().time() < self.onTimeTime:
            return prevCheckinTime.time() < self.onTimeTime
        elif checkinTime is not None:
            return checkinTime.time() < self.onTimeTime
        return False

    def getRelevantCheckins(self):
        weekdays = [checkin for checkin in self.checkins if checkin.weekday() < 5]
        s = set()
        relevantCheckins = []
        for checkin in weekdays:
            if checkin.date() in s:
                continue
            s.add(checkin.date())
            relevantCheckins.append(checkin)
        return relevantCheckins

