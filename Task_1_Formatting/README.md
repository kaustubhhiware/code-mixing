## Formatting the Cleaned Data

### Input Format
The cleaned data contains two lines for each tweet in the raw data.
The first line contains the tweet-id and the tweet.
The second line contains the word level tagging of the tweet based on the language(EN or HI).

Language tagging is done by using the Microsoft language tagger.

### Output Format
The data is formatted and stored in the form of dataframe in a pickle file.If needed, this dataframe can be simply converted into json format using an inbuilt function.

The dataframe contains the following columns:
* tweetid    : Contains the id of the tweet
* isCeleb    : Contains 0 or 1 to indicate whether the person is a celebrity or not.
* Tweet      : Contains the original tweet.
* Tweet-tag  : Contains the tweet-tag of the tweet.
* Word-level : Contains the word-tag and context-tag for each of the words in the tweet

The "Word-level" is in turn a dataframe with words of the tweet as indexes and 'word-tag' and 'context-tag' as columns.

The value of isCeleb is decided based on whether the tweet is a normal tweet or a retweet.
### Tweet tag
The tweets in the data set are classified into six different categories.

* En: Tweet contains 90% or more English words.
* Hi: Tweet contains 90% or more Hindi words.
* CMH: Code-mixed tweet but majority(>50%) words in Hindi.
* CME: Code-mixed tweet but majority(>50%) words in English.
* CMEQ: English and Hindi words almost same number of occurrences.
* CS: (Code-switched) Trail of En / Hi words followed by trail of Hi / En words.
* OTHER : Tweet contains only mentions or URLS.

The tweet-tag for a tweet is assigned based on the word-level tags in the tweet.

### Code-Mixed and Code-Switched Classification
The word tags of the tweet are taken into an array or a list. Then, the number of positions at which the word-tag changes is calculated.

* If the number of changes is one, then the tweet is code-switched tweet.
* If the number of changes is greater than one, then the tweet is code-mixed tweet. 

### Context tag
The context tag for each of the words in a tweet is assigned based on the tweet-tag of the tweet.

* If the tweet tag is either 'EN' or 'CME', then the context tag is 'EN' for all the words in the tweet.
* If the tweet tag is either 'HI' or 'CMH', then the context tag is 'HI' for all the words in the tweet.
* If the tweet tag is 'CMEQ', then the context tag is 'O' for all the words in the tweet.
* If the tweet tag is 'CS', then the context tag is same as the word tag.

### Named Entity Recognition
The named entities in a tweet can be extracted by tagging parts-of-speech using the Natural Language Toolkit.

The word-tags of these words are changed from 'EN' or 'HI' to 'NE' in the dataframe.

### Conversion of dataframe into json format
If required, the dataframe in the pickle file can be converted into json format.


### Files
```
* Source File: Formatting Cleaned data/task_1_final.py
* Conversion into json format: Formatting Cleaned data/dataframe2json.py
```

