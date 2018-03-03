from db.bretDb import insertCheckin, getAllCheckins
from datetime import datetime, timedelta, time

class checkins():
    @staticmethod
    def getAll():
        print getAllCheckins()

    def __init__(self):
        self.checkins = getAllCheckins()

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
        if prevCheckinTime is not None and datetime.now().time() < time(hour=9, minute=45):
            return prevCheckinTime.time() < time(hour=9, minute=45)
        elif checkinTime is not None:
            return checkinTime.time() < time(hour=9,minute=45)
        return False