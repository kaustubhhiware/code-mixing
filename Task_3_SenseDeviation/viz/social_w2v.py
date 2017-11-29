import pandas as pd
import pickle
import nltk
import gensim
import multiprocessing
from gensim import corpora, models, similarities
from gensim.models.keyedvectors import KeyedVectors

import sys
import json
from pprint import pprint
import nltk
import numpy as np
import pandas
import functools
import json
from operator import itemgetter
import operator
from scipy.stats import spearmanr 
from scipy.stats import pearsonr
import _pickle as pickle
sys.path.append("/usr/local/lib/python3.5/site-packages")
import pandas.core.indexes 
sys.modules['pandas.indexes'] = pandas.core.indexes
import pandas.core.base, pandas.core.indexes.frozen
setattr(sys.modules['pandas.core.base'],'FrozenNDArray', pandas.core.indexes.frozen.FrozenNDArray)
import csv 
from sklearn.manifold import TSNE
import re
import matplotlib
import matplotlib.pyplot as plt
import time
import codecs
import matplotlib.font_manager as fm




'''
	create w2v from sm dataset
'''

model = gensim.models.word2vec.Word2Vec.load('complex-sm')
'''model = gensim.models.word2vec.Word2Vec(size = 300,
								min_count = 1, window = 5,
								workers = multiprocessing.cpu_count() / 2)
model.build_vocab(tok_corp)
model.train(tok_corp)'''
# refer: https://rare-technologies.com/word2vec-tutorial/
# min_count => word must appear atleast these much times to be considered
# size => No. of NN layers, dimensions
# workers => parallelization, multiprocessing.cpu_count()
# window => context_size
# Distance, similarity, ranking
# model = gensim.models.Word



orig_stdout = sys.stdout
f = open('complex-sm-points.txt', 'w')
sys.stdout = f



vocab = list(model.wv.vocab)
X = model[vocab]



#print(len(vocab))
#print(type(X))
tsne = TSNE(n_components=2,random_state=0)
X_tsne = tsne.fit_transform(X)



fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.scatter(X_tsne[:,0], X_tsne[:,1])

for i in range(0,X_tsne.shape[0]):
	ax.annotate(vocab[i],(X_tsne[i][0],X_tsne[i][1] ))
	print(vocab[i],end=' ')
	print(X_tsne[i][0],end=' ')
	print(X_tsne[i][1])


plt.savefig('complex-sm.png',bbox_inches='tight')
plt.show()
