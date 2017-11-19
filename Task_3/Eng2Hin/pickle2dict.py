import pickle

words = ['thing', 'way', 'woman',
'press', 'wrong', 'well', 'matter', 'reason', 'question',
'guy', 'moment', 'week', 'luck', 'president',
'body', 'job', 'car', 'god', 'gift', 'status', 'university',
'lyrics', 'road', 'politics', 'parliament', 'review',
'scene', 'seat', 'film', 'degree', 'people', 'play', 'house',
'service', 'rest', 'boy', 'month', 'money', 'cool', 'development',
'group', 'friend', 'day', 'performance',
'school', 'blue', 'room', 'interview', 'share', 'request',
'traffic', 'college', 'star', 'class', 'superstar', 'petrol',
'uncle']

with open('../hi/hiwords.txt','r') as f:
	Hi = f.readlines()

Hi = [x.strip() for x in Hi]
def singlewords(l):
	'''
		takes a list, returns a string of only one word components
	'''
	s = ''
	for each in l:
		if len(each.split(' ')) == 1 and each in Hi:
			s += each + ' X,'

	return s


e = pickle.load(open('EN2HIdict-trimmed.pkl','rb'))
l = []

with open('../sm.txt','r') as f:
	txt = f.readlines()
for each in txt:
	s = each.split(' ')
	for x in s:
		if x.endswith('$'):
			l.append(x[:-1]) # all english nouns in hindi context


with open('en2hi.txt','w') as f:
	for each in e:
		if each in l:
			f.write(each + ':{ ' + singlewords(e[each]) +' }\n')