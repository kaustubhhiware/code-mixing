Contributor  : Karthik 

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
                
                
                  
                   
             
              
              
              
