# a simple file to get count of number of cme, cmh, e, h tweets
# author: kaustubh
import pickle
import pandas as pd
#Tweet-tag, Tweet matters.

def count(pkl_file):
    tweets = pd.DataFrame(pickle.load(open(pkl_file, "rb")))
    print(tweets.groupby(['Tweet-tag']).size())

    print("Total tweets considered")
    print(tweets.groupby(['Tweet-tag']).size().sum())


if __name__ == '__main__':
    count('Data/nonCelebrity_F.pkl')
    # count('Data/Celebrity_F.pkl')