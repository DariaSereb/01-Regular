#!/usr/bin/env python

from sys import argv
import json
import sys
import sqlite3


def main():
    print_number = argv[1]
    connect_DB = sqlite3.connect("scorelib.dat")
    cursor_DB = connect_DB.cursor()
    score = cursor_DB.execute(
        """SELECT score.id FROM print
        INNER JOIN edition ON print.edition = edition.id
        INNER JOIN score ON edition.score = score.id
        WHERE print.id = ?""",
        (print_number,)
    ).fetchall()
    if not score:
        return
    else:
        score = score[0][0]
    composers_DB = cursor_DB.execute(
        """SELECT name, born, died FROM score_author
        INNER JOIN person ON score_author.composer = person.id
        WHERE score_author.score = ?""",
        (score,)
    ).fetchall()
    composers = []
    for composer in composers_DB:
        person = {}
        if composer[0]:
            person['name'] = composer[0]
        if composer[1]:
            person['born'] = composer[1]
        if composer[2]:
            person['died'] = composer[2]
        composers.append(person)
    print(json.dumps(composers, indent=2, ensure_ascii=False))
    connect_DB.close()


if __name__ == '__main__':
    main()
