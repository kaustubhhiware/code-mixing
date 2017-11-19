import gensim
from nltk.corpus import wordnet as wn
nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
'''
	once the model is written, we want to check similarity between all words
'''

def similarity():
model = gensim.models.Word2Vec('complex-sm')
e = []  # English in Hindi context
score = [] 

for each in model.wv.vocab.keys():
	if each.endswith('$'):
		e.append(each)

for each in e:
	if each[:-1] in model.wv.vocab.keys():
		score.append([each[:-1], model.similarity(each[:-1], each) ] )
	else:
		score.append([each[:-1], -1 ] )

with open('dollar_scores.txt','w') as f:
	for each in score:
		f.write(each[0] + ' ' + str(each[1]) + '\n')


if __name__ == '__main__':
	similarity()