Contributor  : Karthik 
NOTE: Celebrity1.txt can be downloaded from [google drive](https://drive.google.com/open?id=1-hNpevHej4qwXsrBuYjMCsVjXztmOLck).

              A word in some language , is said to be borrowed by Language2 , if it is used as a native language word
              instead of using the native language meaning .
              
                Ex : College is used as a native hindi word , instead of vidyalay . Hence , it is a borrowed word from English.
              
              We are interested in exploting different mesaures to eficiently predict , if a word is likely to be  borrowed in future .
              We use Hindi as L1 and English as L2 . We analyse the patterns of borrowed words from english to hindi 
              
              We use Social media sites like twitter . 
              We observe the patterns between the tweets of celebrities and their followers.
              
              
              We use three different metrics to analyse the words in their tweets .
              
              
               The different tags that a word can have are: L1, L2, NE (Named Entity) and Others. Based on the word level tag, 
               we also create a tweet level tag as follows: 
               
                     1. L1: Almosteveryword(> 90%)inthetweet is tagged as L1. 
                     2. L2: Almosteveryword(> 90%)inthetweet is tagged as L2.
                     3. CML1: Code-mixedtweetbutmajority(i.e., > 50%) of the words are tagged as L1. 
                     4. CML2: Code-mixedtweetbutmajority(i.e., > 50%) of the words are tagged as L2. 
                     5. CMEQ: Code-mixed tweet having very similar number of words tagged as L1 and L2 respectively. 
                     6. Code Switched: There is a trail of L1 words followed by a trail of L2 words or vice versa. 
                    
               Using the above classiﬁcation, we deﬁne the following metrics:
               
                    UniqueUserRatio(UUR)–TheUniqueUserRatio for word usage across languages is deﬁned as follows:
                    
                                    UC1 + UCML1
                        UUR(w) =   ---------------                    -(1)   
                                        UL2

                        where UL1 (UL2, UCML1)isthenumberofunique users who have used the word w in a L1 (L2, CML1) tweet at least once. 
                        
                    Unique Tweet Ratio (UTR) – The Unique Tweet Ratio for word usage across languages is deﬁned as follows:
                    
                                    TL1 + TCML1
                        UTR(w) =  ---------------                    -(2)
                                        TL2        

                        whereTL1 (TL2, TCML1)isthetotalnumberofL1 (L2, CML1) tweets which contain the word w.
                      
                   UniquePhraseRatio(UPR)–TheUniquePhrase Ratio for word usage across languages is deﬁned as follows: 
                                       
                                       PL1 
                          UPR(w) =  -------------                 -(3) 
                                       PL2
                          
                          where PL1 (PL2)isthenumberof L1 (L2)phrases which contain the word w. 
                          
             Note that unlike the deﬁnitions of UUR and UTR that exploit the word level language tags,
             the deﬁnition of UPR exploits the phrase level language tags.
             
             
            
            
            
            We then calculated Jacard Index and Spearman Correlation between 
              
                                          Intersection(A,B)
                  JacardIndex(A,B) =   ------------------------
                                            Union(A,B)
              
              
             
             We calculated Jacard Index between celebrities and followers words ( total) 
             
             We ordered sets of (word,metric) pairs of size 50,100,200,300,400 in increasing order of their metric value.
            
             We then Calculated Spearman correlation for metrics of followers and celebrities for all the sets .
             
             
              Files ::
              
                Source File     ::  LargeFilesOutput/prithvi/task2_final.py
                TotalResults    ::  LargeFilesOutput/prithvi/T2Output.txt
                SpearmanResults ::  LargeFilesOutput/prithvi/spearman_final.txt
                
Task2.py

Task Overview:
The code reads two sets of language, word tagged celebrities and followers tweets, calculates the utr, upr, uur values for the english words used in hindi contexts, and finally calculates the relevant jaccard and spearman coefficient. 

Language L1 is hindi.
Language L2 is english.

The tweets must be in json format as shown in the example below:

{
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
 
"1": ...    
}

The tweets must be word tagged and language(tweet) tagged.
2 Tweet sets: Celeb and followers tweets are read. 

The code either reads the celebrity and followers tweets from a text file in json format 
using the lines:

  fin = open('Celebrity1.txt', encoding = 'utf-8')
  tweetsCeleb = json.load(fin)

  fin = open('NonCelebrity1.txt', encoding = 'utf-8')
  tweetsFollow = json.load(fin)

or from pickle files using the lines:

  tweetsCelebFrame = pd.read_pickle('Celebrity_ALL.pkl')
    tweetsFollowFrame = pd.read_pickle('NonCelebrity_ALL.pkl') 

The dataframe read from pickle files are converted to dictionary data structure using generateTweetDicts() function:

    tweetsDict = generateTweetDicts(tweetsCelebFrame, tweetsFollowFrame)
    tweetsCeleb = tweetsDict['celeb']
    tweetsFollow = tweetsDict['follow']
  
Depending upon your tweets data one of these two methods mentioned above should be used and the other commented out.



-->Unique User Ratio (U U R) – The Unique User Ratio for
word usage across languages is defined as follows:
UUR(w) = (U(Hi) + U(CMH)) / U(En)  

where U(Hi) is the number of unique users who have used the
word w in a Hindi tweet at least once, U(En) is the number of
unique users who have used the word w in an English tweet
at least once and U(CMH) is the number of users who have
used the word w in a code-mixed Hindi tweet at least once.
Higher the value of U U R higher should be the likeliness of
the word w being borrowed.

-->Unique Tweet Ratio (U T R) – The Unique Tweet Ratio for
word usage across languages is defined as follows:
UTR(w) = (T(Hi) + T(CMH)) / T(En)

where T(Hi) is the total number of Hindi tweets which con-
tain the word w, T(En) is the total number of English tweets
which contain the word w and T(CMH) is the total number of
CMH tweets which contain the word w . Higher the value
of U T R higher should be the likeliness of the word w being
borrowed.

--> Unique Phrase Ratio (U P R) – The Unique Phrase Ratio for
word usage across languages is defined as follows:
UPR(w) = P(Hi) / P(En)

where P(Hi) is the number of Hindi phrases which contain the
word w, P(En) is the number of English phrases which con-
tain the word w. Note that unlike the definitions of U U R
and U T R that exploit the word level language tags, the defi-
nition of U P R exploits the phrase level language tags. Once
again, higher the value of U P R higher should be the likeli-
ness of the word w being borrowed.

utr, uur, upr values are calculated for the english noun words in hindi context.
Top n(n= 50,100,200) words with highest utr/uur/upr values are taken in both celebrity and followers tweets separately. Jaccard and spearmans coefficient are calculated for both the sets of tweets for all the three cases: utr,uur,upr.  


The function final(tweetsCeleb, tweetsFollow) calls the functions for calculating upr, utr, uur values, spearman, jaccard

final() calls the following:
  * removeRepeatedCelebTweets(tweetsCeleb) to remove repeated tweets from the celebrity tweets

  * updateCelebUsernames(tweetsCeleb) to get the username of the celebrity from the tweet string

  * utr(), upr(), uur() separately for the followers and celebrity tweets which returns a dictionary utrCeleb/uprCeleb/uurCeleb and the corresponding dictionaries for followers.
  * The dictionary's keys represents the word and its values having the utr/uur/upr values


