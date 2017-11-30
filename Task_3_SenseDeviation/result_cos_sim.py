# -*- coding: utf-8 -*- 
from scipy.spatial.distance import cosine
import numpy as np
from gensim import models
import pickle
import operator

'''
	Get cosine similarity between film$ in sm, and film in En
	Store in a file in ascending order of cosine similarity
'''
print( "loading English word2vec")
e_wv = models.KeyedVectors.load_word2vec_format('G.bin', binary=True)

print( "loading SM word2vec")
sm_wv = models.Word2Vec.load("complex-sm")

# ----------------------------------------------------------------------

print( "loading target data")
pkl_file = open('Manual_Tagging/SM2HIdict-test.pkl', 'rb')
word_dict = pickle.load(pkl_file)
pkl_file.close()

# ----------------------------------------------------------------------

print("loading En transformation matrix")
pkl_file1 = open('W-EN-train.pkl', 'rb')
W_en = pickle.load(pkl_file1)
pkl_file1.close()

print("loading SM transformation matrix")
pkl_file2 = open('W-SM-train.pkl', 'rb')
W_sm = pickle.load(pkl_file2)
pkl_file2.close()

# ----------------------------------------------------------------------

cos_sim = {}
for each in word_dict:
	transformed_en = np.dot(W_en, e_wv.wv[each]).tolist()
	transformed_sm = np.dot(W_sm, sm_wv.wv[each+'$']).tolist()
	transformed_en /= np.linalg.norm(transformed_en)
	transformed_sm /= np.linalg.norm(transformed_sm)
	similarity = 1 - cosine(transformed_en, transformed_sm)
	cos_sim[each] = similarity

ascending = sorted(cos_sim.items(), key=operator.itemgetter(1))
with open('result3-cos-similarity.txt', 'w') as f:
	for word, score in ascending:
		f.write(word + ' ' + str(score) + '\n')
