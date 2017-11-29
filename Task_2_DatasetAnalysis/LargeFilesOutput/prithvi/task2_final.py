'''
nlp term project

L1 is hindi.
L2 is english.

2 Tweet sets: Celeb and 'followers' tweets are taken
    The tweets are word tagged and tweet tagged
  
sets of nouns among them are supposed to be taken

jaccord coeff should be calculated for the two sets

utr and uur for the words in the two sets are calculated and sorted accordingly

spearmans coeff is calculated for the two sets

"0": {
        "tweetid": 873141672586117122, 
        "username": "Sameer", 
        "id": 2436645000, 
        "isCeleb": 1, 
        "Tweet": "RT @suhasinih: Press Club of India turns out in full force in support of Press Freedom in the country! #Dontshootthemessenger https://t.co/…", 
        "Tweet-tag": "ENGLISH", ("HINDI", "CME", "CMH", "CMEQ", "CS", "OTHER") 
        "Word-level": {
            "Press": {
                "Label": "EN", ("HI", "NE", "OTHER") 
                "Matrix": "EN"
            }, 
            
        }
    }

'''

import sys
import json
import pandas as pd
from pprint import pprint
import nltk
import numpy as np
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

from nltk.corpus import wordnet as wn
nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}



# with open('Celebrity_ALL.pkl', 'rb') as f:
#     tweetsCeleb = pickle.load(f)

# with open('NonCelebrity_All.pkl', 'rb') as f:
#     tweetsFollow = pickle.load(f)

# fin = open('Celebrity1.txt', encoding = 'utf-8')
# tweetsCeleb = json.load(fin)

# fin = open('NonCelebrity1.txt', encoding = 'utf-8')
# tweetsFollow = json.load(fin)

print('Reading the tweetCeleb pickle file...\n')
tweetsCelebFrame = pd.read_pickle('Celebrity_ALL.pkl')
# tweetsCelebFrame = None

print('Reading the tweetFollow pickle file...\n')
tweetsFollowFrame = pd.read_pickle('NonCelebrity_ALL.pkl')
# tweetsFollowFrame = None


#################### BEGIN Converting Pickle Files to dict #####################

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

def processTweets(tweets):  
  #tweets is a dict
  
  dict = {'size': len(tweets), 'hi': 0, 'cmh': 0, 'en': 0, 'cme': 0, 'cmeq': 0, 'cs': 0}
  
  for key,val in tweets.items():
    if val['Tweet-tag'] == 'HINDI':
      dict['hi'] = dict['hi'] + 1
    elif val['Tweet-tag'] == 'ENGLISH':
      dict['en'] = dict['en'] + 1
    elif val['Tweet-tag'] == 'CMH':
      dict['cmh'] = dict['cmh'] + 1
    elif val['Tweet-tag'] == 'CME':
      dict['cme'] = dict['cme'] + 1
    elif val['Tweet-tag'] == 'CMEQ':
      dict['cmeq'] = dict['cmeq'] + 1
    elif val['Tweet-tag'] == 'CS':
      dict['cs'] = dict['cs'] + 1
  
  return dict

def pdDataFrameToDict(frame):
  print('Converting pd dataframe to dict...\n')
  dict = {}
  wrongFormatTweets = 0
  i = 0
  for row in frame.values:
    if type(row[2]) is not str:
      wrongFormatTweets = wrongFormatTweets + 1
      continue
    
    dict[i] = {}
    dict[i]['tweetid'] = row[0]
    dict[i]['isCeleb'] = row[1]
    dict[i]['Tweet'] = row[2]
    if type(dict[i]['Tweet']) is float:
      print('ERROR pdDataFrameToDict')
      print(row)
    dict[i]['Tweet-tag'] = row[3]
    dict[i]['Word-level'] = row[4].to_dict('index')
    i = i+1
  
  print('pdDataFrameToDict: wrongFormatTweets: ' + str(wrongFormatTweets) + '\n')
  return dict

def generateTweetDicts(tweetsCelebFrame, tweetsFollowFrame):
  # print(type(tweetsCelebFrame))
  # print('\n\n')
  # pprint(tweetsCelebFrame)
  tweetsDict = {}
  
  print('converting the tweetCelebframe to dict...')
  tweetsCeleb = pdDataFrameToDict(tweetsCelebFrame)
  
  # infoCeleb = processTweets(tweetsCeleb)
  # print(infoCeleb)
  
  print('converting the tweetFollowframe to dict...')
  tweetsFollow = pdDataFrameToDict(tweetsFollowFrame)
  
  tweetsDict['celeb'] = tweetsCeleb
  tweetsDict['follow'] = tweetsFollow
  return tweetsDict


tweetsDict = generateTweetDicts(tweetsCelebFrame, tweetsFollowFrame)
tweetsCeleb = tweetsDict['celeb']
tweetsFollow = tweetsDict['follow']

#################### END Converting Pickle Files to dict #####################










def getUsernameFromTweetString(tweet):
  #tweet is string
  start = 0
  username = ''
 
  for i in tweet:
    if i == ':':
      break
    if i == '@':
      start = 1
    if start:
      username = username + i
  
  return username

def addCelebUsername(tweet):
  #tweet is dict having single tweet
  #scans the celeb tweet string and gets the username
  
  if tweet['isCeleb'] == 1:
    if type(tweet['Tweet']) is float:
      print('error')
      pprint(tweet)
    CelebUsername = getUsernameFromTweetString(tweet['Tweet'])
    tweet['CelebUsername'] = CelebUsername

def updateCelebUsernames(tweets):
  #tweet is dict having many tweets
  
  for key, val in tweets.items():
    addCelebUsername(val)

def removeRepeatedCelebTweets(tweets):
  dict = {}
  i = 0
  tweetList = []
  
  for key, val in tweets.items():
    if val['isCeleb'] == 1:
      if val['Tweet'] not in tweetList:
        dict[i] = val
        tweetList.append(val['Tweet'])
        i = i+1
  
  return dict



def segregateTweets(tweets):
  #the function not yet properly started
  dict = {'size': len(tweets), 'hi': 0, 'cmh': 0, 'en': 0, 'cme': 0, 'cmeq': 0, 'cs': 0}


def upr(tweets):
  #tweets is dict containing many tweets
  #returns a dictionary with 'upr values etc' of english words in hindi tweets
  dict = {}
  
  #traversing the tweets
  #extracting english words in hindi tweets into dict (why? fill later) 
  #and calulating corresponding dict[word]['hi']
  for key,val in tweets.items():
    if val['Tweet-tag'] == 'HINDI' or val['Tweet-tag'] == 'CMH':
      for word in val['Word-level'].keys():
        if val['Word-level'][word]['Label'] == 'EN':
          #check if this word is noun
          if word not in nouns:
            continue
          
          #add this word 
          if word not in dict.keys():
            dict[word] = {'hi': 1, 'en': 0, 'upr': '-2'} #-2: not yet calculated
          else:
            dict[word]['hi'] = dict[word]['hi'] + 1
  
  #traversing the tweets
  #updating the dict[word]['en']
  for key,val in tweets.items():
    if val['Tweet-tag'] != 'HINDI' and val['Tweet-tag'] != 'CMH':
      for word in val['Word-level'].keys():
        if val['Word-level'][word]['Label'] == 'EN':
          if word in dict.keys():
            dict[word]['en'] = dict[word]['en'] + 1
  
  #updating upr values in dict
  for key, val in dict.items():
    if val['en'] != 0:
      val['upr'] = val['hi'] / val['en']
    else:
      val['upr'] = -1  
  
  return dict  

def utr(tweets):
  #tweets is dict containing many tweets
  #returns a dictionary with 'utr values etc' of english words in hindi tweets
  dict = {}
  
  #traversing the tweets
  #extracting english words in hindi tweets into dict 
  #and calulating corresponding dict[word]['hi'] etc
  for key,val in tweets.items():
    if val['Tweet-tag'] == 'HINDI' or val['Tweet-tag'] == 'CMH':
      for word in val['Word-level'].keys():
        if val['Word-level'][word]['Label'] == 'EN':
          #check if this word is noun
          if word not in nouns:
            continue
          if word == 'Riteish':
            print('--------------------------ERROR nouns failed')
          #add this word
          if word not in dict.keys():
            dict[word] = {'hi': 0, 'cmh': 0, 'en': 0}
          
          if val['Tweet-tag'] == 'HINDI':
            dict[word]['hi'] = dict[word]['hi'] + 1
          else:
            dict[word]['cmh'] = dict[word]['cmh'] + 1
  
  #traversing the tweets
  #updating the dict[word]['en']
  for key,val in tweets.items():
    if val['Tweet-tag'] == 'ENGLISH':
      for word in val['Word-level'].keys():
        if val['Word-level'][word]['Label'] == 'EN':
          if word in dict.keys():
            dict[word]['en'] = dict[word]['en'] + 1
  
  #updating utr values in dict
  for key, val in dict.items():
    if val['en'] != 0:
      val['utr'] = (val['hi'] + val['cmh']) / val['en']
    else:
      val['utr'] = -1  
  
  return dict  


def uur(tweets):
  #tweets is dict containing many tweets
  #returns a dictionary with 'uur values etc' of english words in hindi tweets
  dict = {}
  
  #traversing the tweets
  #extracting english words in hindi tweets and its user into dict[word]['hi'] 
  for key,val in tweets.items():
    if val['Tweet-tag'] == 'HINDI' or val['Tweet-tag'] == 'CMH':
      for word in val['Word-level'].keys():
        if val['Word-level'][word]['Label'] == 'EN':
          #check if this word is noun
          if word not in nouns:
            continue
          
          #add this word 
          if word not in dict.keys():
            dict[word] = {'hi': {}, 'cmh': {}, 'en': {}}
          
          if val['isCeleb']:
            username = val['CelebUsername']
          else:
            username = val['username']  
          
          if val['Tweet-tag'] == "HINDI":
            label = 'hi'
          else:
            label = 'cmh'  
            
          if username not in dict[word][label].keys():
            dict[word][label][username] = 0
          
          dict[word][label][username] = dict[word][label][username] + 1          
  
  #traversing the tweets
  #updating the dict[word]['en']
  for key,val in tweets.items():
    if val['Tweet-tag'] == 'ENGLISH':
      for word in val['Word-level'].keys():
        if val['Word-level'][word]['Label'] == 'EN':
          if word in dict.keys():
            if val['isCeleb']:
              username = val['CelebUsername']
            else:
              username = val['username']
            
            if username not in dict[word]['en'].keys():
              dict[word]['en'][username] = 0
            
            dict[word]['en'][username] = dict[word]['en'][username] + 1
  
  #updating uur values in dict
  for key, val in dict.items():
    if len(val['en']) != 0:
      val['uur'] = (len(val['hi']) + len(val['cmh'])) / len(val['en'])
    else:
      val['uur'] = -1  
  
  dict2 = {}
  for key,val in dict.items():
    dict2[key] = {'hi':len(val['hi']), 'cmh':len(val['cmh']), 'en':len(val['en']), 'uur': val['uur']}
  
  return dict2 














  




######################################################### BEGIN Karthik Functions Part #################
@functools.total_ordering
class word_score(object):
    def __init__(self,word,score):
        self.word = word
        self.score = score
    
    def __eq__(self, other):
        return (self.word,self.score) == (other.word, other.score)
    
    def __lt__(self,other):
         return self.score > other.score
    
    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)
    
    def __repr__(self):
        if self.score !=0.0 :
            return ('[word=%s score=%lf] ' % (repr(self.word), float(repr(self.score) )  ) )
        else : 
            return ''

@functools.total_ordering
class measure(object):
    
    #word is the actual word,
    #score is either utr, uur or upr
    #values of dictionary is some other attribute
    def __init__(self,word,values,score):
        self.word = word
        self.values= values
        self.score = score
    
    def __eq__(self, other):
        return (self.word,self.score) == (other.word, other.score)
    
    def __lt__(self,other):
         return self.score > other.score
    
    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)


def unique(a):
    
    """ return the list with duplicate elements removed """
    return list(set(a))

def printTop100(dict,type):
  
  dicti = {}
  stri = ''
  if type==1 :
    stri ='utr'
  elif type==2:
    stri ='uur'
  else :
    stri ='upr'
  
  list = []
  for key,value in dict.items():
    a = """ { 'en' :""" +str(value['en']) +', '
    b =""" 'hi' : """ + str(value['hi']) +', '
    c ="""'""" +stri+"""': """+str(value[stri])+'}' 
    d = a + b +c
    
    x = measure(key,d,value[stri])
    list.append(x)
  
  list.sort()
  print('Length of list is ')
  print(len(list))
  list = list[:100]
  
  print('----------------------Printing top 100 '+stri+' values in order ---------------------------------')
  for x in list :
    strin = """{ '""" + x.word + """' : """ + x.values +' }, '
    dicti[x.word]=x.score
    print(strin)
  print('\n\n\n')
  
  print('dictionary size is ',end=' ')
  print(len(dicti))
  return dicti
#lines 498 to  535

def printTopNWords(dict,type,n):
  
  dicti = {}
  stri = ''
  if type==1 :
    stri ='utr'
  elif type==2:
    stri ='uur'
  else :
    stri ='upr'
  
  list = []
  for key,value in dict.items():
    a = """ { 'en' :""" +str(value['en']) +', '
    b =""" 'hi' : """ + str(value['hi']) +', '
    c ="""'""" +stri+"""': """+str(value[stri])+'}' 
    d = a + b +c
    
    x = measure(key,d,value[stri])
    list.append(x)
  
  list.sort()
  print('Length of list is ')
  print(len(list))
  list = list[:n]
  
  print('----------------------Printing top ' + str(n) + ' ' + stri+' values in order ---------------------------------')
  for x in list : 
    strin = """{ '""" + x.word + """' : """ + x.values +' }, '
    dicti[x.word]=x.score
    print(strin)
  print('\n\n\n')
  
  print('dictionary size is ',end=' ')
  print(len(dicti))
  return dicti


def compute_jaccard_index(set_1, set_2):
    
    n = len(set_1.intersection(set_2))
    
    le =float( len(set_1) + len(set_2)-n )
    
    if le!=0 :
      return n / float(len(set_1) + len(set_2) - n) 
    else : 
      return 0


#calculates the spearman coefficient between two sets
def spearman_correlation(dict1,dict2,type):
  """
    The dictionary items are of the form  "a" :{en}
    {'Ab': {'cmh': 3, 'en': 0, 'hi': 0, 'utr': -1},   {'Ab': {'cmh': 2, 'en': 0, 'hi': 0, 'utr': -1},
     'Agar': {'cmh': 1, 'en': 1, 'hi': 0, 'utr': 1.0},     'Agar': {'cmh': 1, 'en': 0, 'hi': 0, 'utr': -1},
     'Ajay': {'cmh': 1, 'en': 1, 'hi': 0, 'utr': 1.0},

  """
  
  #https://stackoverflow.com/questions/19428029/how-to-get-correlation-of-two-vectors-in-python/19429478
  
  keys = list(dict1.keys() & dict2.keys())
  keys = unique(keys)
  list1 = []
  list2 = []
  X = []
  Y = []
  stri =''
  
  #based on type , we can calculate utr , uut , upr
  if type==1:
    stri ='utr'
  elif type==2:
    stri='uur'
  else :
    stri ='upr'
  
  for key,value in dict1.items():
    
    #add this key to dictionary_intersection
    if key in keys :
      temp = word_score(key,value)
      list1.append(temp)
  
  for key,value in dict2.items():
  
    if key in keys:
      temp = word_score(key,value)
      list2.append(temp)
  
  list1.sort(key=operator.attrgetter('word'))
  list2.sort(key=operator.attrgetter('word'))
  
  for x in list1:
    X.append(x.score)
  
  for y in list2:
    Y.append(y.score)
  
  spearman_corr = spearmanr(X,Y)
  return spearman_corr


######################################################### END Karthik Functions Part #################




























#########################################################################################
def final(tweetsCeleb, tweetsFollow):
  
  ################### celeb #################
  print('====================================Celeb====================================' + '\n')
  
  print(type(tweetsCeleb))
  
  #info before removing repeated
  infoCeleb = processTweets(tweetsCeleb)
  print('tweet content original')
  pprint (infoCeleb)
  print ('\n')
  
  ################### The following is only for celeb #################
  #remove repeated celeb tweets
  tweetsCeleb = removeRepeatedCelebTweets(tweetsCeleb)
  
  #info after removing repeated
  print('tweet content original after removing repetitions')
  infoCeleb = processTweets(tweetsCeleb)
  pprint (infoCeleb)
  print ('\n')
  
  
  ################### The following is only for celeb #################
  #extract and add the celeb username from/to the tweets 
  updateCelebUsernames(tweetsCeleb)
  
  
  
  utrCeleb = utr(tweetsCeleb)
  
  #words for which utr>0
  print ('words for which utr etc > 0')
  print ('size: ' + str(len(utrCeleb)))
  print (utrCeleb.keys())
  print ('\n\n\n')
  
  print ('----------------------------------utr----------------------------------')  
  print('utr len: ' + str(len(utrCeleb)))
  pprint (utrCeleb)
  print ('\n\n\n')
  
  print ('----------------------------------uur----------------------------------')  
  uurCeleb = uur(tweetsCeleb)
  print('uur len: ' + str(len(uurCeleb)))
  pprint (uurCeleb)
  print ('\n\n\n')
  
  print ('----------------------------------upr----------------------------------')  
  uprCeleb = upr(tweetsCeleb)
  print('upr len: ' + str(len(uprCeleb)))
  pprint (uprCeleb)
  print ('\n\n\n')
  
  
  ################## Followers #################
  
  print('====================================Followers===================================='+'\n')
  
  #info of the tweets
  print('tweet content')
  infoCeleb = processTweets(tweetsFollow)
  pprint (infoCeleb)
  print ('\n\n\n')
  
  utrFollow = utr(tweetsFollow)
  
  #words for which utr>0
  print ('words for which utr etc > 0')
  print ('size: ' + str(len(utrFollow)))
  print (utrFollow.keys())
  print ('\n\n\n')
  
  print ('----------------------------------utr----------------------------------')  
  print('utr len: ' + str(len(utrFollow)))
  pprint (utrFollow)
  print ('\n\n\n')
  
  # print ('----------------------------------uur----------------------------------')  
  # uurFollow = uur(tweetsFollow)
  # print('uur len: ' + str(len(uurFollow)))
  # pprint (uurFollow)
  # print ('\n\n\n')
  
  
  print ('----------------------------------upr----------------------------------')  
  uprFollow = upr(tweetsFollow)
  print('upr len: ' + str(len(uprFollow)))
  pprint (uprFollow)
  print ('\n\n\n')
  
  
  ################################################## Karthik Code
  # set n here ,lines 391 to 412
  
  test_list=[50,100,200,1000]
  # n.append(50)
  # n.append(100)
  # n.append(200)
  # n.append(300)
  
  for n in test_list :
    
    print('\n\n\n\n')
    print('Printing for the top '+str(n)+'words' )
    
    ########################################## Side Part , Printing only the top 100 words of Celebrity utr ,uut ,upr 
    print('====================================Celebrities===================================='+'\n')
    utrCelebTop = printTopNWords(utrCeleb,1,n)
    uurCelebTop = printTopNWords(uurCeleb,2,n)
    uprCelebTop = printTopNWords(uprCeleb,3,n)
    print('\n\n\n')
    
    ######################################################## Printing Only the top 100 words of Followers utr, uur,upr
    print('====================================Followers===================================='+'\n')
    utrFollowTop = printTopNWords(utrFollow,1,n)
    # uurFollowTop = printTopNWords(uurFollow,2,n)
    uprFollowTop = printTopNWords(uprFollow,3,n)
    
    ######################## Jacard Index Calculation 
    print('-------------------------------Jacard Index between words of Celebrities and Followers --------------------------------')
    print('Jacard Index between Celebrity and Follower Words are ',end=' ')
    J = compute_jaccard_index(set(utrCeleb.keys()),set(utrFollow.keys()))
    print(J)
    print('\n\n\n')
    
    ######################## Spearman Correlation
    print ('-------------------------------spearman for utr-----------------------')
    spearman_corr = spearman_correlation(utrFollowTop,utrCelebTop,1)
    print(spearman_corr)
    print('\n')
    
    # print ('-------------------------------spearman for uur-----------------------')
    # spearman_corr = spearman_correlation(uurFollowTop,uurCelebTop,2)
    # print(spearman_corr)
    # print('\n')
    
    print ('-------------------------------spearman for upr-----------------------')
    spearman_corr = spearman_correlation(uprFollowTop,uprCelebTop,3)
    print(spearman_corr)
    print('\n')


#now we redirect stdout to a file 
orig_stdout = sys.stdout
f = open('T2Output_.txt', 'w')
sys.stdout = f

#Main Function Call
final(tweetsCeleb, tweetsFollow)
sys.stdout=orig_stdout






























##################################################################################
#THE FOLLOWING FUNCTIONS ARE NOT USEFUL FOR OUR GOAL

# def getWords(tweets):
#   #tweets is a dict
#   #returns list of english words present in hindi or cmh tweets
#   #(rest of the english words in the tweets - utr etc is 0)
  
#   words = []

#   for key,val in tweets.items():
#     if val['Tweet-tag'] == 'HINDI' or val['Tweet-tag'] == 'CMH':
#       for key1,val1 in val['Word-level'].items():
#         if val1['Label'] == 'EN':
#           if key1 not in words:
#             words.append(key1)
#             # print(key)
#             # pprint(val)
#             # print(key1 + '\n')

#   return words

# def getWordTagFromWordLevel(word, wordLevel):
#   #word is a string
#   #wordLevel is a dict with word level tags
#   #this returns the tag of the corresponding word of inputword in wordLevel
#   #if not present return none
  
#   for key in wordLevel.keys():
#     if key in word:
#       return wordLevel[key]['label']

#   return None


##################################################################################
#THE FOLLOWING FUNCTIONS ARE OLD,WRONG OUTPUT OR NOT OPTIMAL


# def utrWord(tweets, word):
#   #tweets dict, word string
#   #returns a dict with dict[hindi(cmh,english)] values
  
#   dict = {'hi': 0, 'cmh': 0, 'en': 0 }

#   for key, val in tweets.items():
#     if word in val['Word-level'].keys():
#       if val['Tweet-tag'] == 'HINDI':
#         dict['hi'] = dict['hi'] + 1
#       elif val['Tweet-tag'] == 'CMH':
#         dict['cmh'] = dict['cmh'] + 1
#       elif val['Tweet-tag'] == 'ENGLISH':
#         dict['en'] = dict['en'] + 1

#   if dict['en'] == 0:
#     dict['utr'] = -1
#   else:
#     dict['utr'] = (dict['hi'] + dict['cmh']) / dict['en']

#   return dict



# def utr0(tweets, words):
#   #tweets is dict, words is list
#   #returns a dictionary with 'utr values etc'
#   dict = {}

#   for i in words:
#     dict1 = utrWord(tweets, i)
#     dict[i] = dict1

#   return dict  

# def uurWord(tweets, word):
#   #tweets dict, word string
#   #returns a dict with dict[hindi(cmh,english)] values
  
#   dict = {'hi': 0, 'cmh': 0, 'en': 0 }

#   #used for storing users who used this word
#   usersHI = []
#   usersCMH = []
#   usersEN = []


#   for key, val in tweets.items():
#     if word in val['Word-level'].keys():
#       if val['isCeleb'] == 1:
#         username = val['CelebUsername']
#       else:
#         username = val['username']

#       if val['Tweet-tag'] == 'HINDI':
#         if username not in usersHI:
#           usersHI.append(username)
#           dict['hi'] = dict['hi'] + 1
          
#       elif val['Tweet-tag'] == 'CMH':
#         if username not in usersCMH:
#           usersCMH.append(username)
#           dict['cmh'] = dict['cmh'] + 1
      
#       elif val['Tweet-tag'] == 'ENGLISH':
#         if username not in usersEN:
#           usersEN.append(username)
#           dict['en'] = dict['en'] + 1

#   if dict['en'] == 0:
#     dict['uur'] = -1
#   else:
#     dict['uur'] = (dict['hi'] + dict['cmh']) / dict['en']

#   return dict

# def uur0(tweets, words):
#   #tweets is dict, words is list
#   #returns a dictionary with 'uur values etc'
  
#   dict = {}

#   for i in words:
#     dict1 = uurWord(tweets, i)
#     dict[i] = dict1

#   return dict


