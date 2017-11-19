import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

with open('naive-sm-points.txt') as fname :
	content = fname.readlines()

#print(type(content[0]))

X_tsne =  np.zeros((len(content),2))
words =[]

# exit()

i=0
for x in content :

	
	lis = x.split()
	#print(lis[0])
	#lis[2]=lis[2][:-1]
	X_tsne[i][0]=float(lis[1])
	X_tsne[i][1]=float(lis[2])
	words.append(lis[0])
	i=i+1




fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.scatter(X_tsne[:,0], X_tsne[:,1])

#for i in range(0,len(content)):
#for i in range(0,len(content)):
	#ax.annotate(words[i],(X_tsne[i][0],X_tsne[i][1] ))
	#ax.annotate(txt, (dfnew['x'].iloc[i], dfnew['y'].iloc[i]) 

plt.show()


