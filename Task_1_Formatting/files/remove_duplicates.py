#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
import pandas as pd
#from collections import OrderedDict
import pickle
#import os.path
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
columns = ['tweetid','isCeleb','Tweet','Tweet-tag', 'Word-level']
dff={}
k=0
data1=pd.DataFrame(columns=columns) 
fname='final.pkl'
fn0= 'nonCelebrity_ALL.pkl' 
fn1='Celebrity_ALL.pkl'


k=0
for nm in range(0,6):  
       fname='CelebAll'+str(nm)+'.pkl'   
       data = pd.read_pickle(fname)
       data1=data1.append(data,ignore_index=True)
       print(k)
       k=k+1
data1=data1.drop_duplicates('tweetid')

print(data1.shape)
data1.to_pickle('Celebrity_ALL.pkl') 
