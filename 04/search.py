#!/usr/bin/env python

from sys import argv
import json
import sqlite3


def main():
    
    connect_DB = sqlite3.connect("scorelib.dat")
    cursor_DB = connect_DB.cursor()
    composer_name_w = '%' + argv[1] + '%'
    composers = dict()
    
    composer_id_w = cursor_DB.execute(
        """SELECT DISTINCT person.id, person.name FROM print
        JOIN edition ON print.edition = edition.id
        JOIN score ON edition.score = score.id
        JOIN score_author ON score_author.score = score.id
        JOIN person ON score_author.composer = person.id
        WHERE person.name LIKE ?;""",
        (composer_name_w,)
        ).fetchall()

    
    for composer_id, composer_name, in composer_id_w:
        prints_db = cursor_DB.execute(
            """SELECT print.id, print.partiture,
                      edition.id, edition.year, edition.name,
                      score.id, score.name, score.genre, score.key,
                      score.incipit, score.year FROM print
                JOIN edition ON print.edition = edition.id
                JOIN score ON edition.score = score.id
                JOIN score_author ON score_author.score = score.id
                JOIN person ON score_author.composer = person.id
                WHERE person.id = ?;""",
            (composer_id,)
        ).fetchall()
        prints = []

        
        for (print_id, print_partiture, edition_id, edition_year, edition_name,
             score_id, score_name, score_genre, score_key, score_incipit,
             score_year) in prints_db:

            one_print = dict()
            one_print['Print Number'] = print_id
            one_print['Partiture'] = True if print_partiture == 'Y' else False
            if score_name:
                one_print['Title'] = score_name
            if score_genre:
                one_print['Genre'] = score_genre
            if score_key:
                one_print['Key'] = score_key
            if score_incipit:
                one_print['Incipit'] = score_incipit
            if score_year:
                one_print['Composition Year'] = score_year
            if edition_name:
                one_print['Edition'] = edition_name

            editors_db = cursor_DB.execute(
                """SELECT DISTINCT person.name, person.born,
                        person.died FROM person
                    JOIN edition_author ON edition_author.editor = person.id
                    JOIN edition ON edition_author.edition = edition.id
                    WHERE edition.id = ?""",
                (edition_id,)
            ).fetchall()
            editors = []
            for editor_name, editor_born, editor_died in editors_db:
                editor = dict()
                if editor_name:
                    editor['name'] = editor_name
                if editor_born:
                    editor['born'] = editor_born
                if editor_died:
                    editor['died'] = editor_died
                if editor:
                    editors.append(editor)
            if len(editors) > 0:
                one_print['Editor'] = editors

            print_composers_db = cursor_DB.execute(
                """SELECT DISTINCT person.name, person.born,
                        person.died FROM person
                    JOIN score_author ON score_author.composer = person.id
                    WHERE score_author.score = ?""",
                (score_id,)
            ).fetchall()
            print_composers = []

            
            for name, born, died in print_composers_db:
                print_composer = dict()
                if name:
                    print_composer['name'] = name
                if born:
                    print_composer['born'] = born
                if died:
                    print_composer['died'] = died
                if print_composer:
                    print_composers.append(print_composer)
            if len(print_composers) > 0:
                one_print['Composer'] = print_composers

            voices_db = cursor_DB.execute(
                """SELECT voice.name, voice.range FROM voice
                    WHERE voice.score = ?""",
                (score_id,)
            ).fetchall()
            voices = []

            
            for voice_name, voice_range in voices_db:
                voice = dict()
                if voice_name:
                    voice['name'] = voice_name
                if voice_range:
                    voice['range'] = voice_range
                if voice:
                    voices.append(voice)
            if len(voices) > 0:
                one_print['Voices'] = voices
            prints.append(one_print)
        composers[composer_name] = prints

    print(json.dumps(composers, indent=2, ensure_ascii=False))
    connect_DB.close()


if __name__ == '__main__':
    main()
