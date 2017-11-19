#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
import pandas as pd
import preprocessor as p
import re
import enchant
import nltk
import ordereddict
#nltk.download()
from nltk.corpus import brown
import sys
'''
Input file: input.txt containing Raw twitter data
Output: Text files named with user_id containing tweet set of user 

'''
def neg(b):
     if(b=='EN' or b=='NE'):
         return 'HI'
     elif(b=='HI'):
           return 'EN'

def classify(a):
        ''' Returns 1 if Code-Switching
            Returns >1 if Code-Mixing'''
        c=a[0]
        n=0
        for itm in a:
           if(itm==neg(c)):
                n=n+1
                c=neg(c)
        return n   

reload(sys)
sys.setdefaultencoding('utf-8')

dicth={}
dicte={}
tweets_data = []
SYMBOLS = '{}()[].,:;+-*/&|"!?%^<>₹=~\'$'#1234567890'
SYMBOLS1 = '{}()[].,:;+-*/&|"!?%^<>₹=~$1234567890'
tweets_file = open('input.txt', "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
p.set_options(p.OPT.URL, p.OPT.EMOJI,p.OPT.SMILEY)
nt=len(tweets_data)
index=range(0,nt)
columns = ['username','tweetid','id','isCeleb','Tweet','Tweet-tag', 'Word-level']
data=pd.DataFrame(index=index,columns=columns)

data["Tweet"]=map(lambda tweet: tweet['text'], tweets_data)
data["id"]=map(lambda tweet: tweet['user']['id'], tweets_data)
data["tweetid"]=map(lambda tweet: tweet['id'], tweets_data)
data["username"]=map(lambda tweet: tweet['user']['name'], tweets_data)
data=data.drop_duplicates('tweetid')

data=data.drop_duplicates('tweetid') 
L1=len(data['id'].unique())

dff={}
'''Splitting dataframe into multiple dataframes based on user_id '''
for (x,y) in zip(data['id'].unique(),range(0,L1)):
            dff[y]=data[data['id']==x]
            dff[y]= dff[y].set_index('tweetid')
            dff[y]= dff[y].reset_index()

d = enchant.Dict("en_US")

'''L1 is the number of dataframes each containing tweet set '''
for q in range(0,L1):
    for v in range(0,len(dff[q].index)):
       lis=[]
       lis1=[]
       hindi=[]
       english=[]
       other=[]
       wordlist=[]
       taglist=[]
       NER=[]
       cleantweet=  re.split('\s|(?<!\d)[,.](?!\d)',p.clean(dff[q]['Tweet'][v]))   
       
       '''Named Entities Extraction '''
       chunked=nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(p.clean(dff[q]['Tweet'][v]))))

       ners=[ " ".join(w for w, t in elt) for elt in chunked if isinstance(elt, nltk.Tree) ]
   
       for thing in ners:
             NER.extend(thing.split(" "))

       if(cleantweet[0]=='RT'):
          for item in cleantweet:
              if(str(item).startswith('@') and str(item).endswith(':')):
                    cleantweet.remove(item)
          dff[q]['isCeleb'][v]=1
          cleantweet.remove('RT')
       else:
          dff[q]['isCeleb'][v]=0

       cleantweet=list(filter(None, cleantweet))
       for item in cleantweet:
           if(item[0] in ['@','#']):
              item=item.strip(SYMBOLS) 
              lis1.append(item)
           else:
              item=item.strip(SYMBOLS1) 
              lis1.append(item)
       lis1=list(filter(None, lis1))

       '''For removing duplicates(since set function removes duplicates randomly) '''
       for i in lis1:
          if i not in lis:
             lis.append(i)
       
       '''For number Filtering '''
       lis = filter(lambda i: not str.isdigit(i.encode('utf-8')), lis)
       wordlist=lis1 #lis

       '''Word Tagging based on Language. 
          dicte and dicth are local english and hindi dictionaries '''
       for f in lis:
           if((f in (dicte,brown.words()))or d.check(f)):
                   english.append(f)
                   if(f in NER):
                       dicte[f]='NE'
                   else:
                      dicte[f]='EN'
           else:
             if((f[0]not in ['@','#']) or (f in dicth)):
               hindi.append(f)
               if(f in NER):
                     dicth[f]='NE'
               else:
                  dicth[f]='HI'
             else:
               other.append(f)
      
       Neng=0
       Nhin=0
       for wrd in wordlist:
           if(wrd in english):
              taglist.append('EN')
              Neng=Neng+1
           elif((wrd in hindi) and (wrd not in NER)):
              taglist.append('HI')
              Nhin=Nhin+1
       
       if(Neng>0 or Nhin>0):
            percE=float(Neng)/(Neng+Nhin)
            percH=float(Nhin)/(Neng+Nhin)
 
       elif(Neng==0 and Nhin==0):
            percE=0
            percH=0

       '''Assigning Tweet-tag '''      
       if(percE>0.9):
               dff[q]["Tweet-tag"][v]='ENGLISH'
       elif(percH>0.9):
               dff[q]["Tweet-tag"][v]= 'HINDI'
       else:
         if(taglist):
            if(classify(taglist)==1):
                 dff[q]["Tweet-tag"][v]='CS' 
            elif(percE>0.55 and classify(taglist)>1):
                 dff[q]["Tweet-tag"][v]='CME'
            elif(percH>0.55 and classify(taglist)>1):
                 dff[q]["Tweet-tag"][v]= 'CMH'
            elif((percE<0.55 and percE>0.45)and(percH<0.55 and percH>0.45) and classify(taglist)>1):
                 dff[q]["Tweet-tag"][v]= 'CMEQ'
         else:
           dff[q]["Tweet-tag"][v]='OTHER'
   
       windex=lis
       wcolumns = ['Label','Matrix']
       worddata=pd.DataFrame(index=windex,columns=wcolumns)

       '''Assigning Labels and Matrix '''
       for fn in lis:
            if(fn in english):
                  worddata['Label'][fn]='EN'
            elif(fn in hindi):
                  worddata['Label'][fn]='HI'
            elif(fn in other):
                  worddata['Label'][fn]='OTHER'

       '''Named Entity Tagging'''
       for fn in lis:
             if(fn in NER):
                  worddata['Label'][fn]='NE'

       if(dff[q]["Tweet-tag"][v] in ['ENGLISH','CME']):
             for fn in lis:
                 worddata['Matrix'][fn]='EN'
       elif(dff[q]["Tweet-tag"][v] in ['HINDI','CMH']):
             for fn in lis:
                  worddata['Matrix'][fn]='HI'
       elif(dff[q]["Tweet-tag"][v] =='CMEQ'):
              for fn in lis:
                  worddata['Matrix'][fn]='O'
       elif(dff[q]["Tweet-tag"][v] in['CS','OTHER']):
                 for fn in lis:
                      worddata['Matrix'][fn]=worddata['Label'][fn]
       
       dff[q]["Word-level"][v]=worddata
    uid=dff[q]['id'][0] 
    json_format=(dff[q]).to_json(orient='index')
    jsn=json.dumps(json.loads(json_format,object_pairs_hook=ordereddict.OrderedDict),ensure_ascii=False, indent=4)
    fname=str(uid)+'.txt'
    fp=open(fname,'w')
    fp.write(jsn)
    fp.close()
   
