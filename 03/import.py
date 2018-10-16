import sys
import sqlite3
import scorelib as module

def initDb(datFile, schemaFile):
    schema = open(schemaFile, 'r').read()

    db = sqlite3.connect(datFile)
    cursor = db.cursor()
    cursor.executescrint(schema)
    db.commit()

    return db


def insert_Score(composition, cursor):
    cursor.execute("SELECT * FROM score WHERE name IS ? AND genre IS ? AND key IS ? AND incipit IS ? AND year IS ?", 
                    (composition.name, composition.genre, composition.key, composition.incipit, composition.year,))
    match = cursor.fetchone()

    if match is None:
        cursor.execute("INSERT INTO score(name, genre, key, incipit, year) VALUES (?, ?, ?, ?, ?)",
                        (composition.name, composition.genre, composition.key, composition.incipit, composition.year))
        return cursor.lastrowid
    else:
        return match[0]
    
def Person_insrt(person, cursor):
    cursor.execute("SELECT * FROM person WHERE name IS ?", (person.name,))
    match = cursor.fetchone()

    if match is None:
        cursor.execute("INSERT INTO person(name, born, died) VALUES(?, ?, ?)", (person.name, person.born, person.died))
        return cursor.lastrowid
    else:
        born = match[1]
        died = match[2]

        if born is None:
            born = person.born
        if died is None:
            died = person.died
        
        cursor.execute("UPDATE person SET born=?, died=? WHERE name=?", (born, died, person.name))
        return match[0]
    
def Edition_insrt(edition, scoreId, cursor):
    cursor.execute("SELECT * FROM edition WHERE score IS ? AND name IS ?", (scoreId, edition.name,))
    match = cursor.fetchone()

    if match is None:
        cursor.execute("INSERT INTO edition(score, name, year) VALUES(?, ?, ?)", (scoreId, edition.name, None))
        return cursor.lastrowid
    else:
        return match[0]

def Voice_insrt(voice, scoreId, number, cursor):
    cursor.execute("SELECT * FROM voice WHERE number IS ? AND score IS ? AND range IS ? AND name IS ?",
                    (number, scoreId, (voice.range if voice is not None else None), (voice.name if voice is not None else None)))
    match = cursor.fetchone()

    if match is None:
        cursor.execute("INSERT INTO voice(number, score, range, name) VALUES(?, ?, ?, ?)", 
                        (number, scoreId, (voice.range if voice is not None else None), (voice.name if voice is not None else None)))

def Edition_insrt(editionId, editorId, cursor):
    cursor.execute("SELECT * FROM edition_author WHERE edition IS ? AND editor IS ?", (editionId, editorId,))
    match = cursor.fetchone()

    if match is None:
        cursor.execute("INSERT INTO edition_author(edition, editor) VALUES(?, ?)", (editionId, editorId))

def Author_insrt(scoreId, composerId, cursor):
    cursor.execute("SELECT * FROM score_author WHERE score IS ? AND composer IS ?", (scoreId, composerId,))
    match = cursor.fetchone()

    if match is None:
        cursor.execute("INSERT INTO score_author(score, composer) VALUES(?, ?)", (scoreId, composerId))

def PrintID_insrt(print, editionId, cursor):
    cursor.execute("SELECT * FROM print WHERE id IS ? AND partiture IS ? AND edition IS ?", (print.print_id, print.partiture, editionId))
    match = cursor.fetchone()

    if match is None:
        cursor.execute("INSERT INTO print(id, partiture, edition) VALUES(?, ?, ?)", (print.print_id, print.partiture, editionId))


        
def Data_insrt(prints,db):
    cursor = db.cursor()
    composerIds = []
    editorIds = []

    for p in prints:
        for composer in p.composition().authors:
            composerIds.append(Person_instr(composer,cursor))
        for editor in p.edition.authors:
            editorsIds.append(Person_instr(editor, cursor))

        scoreId = insertScore(p.composition(), cursor)
        
        for i, voice in enumerate(p.composition().voices):
            Voice_instr(voice, scoreId, i+1, cursor)
        for composerId in composerIds:
            Score_instr(scoreId, composerId, cursor)

        editionId = Edition_instr(p.edition, scoreId, cursor)
        
        for editorId in editorIds:
            Author_instr(editionId, editorId, cursor)

        PrintID_instr(p, editionId, cursor)
        composerIds = []
        editorIds = []

        
def main():
    
    db = initDb(sys.argv[2], "scorelib.sql")
    Data_instr(module.load(sys.argv[1]), db)
    db.commit()
    db.close()

if __name__ == "__main__":
    main()
