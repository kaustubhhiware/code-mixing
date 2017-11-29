import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import math
import bisect

class triple(object):

    #word is the actual word,
    #score is either utr, uur or upr
    #values of dictionary is some other attribute
    def __init__(self,x,y,score):
        self.x = x
        self.y = y
        self.dist = score

        
    def __eq__(self, other):
        return (self.x,self.y,self.dist) == (other.x,other.y, other.dist)

    def __lt__(self,other):
         return self.dist < other.dist

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)



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


distances = []

print(len(content))
print(len(content)*len(content)) 

#exit(0)
#we will take all pairs and we will take top 500 points from them and will plot them  
i = 0
j = 100000000
k= j
for x in range(0,len(content)):

	if i==j :
		print(i,end=' ')
		j= j+k
	
	for y in range(0,len(content)):
		i =i +1
		if x ==y : 
			continue
			
		dist = math.sqrt(  (X_tsne[x][0]-X_tsne[y][0])*(X_tsne[x][0]-X_tsne[y][0]) + (X_tsne[x][1]-X_tsne[y][1])*(X_tsne[x][1]-X_tsne[y][1]) )
		temp = triple(x,y,dist)
		

		#now we need to insert them in distances list
		if len(distances)== 0 :
			distances.append(temp)
		elif len(distances) < 1000 :

			if(temp.dist <= distances[0].dist) :
				distances.insert(0,temp)
			elif temp.dist >= distances[len(distances)-1].dist :
				distances.append(temp)
			else :

				bisect.insort_left(distances,temp)
				# for i in range(0,len(distances)):
				# 	if temp.dist < distances[i].dist :
				# 		distances.insert(i,temp)
				# 		break

		elif len(distances)==1000 :
			
			if temp.dist <= distances[0].dist :
				distances.insert(0,temp)
				distances = distances[:-1]
			elif temp.dist >= distances[len(distances)-1].dist :
				continue
			else :
				bisect.insort_left(distances,temp)
				# for i in range(0,len(distances)) :
				# 	if temp.dist < distances[i].dist:
				# 		distances.insert(i,temp)
				# 		break
				distances = distances[:-1]

		
	


print('\n'+str(distances[0].dist))

visited = {}
lis = []
xlis = []
ylis = []
count =0

for x in range(0,len(distances)):

	temp = distances[x]
	if temp.x not in visited :
		visited[temp.x]=True 
		lis.append(temp.x)
		xlis.append( X_tsne[temp.x][0] )
		ylis.append( X_tsne[temp.x][1] )
		count = count +1

	if temp.y not in visited :
		visited[temp.y]=True 
		lis.append(temp.y)
		xlis.append( X_tsne[temp.y][0] )
		ylis.append( X_tsne[temp.y][1] )
		count = count +1

	
	if count>500:
		break


#now we redirect stdout to a file 
orig_stdout = sys.stdout
f = open('Top500Points_naivesm.txt', 'w')
sys.stdout = f

for x in range(0,len(lis)) :
	print( words[lis[x]] + ' ' + str(xlis[x]) + ' ' + str(ylis[x]) )

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.scatter(xlis[:], ylis[:])

#for i in range(0,len(content)):
for i in range(0,len(lis)):
	ax.annotate(words[lis[i]],(xlis[i],ylis[i]))
	#ax.annotate(txt, (dfnew['x'].iloc[i], dfnew['y'].iloc[i]) 

plt.show()




