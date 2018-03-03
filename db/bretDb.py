import os
import sys
import sqlite3
import json

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

confData = json.load(open(get_script_path() + '/ontime.conf'))

sql_file = get_script_path() + '/db/' + confData["sql_file"]

class db():
    def __init__(self):
        self.connection = None

    def openConnection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(sql_file, detect_types=sqlite3.PARSE_DECLTYPES)
        return self.connection

    def beginTransaction(self):
        self.results = None
        self.cursor = self.openConnection().cursor();

    def fetchall(self):
        self.cursor.fetchall()

    def commitTranscation(self):
        if self.connection is not None:
            self.connection.commit()
            self.results = self.cursor.fetchall()
            self.connection.close()
        self.cursor = None
        self.connection = None

    def rollbackTransaction(self):
        if self.cursor is not None:
            self.cursor.rollback()
        self.results = None
        self.cursor = None

    def insertCheckin(self, datetime):
        self.beginTransaction()
        self.cursor.execute('SELECT max(`id`) from `checkins`;')
        #self.cursor.execute('SELECT * from `checkins`;')
        results = self.cursor.fetchall()
        if results is None or len(results) == 0 or results[0][0] == None:
            nextId = 0
        else:
            nextId = results[0][0] + 1
        self.cursor.execute('insert into `checkins` values(?, ?)', (nextId, datetime))
        self.commitTranscation()

    def getAllCheckins(self):
        self.beginTransaction()
        self.cursor.execute('SELECT `check_in_time` from `checkins`;')
        self.commitTranscation();
        return sorted([result[0] for result in self.results])

