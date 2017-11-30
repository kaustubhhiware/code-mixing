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
word_dict_sm = pickle.load(pkl_file)
pkl_file.close()

print( "loading translation data")
pkl_file3 = open('EN2HIdict.pkl', 'rb')
word_dict_en = pickle.load(pkl_file3)
pkl_file3.close()

print("loading En transformation matrix")
pkl_file1 = open('W-EN-train.pkl', 'rb')
W_en = pickle.load(pkl_file1)
pkl_file1.close()

print("loading SM transformation matrix")
pkl_file2 = open('W-SM-train.pkl', 'rb')
W_sm = pickle.load(pkl_file2)
pkl_file2.close()

# f = open("res1.csv",'a')
# writer = csv.writer(f,delimiter=',',quoting=csv.QUOTE_NONE, escapechar='\\')
cos_diff = {}

for k, v in word_dict_sm.items():
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
        continue

    k_trans_en = np.dot(W_en, e_wv.wv[k]).tolist()
    k_trans_sm = np.dot( W_sm, sm_wv.wv[k+'$']).tolist()
    row = [k, k+'$']
    cos_diff[k] = []

    for val in word_dict_en[k]:
        try:
            v_ = h_wv.wv[val]
        except:
            continue
        # v_wv = h_wv.wv[val]
        # Cosine similarity, store in file
        cos_en = 1 - cosine(h_wv.wv[val].tolist(), k_trans_en)
        cos_sm = 1 - cosine(h_wv.wv[val].tolist(), k_trans_sm)
        diff = cosine(h_wv.wv[val].tolist(), k_trans_sm) - cosine(h_wv.wv[val].tolist(), k_trans_en)
        # diff = h_wv.wv.similarity(val, [k_trans_en]) - h_wv.wv.similarity(val, [k_trans_sm])
        cos_diff[k].append((val, diff))
        row.append([val, str(cos_en), str(cos_sm), str(diff)])
    # writer.writerow(str(row))
    print(row)

# f.close()
