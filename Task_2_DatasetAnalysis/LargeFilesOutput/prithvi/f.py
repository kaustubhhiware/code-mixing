import pandas as pd
from pprint import pprint


def printDictTop10(dict0):
  print('printDictTop10: type:' + str(type(dict0)))
  if type(dict0) is not dict:
    print('----------ERROR printDictTop10: input not dict')
    return
  
  if len(dict0) > 10:
    print('----------ERROR printDictTop10: len > 10')
    return
  
  i = 1
  for key,value in dict0.items():
    print(key)
    pprint(value)
    print('\n')
    i = i+1
    if i==100:
      break
  print('\n')

print('Reading the pickle file...')
tweetsCelebFrame = pd.read_pickle('CelebAll5.pkl')
# tweetsFollow = pd.read_pickle('NonCelebAll5.pkl')

def pdDataFrameToDict(frame):
  print('Converting pd dataframe to dict...')
  dict = {}
  i = 0
  for row in frame.values[:10]:
    dict[i] = {}
    dict[i]['tweetid'] = row[0]
    dict[i]['isCeleb'] = row[1]
    dict[i]['Tweet'] = row[2]
    dict[i]['Tweet-tag'] = row[3]
    dict[i]['Word-level'] = row[4].to_dict('index')
    i = i+1
  return dict

def test(tweetsCelebFrame):
  # print(type(tweetsCelebFrame))
  # print('\n\n')
  # pprint(tweetsCelebFrame)
  
  print('converting the pickle file to dict\n')
  tweetsCeleb = pdDataFrameToDict(tweetsCelebFrame)
  
  print('\n\n\n\nprinting tweets celeb 10 if in dict')
  printDictTop10(tweetsCeleb)
  
  print('\n\n')
  

test(tweetsCelebFrame)