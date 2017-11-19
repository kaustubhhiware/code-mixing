#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
import pandas as pd
import preprocessor as p
import re
import nltk
import pickle
p.set_options(p.OPT.URL, p.OPT.EMOJI,p.OPT.SMILEY)
dff={}
def neg(b):
     if(b=='EN'):
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

i=1
columns = ['tweetid','isCeleb','Tweet','Tweet-tag', 'Word-level']
data=pd.DataFrame(columns=columns)
SYMBOLS = '{}()[].,:;+-*/&|"!?%^<>₹=~\'$'#1234567890'
with open('t3') as fh:
  for line1 in fh:
    line2 = next(fh)
    celb=0
    #print(line1)
    #print(line2)
    lis1=[]
    NER=[]
    data1=pd.DataFrame(index=range(0,1),columns=columns)
    line1s=line1.split(",", 1)
    line1ss=line1s[0].split("\t", 1)
    #print(line1ss)
    #print(line1s)
    lis=re.split('\s|[/]',line2)
    #print(lis)
    if(len(line1s)>1 and len(line1ss)>1):
     data1.ix[0,'tweetid']=line1ss[1]
     data1.ix[0,'Tweet']=re.sub(r'^\"\n|\"|\n$', '', line1s[1])
     chunked=nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(p.clean(line1s[1]))))
     ners=[ " ".join(w for w, t in elt) for elt in chunked if isinstance(elt, nltk.Tree) ]
     for thing in ners:
             NER.extend(thing.split(" "))
     #print(data1)
    #print(NER)
    if('https' in lis):
     ind=lis.index('https')
     lis=lis[:ind]
    lis=list(filter(None, lis))
    for item in lis:
              item=item.strip(SYMBOLS)
              lis1.append(item) 
    lis=lis1
    j=0
    while(j<len(lis)-1):
          if(lis[j]==''):
               lis[j+1]=''
               j=j+1
          j=j+1
    j=0
    while(j<len(lis)-4):
          if(lis[j]=='RT'):
               celb=1
               lis[j+1]=''
               lis[j+2]=''
               lis[j+3]=''
               lis[j]=''
          j=j+1
    data1.ix[0,'isCeleb']=celb
    lis=list(filter(None, lis))
    Neng=0
    Nhin=0      
    #print(lis)
    if(len(lis)>4):
     n=int((len(lis)-3)/2)
     wcolumns = ['word','Label','Matrix']
     worddata=pd.DataFrame(index=range(0,n),columns=wcolumns)
     wr=0
     taglist=[]
     words=[]
     for ii in range(3,len(lis)-1,2):
             worddata.loc[wr,'word']=lis[ii]
             words.append(lis[ii])
             worddata.loc[wr,'Label']=lis[ii+1]
             if(lis[ii+1] =='EN'):
                   Neng+=1
                   taglist.append(lis[ii+1])
             elif(lis[ii+1] =='HI'):
                   Nhin+=1
                   taglist.append(lis[ii+1])
             wr+=1
     #print(taglist)
     worddata=worddata.set_index('word')
     if(Neng>0 or Nhin>0):
            percE=float(Neng)/(Neng+Nhin)
            percH=float(Nhin)/(Neng+Nhin)
 
     elif(Neng==0 and Nhin==0):
            percE=0
            percH=0

     if(percE>0.9):
               data1.ix[0,"Tweet-tag"]='ENGLISH'
     elif(percH>0.9):
               data1.ix[0,"Tweet-tag"]= 'HINDI'
     else:
         if(taglist):
            if(classify(taglist)==1):
                 data1.ix[0,"Tweet-tag"]='CS' 
            elif(percE>0.55 and classify(taglist)>1):
                 data1.ix[0,"Tweet-tag"]='CME'
            elif(percH>0.55 and classify(taglist)>1):
                 data1.ix[0,"Tweet-tag"]= 'CMH'
            elif((percE<0.55 and percE>0.45)and(percH<0.55 and percH>0.45) and classify(taglist)>1):
                 data1.ix[0,"Tweet-tag"]= 'CMEQ'
         else:
           data1.ix[0,"Tweet-tag"]='OTHER'
     #print(data1["Tweet-tag"][0])
     if(data1.ix[0,"Tweet-tag"] in ['ENGLISH','CME']):
             for fn in words:
                 worddata.loc[fn,'Matrix']='EN'
     elif(data1.ix[0,"Tweet-tag"] in ['HINDI','CMH']):
             for fn in words:
                  worddata.loc[fn,'Matrix']='HI'
     elif(data1.ix[0,"Tweet-tag"] =='CMEQ'):
              for fn in words:
                  worddata.loc[fn,'Matrix']='O'
     elif(data1.ix[0,"Tweet-tag"] in['CS','OTHER']):
                 for fn in words:
                      worddata.loc[fn,'Matrix']=worddata.loc[fn,'Label']
     for t in words:
          if(t in NER):
              worddata.loc[t,'Label']='NE'
     data1["Word-level"][0]=worddata
     #print(data1) 
     data=data.append(data1,ignore_index=True)
     #print(taglist)
    i+=1
    print(i)
    #if(i>1500):
       #break

for x in range(0,2):
            dff[x]=data[data['isCeleb']==x]
            dff[x]= dff[x].set_index('tweetid')
            dff[x]= dff[x].reset_index()
dff[0]=dff[0].drop_duplicates('tweetid') 
dff[0].to_pickle('NonCelebAll3.pkl')
dff[1]=dff[1].drop_duplicates('tweetid') 
dff[1].to_pickle('CelebAll3.pkl')
