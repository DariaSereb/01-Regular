import sys
import sqlite3

txt_file = sys.argv[1]
dat_file = sys.argv[2]

print (txt_file)
print (dat_file)

try:
    db = sqlite3.connect(datFile)
    cursor = db.cursor()
    print (sqlite3.version)
except Exception as e:
    db.rollback()
    raise e
finally:
    db.close()
    
