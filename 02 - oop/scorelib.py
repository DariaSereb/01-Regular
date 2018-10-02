class Print:
    def __init__(self,edition,print_id,pariture):
       self.edition = edition
       self.print_id = print_id
       self.pariture = pariture
     
          
    def format(self):
        print("Print Number: {}".format(self.print_id), )
         
    
    def composition(self):
         return self.edition.composition
        
class Edition:
    
     edition = []
     
    def __init__(self,composition,authors,name):
        self.composition = composition
        self.authors = authors
        self.name = name

        def authors_name(self, name):
        self.authors.append(Person(name))

class Composition:
    def __init__(self, name, incipit, key, genre, year, composer):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = []
        self.authors = []



class Voice
   def __init__(self,name,range):
       self.name = name
       self.range = range

class Person
   def __init__(self,name,born,died)
        self.name = name
        self.born = born
        self.died = died

if __name__ == "__main__":
    main()
