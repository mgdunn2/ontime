import sqlite3, sys

if len(sys.argv) != 2:
    print "Select one upgrade file"
    sys.exit()
upgradeFile = sys.argv[1]

qry = open(upgradeFile, 'r').read()
conn = sqlite3.connect('bret_db.sqlite')
c = conn.cursor()
c.executescript(qry)
conn.commit()
c.close()
conn.close()
