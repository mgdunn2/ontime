import os
import sys
import sqlite3
import json

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

confData = json.load(open(get_script_path() + '/ontime.conf'))

sql_file = get_script_path() + '/db/' + confData["sql_file"]

def openConnection():
    return sqlite3.connect(sql_file, detect_types=sqlite3.PARSE_DECLTYPES)

def transaction(func):
    def new_func(*args, **kwargs):
        print "something"
        connection = openConnection()
        cursor = connection.cursor()
        try:
            retval = func(cursor, *args, **kwargs)
            connection.commit()
        except:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

        return retval

    # Tidy up the help()-visible docstrings to be nice
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__

    return new_func

@transaction
def insertCheckin(cursor, datetime):
    cursor.execute('SELECT max(`id`) from `checkins`;')
    #self.cursor.execute('SELECT * from `checkins`;')
    results = cursor.fetchall()
    if results is None or len(results) == 0 or results[0][0] == None:
        nextId = 0
    else:
        nextId = results[0][0] + 1
    cursor.execute('insert into `checkins` values(?, ?)', (nextId, datetime))

@transaction
def getAllCheckins(cursor):
    cursor.execute('SELECT `check_in_time` from `checkins`;')
    return sorted([result[0] for result in cursor.fetchall()])

