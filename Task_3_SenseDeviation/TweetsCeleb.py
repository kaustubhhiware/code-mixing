import pandas as pd
import numpy as np
from nltk.corpus import wordnet as wn
import pickle

'''
	extract only the tweets, modifying En words in Hi context
'''
def tweetsExtract():
	print("+--- Starting names")
	nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
	print("+--- names done")

	r = pd.read_pickle('../Task_1_Formatting/Data/Celebrity_ALL.pkl')
	print("+--- pickle done of len", len(r))
	t=r[['Tweet','Tweet-tag','Word-level']]
	tweets,changed = [], []
	# t['Word-level'].iloc[0] # print 0th row in Word-level column
	# len(t) gives length
	for i in range(len(t)):
		print(i)
		l=t.iloc[i]['Word-level']
		tweet = ''
		# flag = False
		for j in range(len(l)):
			# only for nouns, add $ for En word in Hi context
			if( l.index[j] in nouns and
				l.iloc[j]['Label'] == 'EN' and l.iloc[j]['Matrix'] != 'EN'):
				# print(j, l.index[j])
				tweet += l.index[j]+'$ '
				# changed.append(l.index[j])
				# print(l.index[j])
				# flag=True
			elif l.iloc[j]['Label']!='OTHER':
				tweet += l.index[j] + ' '
		# if flag:
		# 	print(tweet)
		tweets.append(tweet)

	print("+--- processing done")
	px = pd.DataFrame(np.array(tweets).reshape(len(tweets),1), columns = ["word"])
	with open('tweets_follow.pkl', 'wb') as f:
		pickle.dump(px, f)

if __name__ == '__main__':
	tweetsExtract()