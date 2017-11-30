# -*- coding: utf-8 -*- 
import numpy as np
from gensim import models
import pickle

'''
	Get neighbors film$ in sm, and film in En
	Save that in a file also
'''
print( "loading English word2vec")
e_wv = models.KeyedVectors.load_word2vec_format('G.bin', binary=True)

print( "loading SM word2vec")
sm_wv = models.Word2Vec.load("complex-sm")

print( "loading Hindi word2vec")
h_wv = models.Word2Vec.load("hi.bin")

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
words,en_sim,sm_sim = '','',''
f = open('result2-neighbors.txt','w')
for each in word_dict:
	transformed_en = np.dot(W_en, e_wv.wv[each])
	transformed_sm = np.dot(W_sm, sm_wv.wv[each+'$'])
	transformed_en /= np.linalg.norm(transformed_en)
	transformed_sm /= np.linalg.norm(transformed_sm)
	en_similar = h_wv.most_similar([transformed_en])
	sm_similar = h_wv.most_similar([transformed_sm])
	words += each + '\n\n\n\n\n\n\n\n\n\n\n'
	for each in en_similar:
		en_sim += str(each) + '\n'
	en_sim += '\n'
	for each in sm_similar:
		sm_sim += str(each) + '\n'
	sm_sim += '\n'

f.write('Words\n' + words + '\n\n\nEnglish\n' + en_sim + '\n\n\nSm\n' + sm_sim + '\n')
f.close()