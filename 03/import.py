import utils
import sqlite3
import traceback
from sys import argv


if __name__ == '__main__':
    input = argv[1]
    output = argv[2]

    script = ''
    with open('scorelib.sql') as schema:
        script = schema.read()

    try:
        conn = sqlite3.connect(output)
        conn.executescript(script)
        utils.load(input, conn)
        conn.commit()


    except:
        getback = traceback.format_exc()
        print(getback)
