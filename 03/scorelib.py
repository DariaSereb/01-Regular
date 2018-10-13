import sys
import re


class Print:

    def __init__(self, edition, print_id: int, partiture: bool):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def composition(self):
        return self.edition.composition


    def comp_lines(self, composition):
        composers = composition.authors
        comp = ''
        
        for composer in composers:
            
            if composer.name:
                comp += composer.name
                if composer.born or composer.died:
                    comp += ' ({}--{})'.format(composer.born or '', composer.died or '')
        return comp

    def edit_lines(self, edition):
        return ", ".join([editor.name for editor in edition.authors if editor.name])


    def format(self):
        lines = {
            'print_id': 'Print Number: {}'.format(self.print_id),
            'composers': 'Composer: %s'%format(self.comp_lines(self.composition())),
            'title': 'Title: %s'%format(self.composition().name or ''),
            'genre': 'Genre: %s'%format(self.composition().genre or ''),
            'key': 'Key: %s'%format(self.composition().key or ''),
            'composition_year': 'Composition Year: %s'%format(self.composition().year or ''),
            'edition': 'Edition: %s'%format(self.edition.name or ''),
            'editors': 'Editor: %s'%format(self.edit_lines(self.edition) or ''),
            'voices': 'Voices: %s'%format(self.voice_lines(self.composition().voices)),
            'partiture': 'Partiture: %s'%format('yes' if self.partiture == True else 'no'),
            'incipit': 'Incipit: %s'%format(self.composition().incipit or ''),}
        return '\n'.join(lines.values())


class Voice:
    def __init__(self, name,range_voice):
        self.name = name
        self.range =range_voice

    def __repr__(self):
        return 'Voice: name=.*, range=.*'


class Person:
    def __init__(self, name, born=None, died=None):
        self.name = name
        self.born = born
        self.died = died

    def __repr__(self):
        return 'Person: name=.*; born=.*; died=.*'




class Edition:
    def __init__(self, composition, authors, name):
        self.composition = composition
        self.authors = authors 
        self.name = name

    def __repr__(self):
        return 'Edition: composition=.*, authors=.*, name=.*'


class Composition:
    
    def __init__(self,name,incipit,key,genre,year,voices,authors):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = voices 
        self.authors = authors 

    def __repr__(self):
        return 'Composition: name=.*, incipit=.*, key=.*, genre=.*, year=.*, voices=.*, authors=.*'


def get_data():
    data = {'composers': []}
    return data


def load(filename):
    
    data = get_data()
    prints = []
    match_year = re.compile(r"\d\d\d\d")
    match_voice = re.compile(r"(\w+\d?)--?(\w+\d?)")

   
    with open(filename, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    
    for line in lines:
        
        split1 = line.split(':')
        if not split1[0].strip() or line == lines[-1]:
                        
            author_lib = []
            voice_lib = []
            composition = scorelib.Composition(data.get('title'),data.get('incipit'),data.get('key'),data.get('genre'),data.get('year'),voice_lib,author_lib)
            editors = scorelib.Person(data.get('editor')),
            edition = scorelib.Edition(composition, editors, data.get('edition'))
            
                            
            for author in data.get('composers', []):
                author_lib.append(scorelib.Person(author['name'], author['born'], author['died']))
            
                       
            if data.get('print_id')!= None:              
                print_ = scorelib.Print(edition, data['print_id'], data['partiture'])
                prints.append(print_)
            data = get_data()
            
            continue

        value1 = split1[0].lower()
        value2 = split1[1].strip() if split1[1] else ""
        
        if 'print' in value1:
            data['print_id'] = int(value2)

        elif 'composer' in value1:
            authors = value2.split(';')
            
            for author in authors:
                split = author.split('(')
                name = split[0].strip()
                born = None
                died = None
                
                if len(split) >1:
                    
                    years = match_year.findall(split[1])
                    
                    if not years:
                        continue
                    born = years[0]
                    
                    if len(years) > 1:
                        died = years[1]
                data['composers'].append({'name': name, 'born': born, 'died': died})
                
                
        elif value1 == 'voice':
             data['voice'] = value2 if value2 else None  
        elif value1 == 'partiture':
            data['partiture'] = value2.lower() == 'yes'           
        elif value1 == 'title':
            data['title'] = value2 if value2 else None 
        elif value1 == 'genre':
            data['genre'] = value2 if value2 else None     
        elif value1 == 'key':
            data['key'] = value2 if value2 else None  
        elif value1 == 'composition year':
            data['year'] = value2 if value2 else None
        elif value1 == 'genre':
            data['genre'] = value2 if value2 else None
        elif value1 == 'incipit':
            data['incipit'] = value2 if value2 else None
        elif value1 == 'edition':
            data['edition'] = value2 if value2 else None
        elif value1 == 'editor':
            data['editor'] = value2 if value2 else None

    return prints

