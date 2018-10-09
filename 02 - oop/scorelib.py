
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
    
    def voice_lines(self, voices):
        parts = []
        for number, voice in enumerate(voices, 1):
            range_ = voice.range
            name = voice.name
            vals = []
            if range_:
                vals.append(range_)
            if name:
                vals.append(name)
            comp = 'Voice {number}: '.format(number=number) + ', '.join(vals)
            parts.append(comp)
        return parts

   

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
            'voices': '\n'.join(self.voice_lines(self.composition().voices)),
            'partiture': 'Partiture: %s'%format('yes' if self.partiture == True else 'no'),
            'incipit': 'Incipit: %s'%format(self.composition().incipit or ''),}
        return '\n'.join(lines.values())



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



