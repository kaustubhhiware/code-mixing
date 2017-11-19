
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

#prop = fm.FontProperties(fname='/mnt/c')
plt.rc('font', family='Lohit Devanagari')


x = [f.name for f in matplotlib.font_manager.fontManager.ttflist]
#matplotlib.use('Agg')
#print(x)



orig_stdout = sys.stdout
f = open('w2vhindi_points.txt', 'w')
sys.stdout = f



with codecs.open('hi.tsv', encoding='utf-8') as tsv:
	AoA = [line.strip().split('\t') for line in tsv]
	#print(len(AoA))
	#print(AoA[1])
	#print(type(AoA[1]))
	#print(len(AoA[1]))
	#quit()


#print(AoA[])

def extract(AoA,total_words):

	#1st line is of type str with word at 1st location and indices at location  
	vectors = np.zeros(shape=(total_words,305))
	words = []


	# Extraction Part 

	j = 0
	k = 0
	flag =False

	while k < total_words :

		

		if j>=len(AoA):
			break

		if flag==False :
			#print(AoA[j][1])
			flag =True

		# first extract via len of list
		words.append(AoA[j][1])

		#since the first line has values in str type , split them and add
		eoe = AoA[j][2].split()

		if eoe[0][0]=='[' :

			if len(eoe[0])>2 :
				eoe[0] = eoe[0][1:]
			else :
				eoe =eoe[1:]

		

		l = 0

		for x in eoe :
			vectors[k][l]=float(x)
			l=l+1


		i=j+1

		while True :

			if i >= len(AoA) or len(AoA[i])>1 :
				break
			else :

				eoe =  AoA[i][0].split()
				
				y = len(eoe)
				st = eoe[y-1]

				if st[len(st)-1]==']' :
					eoe[y-1] = st[:-1]


				#eoe = eoe[:-1]
				for x in eoe:

					if len(x) >0 :
						vectors[k][l]=float(x)
						l=l+1

			i= i+1

		j=i
		k=k+1

	return [words,vectors]

def func(AoA,n) :

	words, vectors = extract(AoA,n)

	#print(words[0])
	#print('Extraction Done ')

	list_of_lists = []
	columns = []
	for x in range(0,300):
		columns.append(x)


	for i in range(0,n):

		lis =[]
		#print('[')
		for j in range(0,vectors.shape[1]):
			if vectors[i][j]==0: 
				break
			#print(vectors[i][j],end=' ')
			lis.append(vectors[i][j])

		#print(']\n\n')
		list_of_lists.append(lis)


	df =pandas.DataFrame(list_of_lists,columns = columns)

	#print("Extraction of vectors done ")
	

	start = time.clock()

	tsne = TSNE(n_components=2)
	X_tsne = tsne.fit_transform(df)
	
	#print(str(time.clock()-start)+'For Data Size of '+str(n)+'\n\n\n') 


	#print(' transformation done ')

	for i in range(0,X_tsne.shape[0]) :
		print(words[i],end=' ')
		print(X_tsne[i][0],end=' ')
		print(X_tsne[i][1])

	
	 
	


	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.scatter(X_tsne[:,0], X_tsne[:,1])
	for i in range(0,n):
		ax.annotate(words[i],(X_tsne[i][0],X_tsne[i][1] ))
	#ax.annotate(txt, (dfnew['x'].iloc[i], dfnew['y'].iloc[i]) 
	plt.show()





# x =10 
# while(x<100) :
	
# 	func(AoA,x)	
# 	print("\n\n")
# 	x = x*10

func(AoA,30390)

# print(len(words))
# #print(words[0].decode('utf-8'))
# #print(words[1].decode('utf-8'))
# #print(words[30392])
# print(vectors[0][0])
# print(vectors[30392][0])

