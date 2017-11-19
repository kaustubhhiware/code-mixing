import pandas as pd
import numpy as np
import pickle
from nltk.corpus import wordnet as wn

'''
	extract only the english nouns
'''

# tweets
# celeb: 770234
# follow: 1367490
# def engNouns():
r = pd.read_pickle('../Task_1_Formatting/Data/Celebrity_ALL.pkl')
print("+++--- pickle done of len", len(r))
t=r[['Tweet','Tweet-tag','Word-level']]
english = []
for i in range(len(t)):
	print(i)
	l=t.iloc[i]['Word-level']
	for j in range(len(l)):
		if( l.iloc[j]['Label'] == 'EN'):
			english.append(l.index[j])

	print("+++--- Processing done")
	# refer to this for npz
	# https://stackoverflow.com/questions/22941147/fastest-file-format-for-read-write-operations-with-pandas-and-or-numpy
	eng = []
	nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
	for each in english:
		if each in nouns:
			eng.append(each)

engs = list(set(eng)) # remove duplicates
with open('eng-nouns-celeb.txt','w') as f:
	for i in engs:
		f.write(i + '\n')
f.close()