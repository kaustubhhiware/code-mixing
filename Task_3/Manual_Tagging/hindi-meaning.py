with open('one-meanings.txt','r') as f:
	one = f.readlines()
with open('many-meanings.txt','r') as f:
	many = f.readlines()

onehindi, manyhindi = [], []
for each in one:
	each = each.strip()
	if each.endswith(' x') or each.endswith('x '):
		print(each)
		onehindi.append(each[:-2] + '\n')

for each in many:
	each = each.strip()
	if each.endswith('x') or each.endswith('x '):
		manyhindi.append(each[:-2] + '\n')

with open('one-hindi.txt','w') as f:
	for each in onehindi:
		f.write(each)

with open('many-hindi.txt','w') as f:
	for each in manyhindi:
		f.write(each)		