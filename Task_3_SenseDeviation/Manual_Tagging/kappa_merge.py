import re
import pickle

words = ['thing', 'way', 'woman', 'press', 'wrong', 'well','matter', 'reason', 
'question', 'guy', 'moment', 'week', 'luck',  'president', 'body', 'job', 
'car', 'god', 'gift', 'status',  'university', 'lyrics', 'road', 'politics',
'parliament',  'review', 'scene', 'seat', 'film', 'degree','people', 'play',
'house', 'service', 'rest', 'boy', 'month', 'money', 'cool',   'development', 
'group', 'friend', 'day', 'performance', 'school', 'blue', 'room', 'interview',
'share', 'request','traffic', 'college', 'star', 'class', 'superstar', 'petrol', 'uncle']

# writing down verbosely so it can be easily copy-pasted
'''
	Get intersection of two results given by the users, find kappa -value from it.
'''

with open('karthik-tags.txt','r') as f:
	a = f.readlines()

for i in range(len(a)):
	a[i] = [y for y in re.split(':|{ |,| |}|\n',a[i]) if y]
	a[i].append(' ') # add empty value for next step

with open('prithvi-tags.txt','r') as f:
	b = f.readlines()

for i in range(len(a)):
	b[i] = [y for y in re.split(':|{ |,| |}|\n',b[i]) if y]
	b[i].append(' ') # add empty value for next step

d, d2 = {}, {}
aYesbYes, aYesbNo, aNobYes, aNobNo = 0, 0 ,0, 0
for i in range(len(a)): # len(a) == len(b) no. of words
	key = a[i][0]
	val = []
	senseA, senseB, notsenseA, notsenseB = [], [], [], []
	for j in range(1, len(a[i])-1):
		if a[i][j+1] is not 'X' and not a[i][j].endswith('X'):
			senseA.append(a[i][j])#.encode('utf-8')
		else:
			notsenseA.append(a[i][j])
	#
	# a[i] and b[i] may have different lengths
	for j in range(1, len(b[i])-1):
		if b[i][j+1] is not 'X' and not b[i][j].endswith('X'):
			senseB.append(b[i][j])#.encode('utf-8'))
		else:
			notsenseB.append(b[i][j])
	#
	# conversion to set mandatory
	intersection = list(set(senseA) & set(senseB))
	val = list(set(senseA) | set(senseB) )
	aYesbYes += len( intersection )
	aYesbNo += len( list( set(senseA) - set(intersection) ) )
	aNobYes += len( list( set(senseB) - set(intersection) ) )
	aNobNo += len( list( set(notsenseA) & set(notsenseB) ) )
	#
	if len(val) is not 0:
		if key.lower() in words:
			d2[key] = val
		else:
			d[key] = val

print('+++--- Kappa value')
print('aYesbYes', aYesbYes, '\n aYesbNo', aYesbNo)
print('aNobYes', aNobYes, '\n aNobNo', aNobNo)
n = aYesbYes + aYesbNo + aNobYes + aNobNo
pO = 1.0 * (aYesbYes + aNobNo) / n # Observed
pYes = 1.0 * (aYesbYes + aYesbNo) * (aYesbYes + aNobYes) / (n * n)
pNo = 1.0* (aNobYes + aNobNo) * (aNobNo + aYesbNo) / (n * n)
pE = pYes + pNo # Expected

k = (pO - pE) / (1 - pE)
print('+++--- Kappa value = ', k)

output = open('SM2HIdict-train.pkl','wb')
pickle.dump(d, output)
output.close()

output2 = open('SM2HIdict-test.pkl','wb')
pickle.dump(d2, output2)
output2.close()

with open('sm2hi-train.txt','w') as f:
	for each in d:
		f.write(each + ': ' + str(d[each]) + '\n')


with open('sm2hi-test.txt','w') as f:
	for each in d2:
		f.write(each + ': ' + str(d2[each]) + '\n')


exit()
lonely = {} # the words for which a hindi interpretation could not be found :/
			# might contain invalid words, need to only distinguish proper words
for each in t:
	if each[0] not in d and each[0] not in d2:
		lonely[each[0]] = each[1:]

with open('untagged-sm.txt','w') as f:
	for each in lonely:
		f.write(each + ': ' + str(lonely[each]) + '\n')