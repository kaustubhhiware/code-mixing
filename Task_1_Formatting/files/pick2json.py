#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
import pandas as pd
from collections import OrderedDict
import pickle
import os.path
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
columns = ['tweetid','isCeleb','Tweet','Tweet-tag', 'Word-level']
data1=pd.DataFrame(columns=columns)
dff={}
k=0
data = pd.read_pickle('Celebrity_ALL.pkl')
data1=data1.append(data,ignore_index=True)
print(data1.shape)
json_format1=(data1).to_json(orient='index')
jsn1=json.dumps(json.loads(json_format1,object_pairs_hook=OrderedDict),ensure_ascii=False, indent=4)
fp1=open('Celebrity_ALL.txt','w')
fp1.write(jsn1)
fp1.close()