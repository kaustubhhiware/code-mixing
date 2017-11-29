import pandas as pd
import numpy as np
import pickle
from nltk.corpus import wordnet as wn
import sys
import operator
'''
	get count of times english noun used in hindi and english context
'''

# tweets
# celeb: 770234
# follow: 1367490
r = pd.read_pickle('../Task_1_Formatting/Data/Celebrity_ALL.pkl')
print("+++--- pickle done of len", len(r))
t=r[['Tweet','Tweet-tag','Word-level']]
english = {}
f_e = {} # frequency counts
f_h = {}
nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
for i in range(len(t)):
	print(i) # Each tweet
	l = t.iloc[i]['Word-level']
	for j in range(len(l)):
		word = l.index[j] # Each word of tweet
		if( l.iloc[j]['Label'] == 'EN' and word in nouns):
			if word not in english:
				english[word] = word
				f_e[word] = 0
				f_h[word] = 0
				# print('added '+word+', now at '+str(len(english)))
			if (l.iloc[j]['Matrix'] == 'EN'):
				f_e[word] += 1
			elif (l.iloc[j]['Matrix'] == 'HI'):
				f_h[word] += 1
print("+++--- Processing done for Celebrity_ALL")

t1 = t
r = pd.read_pickle('../Task_1_Formatting/Data/NonCelebrity_ALL.pkl')
print("+++--- pickle done of len", len(r))
t=r[['Tweet','Tweet-tag','Word-level']]
for i in range(len(t)):
	print(i) # Each tweet
	l = t.iloc[i]['Word-level']
	for j in range(len(l)):
		word = l.index[j] # Each word of tweet
		if( l.iloc[j]['Label'] == 'EN' and word in nouns):
			if word not in english:
				english[word] = word
				f_e[word] = 0
				f_h[word] = 0
				# print('added '+word+', now at '+str(len(english)))
			if (l.iloc[j]['Matrix'] == 'EN'):
				f_e[word] += 1
			elif (l.iloc[j]['Matrix'] == 'HI'):
				f_h[word] += 1
print("+++--- Processing done for Follower_All")


ratio = {}
min_ratio = np.log(0.5 / max(f_h))
for each in english:
	if f_h[each] is 0 or f_e[each] is 0:
		continue
	# invalid 2 cases
	if f_h[each] is 0:
		ratio[each] = 50 # np.log(sys.maxsize) = 43.668272375276551
	elif f_e[each] is 0:
		ratio[each] = min_ratio
	else:
		ratio[each] = np.log(1.0 * f_e[each] / f_h [each])

# save in pandas dataframe
descending = sorted(ratio.items(), key=operator.itemgetter(1), reverse=True)
print('+++--- Sorting and saving to pandas')
l = []
for i in range(len(descending)):
	word = descending[i][0]
	l.append([word, f_e[word], f_h[word], ratio[word]])

d = pd.DataFrame(data = l, columns= ['word','f_e','f_h','ratio'])
d.to_pickle('frequency-count.pkl')

with open('frequency-count.txt','w') as f:
	for each in l:
		f.write(str(each) + '\n')

f.close()