import sys
import re

class Voice:
    def __init__(self, range, name):
        self.name = name
        self.range = range

    def print_voice(self):
        name = str(self.name) if self.name is not None else ''
        range = None
        if len(name) > 0:
            range = str(self.range) + ', ' if self.range is not None else ''
        else:
            range = str(self.range) if self.range is not None else ''
        return range + name

class Person:
    def __init__(self, name, born, died):
        self.name = name
        self.born = born
        self.died = died

    def person_string(self):
        name = self.name if self.name is not None else ''
        born = str(self.born) if self.born is not None else ''
        died = str(self.died) if self.died is not None else ''
        born_died = ' (' + born + '--' + died + ')' if self.born is not None or self.died is not None else ''
        return name + born_died

class Edition:
    def __init__(self, name, authors, composition):
        self.name = name
        self.authors = authors
        self.composition = composition

    def print_edition(self):
        if self.composition is not None:
            self.composition.print_first_part()
        if self.name is not None:
            print("Edition: " + self.name)
        if self.authors:
            print("Editor: " + ', '.join(str(author.person_string()) for author in self.authors))
        if self.composition is not None:
            self.composition.print_voices()


class Composition:
    def __init__(self, name, incipit, key, genre, year, voices, authors):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = voices
        self.authors = authors

    def print_incipit(self):
        if self.incipit is not None:
            print("Incipit: " + self.incipit)

    def print_first_part(self):
        if self.authors:
            print("Composer: ", end='', flush=True)
            print('; '.join(str(author.person_string()) for author in self.authors))
        if self.name is not None:
            print("Title: " + self.name)
        if self.genre is not None:
            print("Genre: " + self.genre)
        if self.key is not None:
            print("Key: " + self.key)
        if self.year is not None:
            print("Composition Year: " + str(self.year))

    def print_voices(self):
        if self.voices:
            for i, voice in enumerate(self.voices):
                if voice is not None:
                    print("Voice " + str(i+1) + ": " + voice.print_voice())
                else:
                    print("Voice " + str(i+1) + ": ")


class Print:
    def __init__(self, edition, print_id, partiture):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def format(self):
        if self.print_id is not None:
            print("Print Number: " + str(self.print_id))
        if self.edition is not None:
            self.edition.print_edition()
        if self.partiture is not None:
            if self.partiture:
                print("Partiture: yes")
            else:
                print("Partiture: no")
        if self.edition is not None and self.composition() is not None:
            self.composition().print_incipit()

    def composition(self):
        return self.edition.composition

def load(filename):
    prints = []
    print_object = None
    print_id = None
    partiture = None
    edition_name = None
    edition = None
    composition = None
    composition_name = None
    incipit = None
    key = None
    genre = None
    year = None
    voices = []
    composers = []
    editors = []

    for line in open(filename, 'r', encoding='UTF8'):
        if line == "\n" and print_id != None:
            composition = Composition(composition_name, incipit, key, genre, year, voices.copy(), composers.copy())
            edition = Edition(edition_name, editors.copy(), composition)
            print_object = Print(edition, print_id, partiture)
            prints.append(print_object)
            prints = prints.copy()

            print_object = None
            print_id = None
            partiture = None
            edition_name = None
            composition_name = None
            incipit = None
            key = None
            genre = None
            year = None
            composition = None
            edition = None
            voices = []
            composers = []
            editors = []
        else:
            id_regex = re.compile( r"Print Number: (.*)" )
            edition_name_regex = re.compile( r"Edition: (.*)" )
            composer_regex = re.compile(r"Composer: (.*)")
            editor_regex = re.compile(r"Editor: (.*)")
            year_regex = re.compile(r"Composition Year: (.+ )*(\d{4})( .+)*$")
            partiture_regex = re.compile(r"Partiture: (.*)")
            genre_regex = re.compile(r"Genre: (.*)")
            key_regex = re.compile(r"Key: (.*)")
            incipit_regex = re.compile(r"Incipit: (.*)")
            title_regex = re.compile(r"Title: (.*)")
            voice_regex = re.compile(r"Voice .*:(.*)")

            is_print_id = id_regex.match(line)
            is_edition_name = edition_name_regex.match(line)
            is_composer = composer_regex.match(line)
            is_editor = editor_regex.match(line)
            is_year = year_regex.match(line)
            is_partiture = partiture_regex.match(line)
            is_genre = genre_regex.match(line)
            is_key = key_regex.match(line)
            is_incipit = incipit_regex.match(line)
            is_title = title_regex.match(line)
            is_voice = voice_regex.match(line)

            if is_print_id:
                print_id = int(is_print_id.group(1).strip())
            elif is_partiture:
                partiture_text = is_partiture.group(1)
                partiture = None
                if 'yes' in partiture_text:
                    partiture = True
                else:
                    partiture = False
            elif is_edition_name:
                edition_name = is_edition_name.group(1).strip()
            elif is_title:
                composition_name = is_title.group(1).strip()
            elif is_incipit:
                incipit = is_incipit.group(1).strip()
            elif is_key:
                key = is_key.group(1).strip()
            elif is_genre:
                genre = is_genre.group(1).strip()
            elif is_year:
                if len(is_year.group(2).strip()) > 0:
                    year = int(is_year.group(2).strip())
            elif is_composer:
                s = is_composer.group(1).split(';')
                for composer in (s):
                    something = re.split(r'\(|\)', composer)
                    cleared_name = something[0].strip()
                    if len(something) > 1:
                        splitted_dash = None
                        if '-' in something[1]:
                            splitted_dash = re.split(r'-+', something[1])
                        regex_dash = re.compile(r"^\d{4}$")
                        regex_asterix = re.compile(r"^\*(\d{4})$")
                        regex_plus = re.compile(r"^\+(\d{4})$")
                        is_dash = regex_dash.match(something[1])
                        is_asterix = regex_asterix.match(something[1])
                        is_plus = regex_plus.match(something[1])
                        if splitted_dash is not None:
                            is_born = regex_dash.match(splitted_dash[0])
                            is_died = regex_dash.match(splitted_dash[1])
                            born = None
                            died = None
                            if is_born:
                                born = int(splitted_dash[0])
                            if is_died:
                                died = int(splitted_dash[1])
                            composers.append(Person(cleared_name, born, died))
                        elif is_asterix:
                            composers.append(Person(cleared_name, int(is_asterix.group(1)), None))
                        elif is_plus:
                            composers.append(Person(cleared_name, None,  int(is_plus.group(1))))
                        else:
                            if len(cleared_name) >0:
                                composers.append(Person(cleared_name, None,  None))
                    elif len(cleared_name) >0:
                        composers.append(Person(cleared_name, None,  None))
            elif is_editor:
                to_join = None
                line = is_editor.group(1)
                split = line.split(',')
                if len(split) < 2:
                    editors.append(Person(split[0].strip(), None, None))
                else:
                    for name in split:
                        name = name.strip()
                        if to_join is not None:
                            editors.append(Person(to_join + ', ' + name, None, None))
                            to_join = None
                        elif ' ' in name:
                            editors.append(Person(name, None, None))
                        else:
                            to_join = name
            elif is_voice:
                line = is_voice.group(1).strip()
                if '--' not in line and len(line) > 0:
                    voices.append(Voice(None ,line))
                else:
                    regex_range_name = re.compile(r"([^,|;]+--[^,|;]+)[,|;] (.*)")
                    regex_range = re.compile(r"([^,|;]+--[^,|;]+)([,|;] (.*))*")
                    is_regex_range_name = regex_range_name.match(line)
                    is_regex_range = regex_range.match(line)
                    if is_regex_range_name:
                        voices.append(Voice(is_regex_range_name.group(1), is_regex_range_name.group(2)))
                    elif is_regex_range:
                        voices.append(Voice(is_regex_range.group(1), None))
                    else:
                        voices.append(None)
    composition = Composition(composition_name, incipit, key, genre, year, voices.copy(), composers.copy())
    edition = Edition(edition_name, editors.copy(), composition)
    print_object = Print(edition, print_id, partiture)
    prints.append(print_object)
    prints = prints.copy()

    return prints
