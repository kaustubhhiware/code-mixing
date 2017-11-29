#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
import pandas as pd
import preprocessor as p
import importlib
import re
import nltk
#nltk.download()
from collections import OrderedDict
import enchant
from nltk.corpus import brown
import sys
'''
Input file: Status.txt containing Raw twitter data
Output: Two text files containing tweet set of celebrities and non-celebrities 

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

#importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

dicth={}
dicte={}
SYMBOLS = '{}()[].,:;+-*/&|"!?%^<>₹=…~\'$'#1234567890'
SYMBOLS1 = '{}()[].,:;+-*/&|"!?%^<>₹=…~\'$1234567890'
tweets_file = open('Status.txt', "r")
i=0
k=1
#print(tweets_data)
p.set_options(p.OPT.URL, p.OPT.EMOJI,p.OPT.SMILEY)
#nt=len(tweets_data)
#index=range(0,nt)
columns = ['username','tweetid','id','isCeleb','Tweet','Tweet-tag', 'Word-level']
data1=pd.DataFrame(columns=columns)	
#print(data)
#print(data)
#print(data)
dff={}
print('hello')
d = enchant.Dict("en_US")
#data=data.set_index('tweetid')
#data=data.reset_index()
#LL=len(data.index)

for line in tweets_file:
    #tweets_data = []
 # if not line.strip():  
    try:
       data=pd.DataFrame(index=range(0,1),columns=columns) 
       #data=data.dropna()
       tweet = json.loads(line)
       #tweets_data.append(tweet)
       print(k)
       k=k+1
       #print(data.index.values)
       data.ix[0,"Tweet"]=tweet['text']
       #print(data['Tweet'])
       data.ix[0,"id"]=tweet['user']['id']
       data.ix[0,"tweetid"]=tweet['id']
       data.ix[0,"username"]=tweet['user']['name']
       #print(data['username'])
#for v in range(0,LL):
       lis=[]
       lis1=[]
       hindi=[]
       english=[]
       other=[]
       wordlist=[]
       taglist=[]
       NER=[]
       cleantweet= re.split('\s|(?<!\d)[,.](?!\d)|[/,…]',p.clean(str(tweet['text'])))   
       '''Named Entities Extraction '''
       chunked=nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(p.clean(str(tweet['text'])))))

       ners=[ " ".join(w for w, t in elt) for elt in chunked if isinstance(elt, nltk.Tree) ]
       #print(cleantweet)
       for thing in ners:
             NER.extend(thing.split(" "))
       #print(NER)
       if(cleantweet[0]=='RT' or cleantweet[1]=='RT'):
          for item in cleantweet:
              if(str(item).startswith('@') and str(item).endswith(':')):
                    cleantweet.remove(item)
          data['isCeleb']=1
          cleantweet.remove('RT')
       else:
          data['isCeleb']=0

       cleantweet=list(filter(None, cleantweet))
       #print(cleantweet)

       for item in cleantweet:
           if(item[0] in ['@','#']):
              item=item.strip(SYMBOLS) 
              lis1.append(item)
           else:
              item=item.strip(SYMBOLS1) 
              lis1.append(item)
       lis1=list(filter(None, lis1))
       #print(lis1)
       '''For removing duplicates(since set function removes duplicates randomly) '''
       for i in lis1:
          if i not in lis:
             lis.append(i)
       
       '''For number Filtering '''
       lis = list(filter(lambda i: not str.isdigit(str(i.encode('utf-8'))), lis))
       wordlist=lis1 #lis
       #print(lis)
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

       #print(data["Tweet-tag"])
       
       '''Assigning Tweet-tag '''      
       if(percE>0.9):
               data.ix[0,"Tweet-tag"]='ENGLISH'
               #data.iloc[0,"Tweet-tag"]= data.loc[0,"Tweet-tag"].values[0]
       elif(percH>0.9):
               data.ix[0,"Tweet-tag"]='HINDI'
               #data.iloc[0,"Tweet-tag"]= data.loc[0,"Tweet-tag"].values[0]
              
       else:
         if(taglist):
            if(classify(taglist)==1):
                 data.ix[0,"Tweet-tag"]='CS'
            elif(percE>0.55 and classify(taglist)>1):
                 data.ix[0,"Tweet-tag"]='CME'
            elif(percH>0.55 and classify(taglist)>1):
                 data.ix[0,"Tweet-tag"]= 'CMH'
            elif((percE<0.55 and percE>0.45)and(percH<0.55 and percH>0.45) and classify(taglist)>1):
                 data.ix[0,"Tweet-tag"]='CMEQ'
                 #data.loc[0,"Tweet-tag"]= data.loc[0,"Tweet-tag"].values[0]
         else:
           data.ix[0,"Tweet-tag"]='OTHER'
       #print(data["Tweet-tag"])
       windex=lis
       #print(windex)
       wcolumns = ['Label','Matrix']
       worddata=pd.DataFrame(index=windex,columns=wcolumns)
       #print(worddata)
       
       '''Assigning Labels and Matrix '''
       for fn in lis:
            if(fn in english):
                  worddata.loc[fn,'Label']='EN'
            elif(fn in hindi):
                  worddata.loc[fn,'Label']='HI'
            elif(fn in other):
                  worddata.loc[fn,'Label']='OTHER'

       '''Named Entity Tagging'''
       for fn in lis:
             if(fn in NER):
                  worddata.loc[fn,'Label']='NE' 

       #print(data["Tweet-tag"].values[0])
       if(data["Tweet-tag"].values[0] in ['ENGLISH','CME']):
             for fn in lis:
                 worddata.loc[fn,'Matrix']='EN'
       elif(data["Tweet-tag"].values[0] in ['HINDI','CMH']):
             for fn in lis:
                  worddata.loc[fn,'Matrix']='HI'
       elif(data["Tweet-tag"].values[0] =='CMEQ'):
              for fn in lis:
                  worddata.loc[fn,'Matrix']='O'
       elif(data["Tweet-tag"].values[0] in['CS','OTHER']):
                 for fn in lis:
                      worddata.loc[fn,'Matrix']=worddata.loc[fn,'Label']

       #print(worddata)
       data["Word-level"][0]=worddata
       #print(data)
       #print('dddddd')
       data1=data1.append(data,ignore_index=True)
       #print(data1)
    except:
       continue

#print(data1)       
data1=data1.drop_duplicates('tweetid') 

for x in range(0,2):
            dff[x]=data1[data1['isCeleb']==x]
            dff[x]= dff[x].set_index('tweetid')
            dff[x]= dff[x].reset_index()
'''Converting dataframe to json format '''
fname1='NonCelebrity2.txt'
fname2='Celebrity2.txt'
json_format1=(dff[0]).to_json(orient='index')
jsn1=json.dumps(json.loads(json_format1,object_pairs_hook=OrderedDict),ensure_ascii=False, indent=4)
fp1=open(fname1,'w')
fp1.write(jsn1)
fp1.close()

json_format2=(dff[1]).to_json(orient='index')
jsn2=json.dumps(json.loads(json_format2,object_pairs_hook=OrderedDict),ensure_ascii=False, indent=4)
fp2=open(fname2,'w')
fp2.write(jsn2)
fp2.close()
