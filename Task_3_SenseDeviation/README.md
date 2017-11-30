# Task 3: Sense Deviation

We aim to identify the senses in which English words are used in Hindi context on Social media.

NOTE: complex-sm can be downloaded from [google drive](https://drive.google.com/open?id=1NbLyKQbr5McBXH-FU0PmVq0Md7UGv3QW).

## Separating English nouns for training

For this, we shall first distinguish English nouns in English context and English nouns in Hindi context.
We shall do this by appending an '$' to every english word in Hindi context.

So, _Aaj mein film dekhne gya_ becomes _Aaj mein film$ dekhne gya_.

This will be done using `TweetsCeleb.py` which takes as input the tweets from celebrities and followers.
The modified tweets are stored in `tweets_celeb.pkl` and `tweets_follow.pkl`. The modified tweets
can be found at `socialMixedTweets.txt`.


## Representing words in Social media

 Once we separate English nouns in English and Hindi contexts, we need to represent words like _film_ and
 _film$_ differently according to their occurences in Social media.

 We will be using **gensim** module in python, the code for which is available on `social_w2v.py`.
 The word2vec model is stored in `complex-sm` and `naive-sm`.

 For `naive-sm`, a word requires to be appearing atleast 5 times to be accounted for. However, for `complex-sm`,
 we are considering all words. To speeden the process, we use multiple workers (24).


## Getting possible senses for English nouns

Using `englishWords.py`, we will be extracting English nouns from our tweet dataset. The nouns are stored in
`eng_nouns.txt`. A total of 6846 nouns were found.

The further handling for English nouns is done in [Eng2Hin](Eng2Hin).

For a sample word, say _film_, we identify synonyms for the word using wordnet. Now, we shall translate
every synonym to Hindi using google translate programmatically. All these translated Hindi words are then
assigned as possible Hindi senses for the word _film_.

The code for this is available on `EN2HItranslation.py`, the output for which is `EN2HIdict.pkl`.

Now, to test our sense analysis, we shall separate a target test set of 57 words ('thing', 'way', 'woman', 'press', 'wrong', 'well','matter', 'reason', 'question', 'guy', 'moment', 'week', 'luck',  'president', 'body', 'job', 'car', 'god', 'gift', 'status',  'university', 'lyrics', 'road', 'politics', 'parliament',  'review', 'scene', 'seat', 'film', 'degree','people', 'play', 'house', 'service', 'rest', 'boy', 'month', 'money', 'cool',   'development', 'group', 'friend', 'day', 'performance', 'school', 'blue', 'room', 'interview', 'share', 'request','traffic', 'college', 'star', 'class', 'superstar', 'petrol', 'uncle').

These words were found using the work from [All that is English may be Hindi: Enhancing language identification through
automatic ranking of likeliness of word borrowing in social media](https://arxiv.org/abs/1707.08446).

The above words were found comparing the frequency of an English noun in English newspaper corpus and Hindi newspaper corpus.
For each word, we identify the ratio
```
            [ F(English, word)   ]
        log[ ------------------ ]
            [   F(Hindi, word)   ]
```

Based on this ratio, we chose 30 words with extremely high and extremely low ratio, and 27 words with moderate ratio.

To separate training from test set, we separated those 57 test words using `pickle2dict.py`. The corrected training set
for English nouns is stored at `EN2HIdict-trimmed.pkl`.


## Visualising social-media vector

Word2Vec is building word projections (embeddings) in a latent space of N dimensions, (N being the size of the word vectors obtained). 
Obtained coordinates of all words in 300 dimensions.
 
Used Dimensionality reduction (TSNE) to visualise vectors in 2 dimensions.
 
Stored these points and plotted using Matplotlib

Reference: https://www.tensorflow.org/tutorials/word2vec and https://radimrehurek.com/gensim/models/word2vec.html 


## Checking similarity within social-media Dataset

To evaluate how similar _film_ and _film$_, we evaluate the similarity using word2vec of these 2 words.
However, this is only an intermediate result. The score is computed by `dollar_similarity.py` and stored at `dollar_scores.txt`.


## Finding actual senses appearing in Social Media context

We identified 2238 English nouns which appear in Hindi context. For each word _film$_, we will evaluate what possible
senses this word appears in our tweet dataset. This involves manual tagging for 2 words.

Two students were asked to tag all 2238 words as `user1-tags.txt` and `user2-tags.txt`. We found the interannotator agreement (Cohen's kappa value) as 0.633. Now, to merge those 2 tags, we use `kappa_merge.py`, which additionally calculates kappa.
The output is stored both as pickles and txt files at `SM2HIdict-test.pkl`, `SM2HIdict-train.pkl`
and corresponding text files.

Along with this, we also try to analyse how many senses a word is borrowed into. We found 154 words
have a singular sense in our social-media context and 71 words have multiple senses. After manual tagging,
we procure `one_meanings.txt` and `many-meanings.txt`, which then uses `hindi-meaning.py` to generate
`one-hindi.txt` and `many-hindi.txt` which provides us these statistics.


## Transforming vectors to Hindi vector space

To properly compare words like _film$_ in social media, and _film_ in conventional English, we shall
be transforming vectors in social-media vectorspace and English vectorspace to Hindi vectorspace.

For this, we require Hindi word2vec pre-trained model `hi.bin` which can be downloaded from
[Kyubyong/wordvectors](https://github.com/Kyubyong/wordvectors#pre-trained-models) and English
word2vec model (Google news) from [here](https://github.com/mmihaltz/word2vec-GoogleNews-vectors).
`hi/hiwords.txt` is the complete list of words in our Hindi model.

Using `proc.py`, and proctruses, we shall be storing the transformation matrix from
English to Hindi as `W-EN-train.pkl` and the matrix from Social media to Hindi
as `W-SM-train.pkl`. A sample run for this process can be found at `T.txt`.

![https://imgur.com/obkTiYE](https://imgur.com/obkTiYE.png)

Using the method described in [Hamilton’s (2016): Diachronic Word Embeddings Reveal Statistical Laws of Semantic Change](https://aclanthology.info/pdf/P/P16/P16-1141.pdf), we use proctruses method for minimising the aforementioned error.
Xi refers to English / social media vector and Zi is Hindi vector, where W is the transformation matrix.


## Obtaining results

The organised results can be found on [this Google sheet](https://docs.google.com/spreadsheets/d/1Is0Q2JT_B2GADr4Mfa2qEZckEjZrHVAh2v7hDhpFCM4).

NOTE: The cosine similarity in gensim can be negative. Please refer to 
[this stackoverflow answer](https://stackoverflow.com/questions/42381902/interpreting-negative-word2vec-similarity-from-gensim).

First we shall transform social media vector for _film$_ and english vector for _film_.

We are trying to analyse 3 kinds of results.

### Sense similarity

For an English noun E which appears in Hindi context (E$), we consider the possible senses (H1, H2, H3, ..).

For every possible sense, we consider the cosine similarity of (E, H1) and (E$, H1). Using this, we were able
to find if, for a certain sense, it is closer to E or E$.

For a sense Hx, if  **cosine(Hx, E$) > cosine(Hx, E)**, it means when an English word appears
in Hindi context, it is more likely to mean in the sense of Hx.

The code for this is `res1.py` and `res1-union.py`, which outputs `res1.txt` and `res1-union.txt` respectively.

### Vector similarity

Now, for each English noun E which appears in Hindi context (E$), we consider the similarity of E and E$.
If cosine(E, E$) is high, it means that the senses of E and E$ are closer to each other.

This is possible when E does not have multiple senses. Example, _movie_ and _movie$_ will have higher
cosine similarity than _film_ and _film$_, because movie has very few possible senses, however
film can mean cinema, strip, photographic film, etc.

The code for vector similarity is `result_cos_sim.py`, the output for which is at `result2-cos-similarity.txt`

### Nearest neighbours

For every English noun E in Hindi context E$, we take its 10 nearest neighbors in the Hindi vectorspace.

The code is at `result_neighbors.py`, which outputs `result3-neighbors.txt`.


## Obtaining frequency specific data (redundant)

Using `frequency_target.py`, we tried to obtain the count for each English word in Hindi context and
in English context in our social media. The count and ratio of log (Fe / Fh) can be found in `frequency-count.txt`.
However, these words were not used ultimately since the results for these parts were not compatible with
newspaper corpus, so we dismissed the selected words.
