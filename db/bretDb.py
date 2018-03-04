import os
import sys
import sqlite3
import json
from db import transaction

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
confData = json.load(open(get_script_path() + '/ontime.conf'))
bret_sql_file = get_script_path() + '/db/' + confData["sql_file"]

@transaction(bret_sql_file)
def insertCheckin(cursor, datetime):
    cursor.execute('SELECT max(`id`) from `checkins`;')
    results = cursor.fetchall()
    if results is None or len(results) == 0 or results[0][0] == None:
        nextId = 0
    else:
        nextId = results[0][0] + 1
    cursor.execute('insert into `checkins` values(?, ?)', (nextId, datetime))

@transaction(bret_sql_file)
def getAllCheckins(cursor):
    cursor.execute('SELECT `check_in_time` from `checkins`;')
    return sorted([result[0] for result in cursor.fetchall()])

