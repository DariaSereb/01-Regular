import sys
import scorelib
import re

def get_data():
    data = {'composers': [], 'voices': []}
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
            
            for voice in data.get('voices', []):
                voice_lib.append(scorelib.Voice(voice['name'], voice['range']))
                
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

        elif value1 == 'composer':
            authors = value2.split(';')
            
            for author in authors:
                split = author.split('(')
                name = split[0].strip()
                born = None
                died = None
                
                if len(split) > 1:
                    years = match_year.findall(split[1])
                    
                    if not years:
                        continue
                    born = years[0]
                    
                    if len(years) > 1:
                        died = years[1]
                data['composers'].append({'name': name, 'born': born, 'died': died})
                
                
        elif 'voice' in value1:
            
            voice_n = None
            voice_number = None

            if '--' in value2:
                v_split = value2.split(',', 1)
                count_voice = match_voice.match(v_split[0])
                if not count_voice:
                    voice_number = None
                else:
                    voice_number = '{}--{}'.format(
                        count_voice.group(1), count_voice.group(2)
                    )
                voice_n = v_split[1].strip() if len(v_split) > 1 else None
                
            elif value2:
                voice_n = value2.strip()
            data['voices'].append({'name': voice_n, 'range': voice_number})

            
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


if __name__ == "__main__":
    args = sys.argv
    filepath = args[1]
    
    prints = load(filepath)
    print(len(prints))
    
    prints_str = [print_.format() for print_ in prints]
    print("\n\n".join(prints_str))
