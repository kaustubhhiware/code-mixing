# -*- coding: utf-8 -*-
from nltk.corpus import wordnet
from translation import bing
import nltk
#nltk.download()
import pickle
from googletrans import Translator
translator = Translator()

dicta={}

N=0
pkl_file = open('wordlist.pkl', 'rb')
mylis = pickle.load(pkl_file)
pkl_file.close()


fl1 = open('EN2HIdict.pkl', 'wb')
pickle.dump(dicta, fl1)
fl1.close()

for word in mylis:
    print(N)
    N+=1
    #line=lin.strip()
    print(word)
    synonyms = []
    antonyms = []
    s2=[]
    tran=[]
    for syn in wordnet.synsets(word):
      for l in syn.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())
    s1=list(set(synonyms))

###### To translate the words into hindi
    translations = translator.translate(s1, dest='hi')
    for translation in translations:
      t1=(translation.text)#.encode('utf-8')
      if(t1 not in s1):
         tran.append(t1)

    tran=list(set(tran))
    for i in tran:
       print(i)
    #dicta[word]=tran
    pkl_file1 = open('EN2HIdict.pkl', 'rb')
    mydict2 = pickle.load(pkl_file1)
    pkl_file1.close()
    mydict2[word]=tran
    output = open('EN2HIdict.pkl', 'wb')
    pickle.dump(mydict2, output)
    output.close()

