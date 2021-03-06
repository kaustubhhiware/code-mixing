# -*- coding: utf-8 -*- 
from scipy.spatial.distance import cosine
import numpy as np
from gensim import models
import unicodecsv as csv
import pickle

print( "loading English word2vec")
e_wv = models.KeyedVectors.load_word2vec_format('G.bin', binary=True)

print( "loading SM word2vec")
sm_wv = models.Word2Vec.load("complex-sm")

print( "loading Hindi word2vec")
h_wv = models.Word2Vec.load("hi.bin")

print( "loading translation data")
pkl_file = open('Manual_Tagging/SM2HIdict-test.pkl', 'rb')
word_dict = pickle.load(pkl_file)
pkl_file.close()

print("loading En transformation matrix")
pkl_file1 = open('W-EN-train.pkl', 'rb')
W_en = pickle.load(pkl_file1)
pkl_file1.close()

print("loading SM transformation matrix")
pkl_file2 = open('W-SM-train.pkl', 'rb')
W_sm = pickle.load(pkl_file2)
pkl_file2.close()

cos_diff = {}
print("worddict is of len",len(word_dict))
count = 0
x = 0
y = 0
for k, v in word_dict.items():
    # if k[-1] == '$':
    #     k_trans_en = np.dot(W_en, e_wv.wv[k[:-1]]).tolist()
    #     k_trans_sm = np.dot( W_sm, sm_wv.wv[k]).tolist()
    #     row = [k[:-1], k]
    #     cos_diff[k[:-1]] = []
    # else:
    #     k_trans_en = np.dot(W_en, e_wv.wv[k]).tolist()
    #     k_trans_sm = np.dot( W_sm, sm_wv.wv[k+'$']).tolist()
    #     row = [k, k+'$']
    #     cos_diff[k] = []
    try:
        e_wv.wv[k]
        sm_wv.wv[k+'$']
    except:
        x += 1
        # print(k, "is not available")
        continue
    k_trans_en = np.dot(W_en, e_wv.wv[k]).tolist()
    k_trans_sm = np.dot( W_sm, sm_wv.wv[k+'$']).tolist()
    row = [k, k+'$']
    cos_diff[k] = []
    for val in v:
        # print(val)
        # print(h_wv.wv[val])
        try:
            v_ = h_wv.wv[val]
        except:
            y += 1
            continue
        # v_wv = h_wv.wv[val]
        # Cosine similarity, store in file
        cos_en = 1 - cosine(h_wv.wv[val].tolist(), k_trans_en)
        cos_sm = 1 - cosine(h_wv.wv[val].tolist(), k_trans_sm)
        diff = cosine(h_wv.wv[val].tolist(), k_trans_sm) - cosine(h_wv.wv[val].tolist(), k_trans_en)
        # diff = h_wv.wv.similarity(val, [k_trans_en]) - h_wv.wv.similarity(val, [k_trans_sm])
        cos_diff[k].append((val, diff))
        count += 1
        row.append([val, str(cos_en), str(cos_sm), str(diff)])
    print(row)