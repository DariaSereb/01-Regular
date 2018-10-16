import sys
import re


class Print:

    def __init__(self, edition, print_id, partiture):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def composition(self):
        return self.edition.composition

    
    def format(self):
        result = ''
        result += 'Print number:' + putSpace (str(self.print_id)) + '\n'
        result += 'Composer:' + putSpace(printPeople(self.composition().authors, ";")) + "\n"
        result += 'Title:' + putSpace(checkNone(self.composition().name)) + "\n"
        result += 'Genre:' + putSpace(checkNone(self.composition().genre)) + "\n"
        result += 'Key:' + putSpace(checkNone(self.composition().key)) + "\n"
        result += 'Composition Year:' + putSpace(str(checkNone(self.composition().year))) + "\n"
        result += 'Edition:' + putSpace(checkNone(self.edition.name)) + "\n"
        result += 'Editor:' + putSpace(printPeople(self.edition.authors, ",")) + "\n"
        result += printVoices(self.composition().voices)
        result += 'Partiture:' + putSpace(printPartiture(self.partiture)) + "\n"
        result += 'Incipit:' + putSpace(checkNone(self.composition().incipit))
        print(result)


class Voice:
    def __init__(self, name,range_voice):
        self.name = name
        self.range =range_voice


class Person:
    def __init__(self, name, born=None, died=None):
        self.name = name
        self.born = born
        self.died = died

class Edition:
    def __init__(self, composition, authors, name):
        self.composition = composition
        self.authors = [] 
        self.name = name.strip() if name else None


class Composition:
    
    def __init__(self,name,incipit,key,genre,year,voices,authors):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = voices 
        self.authors = authors
        
def check (value):
    if value == None:
        return ''
    elif value == '':
            return value
    elif value is None:
            return None
    else:
        return value
    return value


def Voices_prints (voices):
    prints = ''
    i = 1

    for v in voices:
        prints += 'Voice ' + str(i) + ':'

        if v != None:
            if v.range != None and v.name != None:
                prints += v.range + ', ' + v.name
            elif v.range != None and v.name == None:
                prints += v.range
            elif v.range == None and v.name != None:
                prints += v.name

        i += 1
        prints += '\n'

    return prints
           
    
def get_data():
    data = {'composers': []}
    return data

def Person_print(people, separator):
    prints = ""
    i = 1

    for p in people:
        if i != 1:
            prints += separator + " "

        prints += p.name

        if p.born != None or p.died != None:
            prints += " (" + str(checkNone(p.born)) + "--" + str(checkNone(p.died)) + ")"

        i = i + 1

    return prints

def printPartiture(value):
    if value == 'Y':
        return "yes"
    elif value == 'P':
        return "partial"
    else:
        return "no"

def Person_comp(people, deliminator):
    prints = []
    
    if people != None:
        clean = people.split(';')
        clean = map(str.strip, clean)
        clean = list(filter(None, clean))
        
        person1= re.compile( r'.*\(\*([0-9]{4})\)' )
        person2 = re.compile( r'.*\(\+([0-9]{4})\)' )
        person3 = re.compile( r'.*\(([0-9]{4})?(-{1,2})([0-9]{4})?\)' )
        
        for item in clean:
            name = re.sub( r'\(.*\)', '', item )
            name = name.strip()

            person1_1 = person1.match(item)
            person2_1 = person2.match(item)
            person3_1 = person.match(item)

            if person1_1 is not None:
                prints.append(Person(name, intNone(person1_1.group(1)), intNone(person1_1.group(3))))
            elif person2_1 is not None:
                prints.append(Person(name, int(person2_1.group(1)), None))
            elif person3_1 is not None:
                prints.append(Person(name, None, int(person3_1.group(1))))
            else:
                prints.append(Person(name, None, None))

    return prints

def Editor_comp(editors):
    prints = []

    clean = re.sub( r'\(.*\)', '', editors )
    clean = clean.split(',')
    clean = map(str.strip, clean)
    clean = list(filter(None, clean))

    name = ""

    for item in clean:
        if name == "":
            name += item
        else:
            if item.find(' ') == -1:
                name += ", " + item
                prints.append(Person(name, None, None))
                name = ""
            else:
                prints.append(Person(name, None, None))
                prints.append(Person(item, None, None))
                name = ""

    if name != "":
        prints.append(Person(name, None, None))

    return prints



def Voices_comp(dict):
    prints = []
    index = 1

    range_prints = re.compile ( r'(.*?--.*?)($|\,)(.*)' )
    
    while 'Voice ' + str(index) in dict:
        voice = dict['Voice ' + str(index)]

        if voice is None:
            prints.append(None)
        else:
            voice = voice.replace(';', ',')
            range_prints2 = range_prints.match(voice)

            if range_prints2 is not None:
                Range = range_prints2.group(1).strip()
                Name = range_prints2.group(3).strip()

                if Name == "":
                    prints.append(Voice(None, Range))
                else:
                    prints.append(Voice(Name, Range))
            else:
                prints.append(Voice(voice, None))
        index += 1
    return prints


def Print_Item(item):
    p = Print(None, None, None)  
    p.print_id = int(item['Print Number'])


    if 'Editor' in item:
        if item['Editor'] is None:
            p.edition.authors = []
        else:
            p.edition.authors = parseEditors(item['Editor'])
    else:
        p.edition.authors = []

    p.edition.composition = Composition(item['Title'], item['Incipit'], None, None, None, None, None)
    
    if 'Genre' in item:
        p.edition.composition.genre = item['Genre']
    else:
        p.edition.composition.genre = None

    
    if item['Partiture'] != None:
        
        if item['Partiture'].find("partial") is not -1:
            p.partiture = 'P'
        elif item['Partiture'].find("yes") is not -1:
            p.partiture = 'Y'
        else:
            p.partiture = 'N'
    else:
        p.partiture = 'N'

    p.edition = Edition(None, None, item['Edition'])

    if 'Key' in item:
        p.edition.composition.key = item['Key']
    else:
        p.edition.composition.key = None
    p.edition.composition.authors = Person_comp(item['Composer'], ";")


    if 'Composition Year' in item and item['Composition Year'] != None:
        yearR = re.compile( r"(.*?)([0-9]{4})" )
        yearM = yearR.match(item['Composition Year'])

        if yearM is not None:
            p.edition.composition.year = int(yearM.group(2))
        else:
            p.edition.composition.year = None
    else:
        p.edition.composition.year = None

    p.edition.composition.voices = parseVoices(item)

    return p



def load(filename):
    resul = []
    f = open(filename, 'r', encoding='utf8')
    prints= {}

    line =  re.compile( r"(.*?):(.*)" )

    for line in f:
        line_match = line.match(line)

        if line_match is None:
            continue

        label = line_match.group(1).strip()
        value = line_match.group(2).strip()

        if value != '':
            printItem[label] = value
        else:
            printItem[label] = None

        if label == 'Incipit':
            resul.append(parsePrintItem(printItem))
            prints = {}

    return sorted(resul, key=lambda x: x.print_id)
