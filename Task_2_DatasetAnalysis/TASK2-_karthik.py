#system library python 3.5
import sys
sys.path.append("/usr/local/lib/python3.5/site-packages")

#other user - defined libraries
import nltk
import numpy as np
import pandas as pd
import functools
import json

#Tagger for hindi Pos
from nltk.corpus import indian
from nltk.tag import tnt

##################### Downloads from nltk mentioned here
nltk.download('indian')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
########################################


#also train the tagger with hindi sentences
train_data = indian.tagged_sents('hindi.pos')
tnt_pos_tagger = tnt.TnT()
tnt_pos_tagger.train(train_data) #Training the tnt Part of speech tagger with hindi data

################# Stop words 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))

#used to check if a word is hindi or not
seperators = [u"।", u",", u"."]


#now we redirect stdout to a file 
orig_stdout = sys.stdout
f = open('T2Output.txt', 'w')
sys.stdout = f


################################# DECODING PART ######################################################################
json_decode ={}
with open("output.txt", encoding='utf-8-sig') as fin:
    json_decode = json.load(fin)
    

################################# DECODING PART ######################################################################


"""

The data is assumed to be given in this way and is proceesed accordingly
"0": {
        "tweetid": 873141672586117122, 
        "username": "Sameer", 
        "id": 2436645000, 
        "isCeleb": 0, 
        "Tweet": "RT @suhasinih: Press Club of India turns out in full force in support of Press Freedom in the country! #Dontshootthemessenger https://t.co/…", 
        "Tweet-tag": "ENGLISH", 
        "Word-level": {
            "RT": {
                "Label": "OTHER", 
                "Matrix": "EN"
            }, 
            "@suhasinih": {
                "Label": "OTHER", 
                "Matrix": "EN"
            }, 
            "Press": {
                "Label": "EN", 
                "Matrix": "EN"
            }, 
            "Club": {
                "Label": "EN", 
                "Matrix": "EN"
            }, 
            "of": {
                "Label": "EN", 
                "Matrix": "EN"
            }, 
            "India": {
                "Label": "NE", 
                "Matrix": "EN"
            }, 
            "turns": {
                "Label": "EN", 
                "Matrix": "EN"
            }, 
            "out": {
                "Label": "EN", 
                "Matrix": "EN"
            }, 
            "in": {
                "Label": "EN", 
                "Matrix": "EN"
            }, 
            "full": {
                "Label": "EN", 
                "Matrix": "EN"
            }, 
            "force": {
                "Label": "EN", 
                "Matrix": "EN"
            }, 
            "support": {
                "Label": "EN", 
                "Matrix": "EN"
            }, 
            "Freedom": {
                "Label": "EN", 
                "Matrix": "EN"
            }, 
            "the": {
                "Label": "EN", 
                "Matrix": "EN"
            }, 
            "country": {
                "Label": "EN", 
                "Matrix": "EN"
            }, 
            "#Dontshootthemessenger": {
                "Label": "OTHER", 
                "Matrix": "EN"
            }
        }
    },

"""




class user_word_tweet_tag(object):

    def __init__(self,user,word,tweet_type):
        self.user = user
        self.word = word
        self.tweet_type = tweet_type
        
    def __hash__(self):
        return hash((self.user,self.word, self.tweet_type))

    def __eq__(self, other):
        return (self.user,self.word, self.tweet_type) == (other.user,other.word, other.tweet_type)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)


class word_tweet_tag(object):

    def __init__(self,word,tweet_type):
        self.word = word
        self.tweet_type = tweet_type
        
    def __hash__(self):
        return hash((self.word, self.tweet_type))

    def __eq__(self, other):
        return (self.word, self.tweet_type) == (other.word, other.tweet_type)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)


@functools.total_ordering
class word_score(object):

    def __init__(self,word,score):
        self.word = word
        self.score = score
        
    def __eq__(self, other):
        return (self.word,self.score) == (other.word, other.score)

    def __lt__(self,other):
         return self.score < other.score

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

    def __repr__(self):
        if self.score !=0.0 :
            return ('[word=%s score=%lf] ' % (repr(self.word), float(repr(self.score) )  ) )
        else : 
            return ''


#all the dictionaries that use these words 
uur_follower = []
uur_celebrity= []

utr_follower = []
utr_celebrity= []

upr_follower = []
upr_celebrity = []
    
words_followers = []
words_celebrity=[]
    
        
#checks if word and  tweet tag is already used by the user or not 
#so as to count unique user
user_word_dict_celebrity={}
user_word_dict_follower={}

#counts unique users using word and tweet tag
tweet_word_dict_celebrity={}
tweet_word_dict_follower={}

#counts total tweets which use the word and tweet tag 
word_tweet_count_celebrity={}
word_tweet_count_follower={}
    
#counts how many phrases contain the word if it is L1 or L2
word_phrase_tag_celebrity={}
word_phrase_tag_follower={}

#phrases used in main function
words_with_tags = []
lang_of_phrases = []

################# Functions Definitions and other prototypes

def unique(a):

    """ return the list with duplicate elements removed """
    return list(set(a))


def intersect(a, b):

    """ return the intersection of two lists """
    c = unique(a)
    d = unique(b)

    e = list(set(c) & set(d))
    return len(e)

def union(a, b):

    """ return the union of two lists """
    c = unique(a)
    d = unique(b)

    e = list(set(c) | set(d))
    return len(e)

def mini(a,b) :
    """ return the union of two lists """
    c = unique(a)
    d = unique(b)
    
    e = min( len(c), len(d) )
    return e
    

def compute_jaccard_index(set1,set2):
    n = intersect(set1,set2)
     
    x = len(set1) + len(set2)-n 
    if x==0 :
        return 0.0
    else :
        return n / float(x)


# this will tokenize words and extract all nouns from it 
def process(dict_word_level):

    #get all words excluding the ones with "OTHER" tag    
    del words_with_tags[:]
    del lang_of_phrases[:]
    currentWord = 1 #indicates english
    alpha = ''
    counter = 1
    blipped=False

    #https://stackoverflow.com/questions/2287962/c-how-to-read-unicode-characters-hindi-script-for-e-g-using-c-or-is-th

    for key,value in dict_word_level.items() :
        
        # if its label is not other , we can extract it  ,only if it is not hindi
        if value['Label']!="OTHER" :
            if key[-1] in seperators and len(key)>1 :   
                continue
            else : 
                # if it is not a stop word , add it
                if key not in stop_words :
                    words_with_tags.append(key)
    
   

    return words_with_tags


    
def calculations():

    #now this is the extraction part 
    
    # This is the input file extraction part 
    #input_file  = open('output.json','w')

    #with open(path,) as f:
    #records=[json.loads(line) for line in f]

    

  ############## Now we extract words 
   
    #print(json_decode)
    print("\n\n\n\n")
    for key,values in json_decode.items() :

       
        
        
        

        #seperate the  other  labelled words from this  and also tag words with their Pos and then seperate Nominal Nouns from them
        nouns=process(values['Word-level'])
        
        value={}
        value['Word-level'] = values['Word-level']
        value['isCeleb']    = values['isCeleb']
        value['Tweet-tag']  = values['Tweet-tag']
        value['username']   = values['username']        
    

        #The one which contains list of nouns
        


        counter =0
        #now this words_with_tags is a list of strings 
        #these may contain phrases of hindi and english tweets in a subsequent manner 
        #now we do the pos tagging for the tweete using nltk kit
        

        if value['isCeleb']==0:    
    
            for word in nouns:
                
                

                # need to check word ,if the user has used this word in an tagged tweet or not
                # if he didnt , he should be added to that tag list as the unique user
                #who used this word 
                ###  This part is for uur calculation
                temp = user_word_tweet_tag(value['username'],word,value['Tweet-tag'])
                if temp not in user_word_dict_follower:
                    user_word_dict_follower[temp]=True


                    temp2= word_tweet_tag(word,value['Tweet-tag'])
                    #print(temp2.word)
                    #print(temp2.tweet_type)
                    #return

                    if temp2 not in tweet_word_dict_follower:  
                        tweet_word_dict_follower[temp2]=1
                    else:
                        tweet_word_dict_follower[temp2]=tweet_word_dict_follower[temp2]+1


#checks if the tweets and phrases are repeated is to be done

            
                #calculate how many tweets with this tweet tag contain 
                #this word . Used to calculate Utr 
                temp3 =word_tweet_tag(word,value['Tweet-tag'])
                if temp3 not in word_tweet_count_follower:
                    word_tweet_count_follower[temp3]=1
                else:
                    word_tweet_count_follower[temp3]+=1


                #calculate phrase for this 
                #if it is code shifted , then it must be either L1 or L2 word
                #get that tag and we can get the tag for the phrase
                #This is used for UPR calculation
                dict_word_level = value['Word-level']
                if word in dict_word_level:
                    val = dict_word_level[word]
                else :
                    continue

                tag=val['Label']
                if tag=='EN' :
                    tag='ENGLISH'
                elif tag=='HI' :
                    tag="HINDI"
                else :
                    continue

                #print(tag)                


                temp4 =word_tweet_tag(word,tag)
                if temp4 not in word_phrase_tag_follower:
                    word_phrase_tag_follower[temp4]=1
                else:
                    word_phrase_tag_follower[temp4]+=1

    
                #add this word to word-list
                if word not in words_followers:     
                    words_followers.append(word)    

        
            #now iterate all words and do processing
            for word in words_followers :

                x=x1=x2=0
                y=y1=0
                z=z1=z2=0

                temp= word_tweet_tag(word,'ENGLISH')        
                if temp in tweet_word_dict_follower :
                    x=tweet_word_dict_follower[temp]

                if temp in word_tweet_count_follower :
                    x1 = word_tweet_count_follower[temp]
                if temp in word_phrase_tag_follower :
                    x2 =word_phrase_tag_follower[temp]
            
                temp2= word_tweet_tag(word,'CME')        
                if temp2 in tweet_word_dict_follower:
                    y = tweet_word_dict_follower[temp2]
                if temp2 in word_tweet_count_follower:
                    y1= word_tweet_count_follower[temp2]        

                temp3= word_tweet_tag(word,'HINDI') 
                if temp3 in tweet_word_dict_follower:       
                    z =tweet_word_dict_follower[temp3]
                if temp3 in word_tweet_count_follower:
                    z1 = word_tweet_count_follower[temp3]       
                if temp3 in word_phrase_tag_follower:
                    z2 =word_phrase_tag_follower[temp3]
    
                if z==0: 
                    temp5 = word_score(word,0)
                else :
                    temp5 = word_score(word,(x+y)/z)
                uur_follower.append(temp5)
                
                if z1==0 :
                    temp6 = word_score(word,0)
                else :
                    temp6 = word_score(word,(x1+y1)/z1)                
                utr_follower.append(temp6)

                if z2==0 :
                    temp7 = word_score(word,0)
                else :
                    temp7 = word_score(word,(x2/z2))
                upr_follower.append(temp7)

    

        else:
    
            for word in nouns:

                # need to check word ,if the user has used this word in an tag or not
                # if he didnt , he should be added to that tag list as the unique user
                #who used this word 
                temp = user_word_tweet_tag(value['username'],word,value['Tweet-tag'])
                if temp not in user_word_dict_celebrity:

                    user_word_dict_celebrity[temp]=True
            
                    temp2=word_tweet_tag(word,value['Tweet-tag'])
                    if temp2 not in tweet_word_dict_celebrity:
                        tweet_word_dict_celebrity[temp2] =1
                    else:
                        tweet_word_dict_celebrity[temp2]+=1
            

#checks if the tweets and phrases are repeated is to be done

                
                #calculate how many tweets with this tweet tag contain 
                #this word
                temp3 =word_tweet_tag(word,value['Tweet-tag'])
                if temp3 not in word_tweet_count_celebrity:
                    word_tweet_count_celebrity[temp3]=1
                else:
                    word_tweet_count_celebrity[temp3]+=1



                #calculate phrase for this 
                #if it is code shifted , then it must be either L1 or L2 word
                #get that tag and we can get the tag for the phrase
        
                dict_word_level = value['Word-level']
                if word in dict_word_level :
                    val = dict_word_level[word]                
                else :
                    continue
                
                tag=val['Label']
                if tag=='EN' :
                    tag='ENGLISH'
                elif tag=='HI' :
                    tag="HINDI"
                else :
                    continue


                temp4 =word_tweet_tag(word,tag)
                if temp4 not in word_phrase_tag_celebrity:
                    word_phrase_tag_celebrity[temp4]=1
                else: 
                    word_phrase_tag_celebrity[temp4]+=1




                if word not in words_celebrity:     
                    words_celebrity.append(word)    


#these uur ,upr , utr need to be listed 

            for word in words_celebrity :

                x=x1=x2=0
                y=y1=0
                z=z1=z2=0

                temp= word_tweet_tag(word,'ENGLISH')        
                if temp in tweet_word_dict_celebrity:
                    x = tweet_word_dict_celebrity[temp]
                if temp in word_tweet_count_celebrity :
                    x1 = word_tweet_count_celebrity[temp]
                if temp in word_phrase_tag_celebrity:  
                    x2 =word_phrase_tag_celebrity[temp]
            
                temp2= word_tweet_tag(word,'CME')   
                if temp2 in tweet_word_dict_celebrity :     
                    y =tweet_word_dict_celebrity[temp2]
                if temp2 in word_tweet_count_celebrity:
                    y1= word_tweet_count_celebrity[temp2]        

                temp3= word_tweet_tag(word,'HINDI')        
                if temp3 in tweet_word_dict_celebrity :
                    z =tweet_word_dict_celebrity[temp3]
                if temp3 in word_tweet_count_celebrity :
                    z1 = word_tweet_count_celebrity[temp3]       
                if temp3 in word_phrase_tag_celebrity :
                    z2= word_phrase_tag_celebrity[temp3]   

                if z==0 :
                    temp5 =word_score(word,0)
                else :    
                    temp5 = word_score(word,(x+y)/z)
                uur_celebrity.append(temp5)
                
                if z1==0 :
                    temp6=word_score(word,0)
                else :
                    temp6 = word_score(word,(x1+y1)/z1)                
                utr_celebrity.append(temp6)

                if z2==0:
                    temp7 =word_score(word,0)
                else :
                    temp7 = word_score(word,(x2/z2))
                upr_celebrity.append(temp7)


    #order the uur , utr , upr as per the scores 
    print("celebrity words size %d "% len(words_celebrity) )
    print("followers words size %d " % len(words_followers) )


    uur_follower.sort()
    for x in uur_follower :
           print(x.word, end=' ') 
    print('\n\n\n\n\n')
    
    uur_celebrity.sort()
    for x in uur_celebrity :
            print(x.word,end=' ')
    print('\n\n\n\n\n')

    utr_follower.sort()
    for x in utr_follower :
            print(x.word,end=' ')
    print('\n\n\n\n\n')

    utr_celebrity.sort()
    for x in utr_celebrity :
            print(x.word,end=' ')
    print('\n\n\n\n\n')


    upr_follower.sort()
    for x in upr_follower :
            print(x.word,end=' ')
    print('\n\n\n\n\n')

    upr_celebrity.sort()
    for x in upr_celebrity :
            print(x.word,end=' ')
    print('\n\n\n\n\n')
    

    #jacobian coefficient
    a_int =intersect(words_followers,words_celebrity)    

    union_followers_celebrities = union(words_followers,words_celebrity)
    if union_followers_celebrities == 0 :
        jacobian_A =0
    else :
        jacobian_A = a_int / union_followers_celebrities
    
    mini_followers_celebrities = mini(words_followers,words_celebrity)
    if mini_followers_celebrities ==0 :
        jacobian_B =0
    else :
        jacobian_B = a_int /mini_followers_celebrities



    print("Jacobian_A is : ")
    print(jacobian_A)
    print('\n\n\n\n\n')
    print("Jacobian_B is : ")
    print(jacobian_B)

    #we calculate jacard Coefficient here 
    jacar = compute_jaccard_index(words_followers,words_celebrity)

    print('\n\n\n\n\n'+"Jacard_index is ")
    print(jacar)

    #spearman correlation -> need to be done by tomorrow
    uur_f = pd.DataFrame({'col':uur_follow})
    uur_c = pd.DataFrame({'col':uur_celeb})

    spearman_uur = pd.concat([uur_f,uur_c], axis=1).corr(method="spearman").iloc[len(uur_f):,:len(uur_c)]

    print('\n\n\n\n\n'+"Spearman correlation value between uur's is ")
    print(spearman_uur)


    utr_f = pd.DataFrame({'col':utr_follower})
    utr_c = pd.DataFrame({'col':utr_celebrity})

    spearman_utr = pd.concat([utr_f,utr_c], axis=1).corr(method="spearman").iloc[len(utr_f):,:len(utr_c)]

    print('\n\n\n\n\n'+"Spearman correlation value between utr's is ")
    print(spearman_utr)
    
    upr_f = pd.DataFrame({'col':upr_follower})
    upr_c = pd.DataFrame({'col':upr_celebrity})

    spearman_upr = pd.concat([upr_f,upr_c], axis=1).corr(method="spearman").iloc[len(upr_f):,:len(upr_c)]

    print('\n\n\n\n\n'+"Spearman correlation value between upr's is ")
    print(spearman_upr)


#nltk.download()
#print(tag_defining(-1))
calculations()
sys.stdout = orig_stdout
f.close()






