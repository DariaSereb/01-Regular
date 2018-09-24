
import re
import string
import sys

if sys.argv[0] == "composer":
    frequency = {}
    document_text = open('scorelib.txt',encoding="utf8")
    text_string = document_text.read()

    match_pattern = re.findall(r'(?<=Composer: )(\S*..\S*..[a-z]+|\S*..\S*|\b)', text_string)
    match_pattern2 = re.findall(r'(?<=; )([a-z]*\w{4,15}..[a-z]*..[a-z]*..[a-z]+|[a-z]*\w{4,15}..[a-z]*..[a-z]*)', text_string)
    match_pattern2. remove('Courante nova; Courante')
    match_pattern2. remove('Oeuvre III')
    match_pattern2. remove('Gavotte ')
    match_pattern2. remove('Rigadoon; Iers lied')
    match_pattern2. remove('Saltarello ')
    match_pattern2. remove('Chaconne ')
    match_pattern2. remove('Molto Allegro')
    match_pattern. remove('Petzold, Chr; Anonymous')
    match_pattern.append('Petzold')

   for word in match_pattern:
    count = frequency.get(word,0)
    frequency[word] = count + 1

   for word in match_pattern2:
    count = frequency.get(word,0)
    frequency[word] = count + 1
     
   frequency_list = frequency.keys()
    
   for words in frequency_list:
    
        print (words,':',frequency[words])

elif sys.argv[0] == "century":

    frequency = {}
    document_text = open('scorelib.txt',encoding="utf8")
    text_string = document_text.read()
    match_pattern = re.findall(r'(?<=Composition Year: 15\d{2})', text_string)

    for word in match_pattern:
      count = frequency.get(word,0)
      frequency[word] = count + 1

 
      frequency_list = frequency.keys()
    
    for words in frequency_list:
   
       print ('16th century:',frequency[words])

       frequency.clear()

    match_pattern = re.findall(r'(?<=Composition Year: 16\d{2})', text_string)
    match_pattern2 = re.findall(r'(?<=Composition Year: 17th)', text_string)

    for word in match_pattern:
       count = frequency.get(word,0)
       frequency[word] = count + 1
    for word in match_pattern2:
       count = frequency.get(word,0)
       frequency[word] = count + 1

 
    frequency_list = frequency.keys()
    
    for words in frequency_list:
   
       print ('17th century:',frequency[words])
     
    frequency.clear()

    match_pattern = re.findall(r'(?<=Composition Year: 17\d{2})', text_string)
    match_pattern2 = re.findall(r'(?<=Composition Year: 18th)', text_string)

    for word in match_pattern:
       count = frequency.get(word,0)
       frequency[word] = count + 1
    for word in match_pattern2:
       count = frequency.get(word,0)
       frequency[word] = count + 1

 
    frequency_list = frequency.keys()
    
    for words in frequency_list:
   
       print ('18th century:',frequency[words])

    frequency.clear()

elif sys.argv[0] == "key_of_c_minor":
    match_pattern = re.findall(r'Key: c', text_string)


    for word in match_pattern:
       count = frequency.get(word,0)
       frequency[word] = count + 1


 
   frequency_list = frequency.keys()
    
   for words in frequency_list:
   
       print ('Key c:',frequency[words])

   frequency.clear()
