from db.bretDb import insertCheckin, getAllCheckins
from datetime import datetime, timedelta, time

class checkins():
    def __init__(self, onTimeTime):
        self.checkins = getAllCheckins()
        self.relevantCheckins = self.getRelevantCheckins()
        self.onTimeTime = onTimeTime

    def getRelevantCheckins(self):
        weekdays = [checkin for checkin in self.checkins if checkin.weekday() < 5]
        s = set()
        relevantCheckins = []
        for checkin in weekdays:
            if checkin.date() in s:
                continue
            s.add(checkin.date())
            relevantCheckins.append(checkin)
        return {dateTime.date(): dateTime for dateTime in relevantCheckins}

    def getFirstCheckinForDayReturnFridayIfWeekend(self, dateTime=datetime.now()):
        if dateTime.weekday() == 5:
            dateTime = dateTime - timedelta(days=1)
        if dateTime.weekday() == 6:
            dateTime = dateTime - timedelta(days=2)
        if dateTime.date() in self.relevantCheckins:
            return self.relevantCheckins[dateTime.date()]
        return None

    def getMostRecent(self):
        return list(reversed(self.checkins))[0]

    def isOnTime(self, dateTime=datetime.now()):
        dateTime = dateTime
        checkin = self.getFirstCheckinForDayReturnFridayIfWeekend(dateTime)
        print checkin
        # If there is a checkin time for the day, see if it is on time
        if checkin is not None:
            print checkin.time(), self.onTimeTime
            if checkin.time() < self.onTimeTime:
                return 1
            else:
                return -1
        # If there isn't a checkin yet but we aren't past the late time
        # then return 0 to indicate that it's a maybe
        if dateTime.time() < self.onTimeTime:
            return 0
        # Finally, there's no checkin and it's past time so return -1 for late
        return -1

    def getStreak(self, dateTime=datetime.now()):
        count = 0
        result = 0
        while result >= 0:
            result = self.getIfOnTimeWeekday(dateTime)
            if result == 1:
                count = count + 1
            dateTime = dateTime - timedelta(days=1)
        return count

    def getIfOnTimeWeekday(self, dateTime):
        if dateTime.weekday() > 4:
            return 0
        return self.isOnTime(dateTime)





