import sys
import sqlite3

txt_file = sys.argv[1]
dat_file = sys.argv[2]

db = sqlite3.connect(dat_file)
try:
    cursor = db.cursor()
    print (sqlite3.version)
    print (db)
except Exception as e:
    db.rollback()
    raise e
finally:
    db.close()
    
    
