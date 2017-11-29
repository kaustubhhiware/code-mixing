import re
import pickle
# import transliteration 
'''
	get from manually tagged entries, Social media's english word
			and the senses it is used in social media Hindi
sample:
'permission:{ लाइसेंस ,परमिट ,अनुमति }\n'
'''

# c = transliteration.getInstance()
def hindify(word):
	result = ''
	# result = c.transliterate(word, "hi_IN")
	return result.encode('utf-8')

# words = ['give','get','till','there','nothing','can','victory',
# 'more','today','will','here','way','people','moment','like',
# 'double','class','expert','serial','cricketer','captain',
# 'politician','artist','sir','information','problem','channel',
# 'phone','crore','desk','dance','family','trophy','army','reply',
# 'reservation','romantic','uncle','song','list','server','bank','film',
# 'spelling','cake','computer','typing','audition','fat','plate',
# 'certificate','bomb','prediction','star','joke','production','mobile']

words = ['thing', 'way', 'woman', 'press', 'wrong', 'well','matter', 'reason', 'question', 'guy', 'moment', 'week', 'luck',  'president', 'body', 'job', 'car', 'god', 'gift', 'status',  'university', 'lyrics', 'road', 'politics', 'parliament',  'review', 'scene', 'seat', 'film', 'degree','people', 'play', 'house', 'service', 'rest', 'boy', 'month', 'money', 'cool',   'development', 'group', 'friend', 'day', 'performance', 'school', 'blue', 'room', 'interview', 'share', 'request','traffic', 'college', 'star', 'class', 'superstar', 'petrol', 'uncle']

with open('tagged-sm.txt','r') as f:
	t = f.readlines()

for i in range(len(t)):
	# x = re.split(':|{ |,| |}|\n', t[i])
	t[i] = [y for y in re.split(':|{ |,| |}|\n',t[i]) if y]
	t[i].append(' ') # add empty value for next step
	# if t[i][0] == 'horn':
	# 	print(t[i])
	# 	print(x)

d = {}
d2 = {}
for i in range(len(t)):
	key = t[i][0]
	val = []
	for j in range(1, len(t[i])-1):
		if t[i][j+1] is not 'X' and not t[i][j].endswith('X'):
			val.append(t[i][j])#.encode('utf-8'))
	if len(val) is not 0:
		if key.lower() in words:
			d2[key] = val
		else:
			d[key] = val

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



lonely = {} # the words for which a hindi interpretation could not be found :/
			# might contain invalid words, need to only distinguish proper words
for each in t:
	if each[0] not in d and each[0] not in d2:
		lonely[each[0]] = each[1:]

with open('untagged-sm.txt','w') as f:
	for each in lonely:
		f.write(each + ': ' + str(lonely[each]) + '\n')

exit()

one, many = {}, {}
for each in d:
	if len(d[each]) == 1:
		one[each] = d[each]
	else:
		many[each] = d[each]

with open('one-meanings.txt','w') as f:
	for each in one:
		f.write(each + ': ' + str(d[each]) + '\n')

with open('many-meanings.txt','w') as f:
	for each in many:
		f.write(each + ': ' + str(d[each]) + '\n')

hindione, hindimany = {}, {}
for each in one:
	if hindify(each) in one[each]:
		print('one',each)
		hindione[each] = one[each]

for each in many:
	if hindify(each) in many[each]:
		print('many',each)
		hindimany[each] = many[each]

with open('hindi-one.txt','w') as f:
	for each in one:
		f.write(each + ': ' + str(d[each]) + '\n')

with open('hindi-many.txt','w') as f:
	for each in many:
		f.write(each + ': ' + str(d[each]) + '\n')
