import pandas as pd
import pickle
import nltk
import gensim
import multiprocessing
from gensim import corpora, models, similarities
from gensim.models.keyedvectors import KeyedVectors

'''
	create w2v from sm dataset
'''

# useful indices with $ in them
# 141, 151, 337, 358, 395, 532, 624, 625, 770, 820, 956

# def w2v():
tc, tf = pd.read_pickle('tweets_celeb.pkl'), pd.read_pickle('tweets_follow.pkl')
t = pd.concat([tc,tf]) # merge all tweets
corpus = t['word'].values.tolist()

tok_corp = []
for i in range(len(corpus)):
	tok = nltk.word_tokenize(corpus[i])
	print(i)
	for i in range(len(tok)-1):
		if tok[i+1]=='$':
			tok[i] += '$'
	tok = [w for w in tok if w!='$']
	tok_corp.append(tok)

# tok_corp= [nltk.word_tokenize(tweet) for tweet in corpus]
# no need to decode utf-8, strings in python are unicode by default

model = gensim.models.word2vec.Word2Vec(tok_corp, size = 300,
								min_count = 1, window = 5,
								workers = multiprocessing.cpu_count() / 2)
'''
model = gensim.models.word2vec.Word2Vec(size = 300,
								min_count = 1, window = 5,
								workers = multiprocessing.cpu_count() / 2)
model.build_vocab(tok_corp)
  '''
 # Normalise data
model.delete_temporary_training_data(replace_word_vectors_with_normalized=True) 
# refer: https://rare-technologies.com/word2vec-tutorial/
# min_count => word must appear atleast these much times to be considered
# size => No. of NN layers, dimensions
# workers => parallelization, multiprocessing.cpu_count()
# window => context_size
# Distance, similarity, ranking
# model = gensim.models.Word2Vec.load('testmodel')
model.save('complex-sm')

# see which words end in $, their similarity
# len(m.wv.vocab)
for each in model.wv.vocab.keys():
    if each.endswith('$'):
        print(each)


# if __name__ == '__main__':
# 	w2v()