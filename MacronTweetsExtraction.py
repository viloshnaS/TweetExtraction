# General:
import tweepy           # To consume Twitter's API
import pandas as pd     # To handle data
import numpy as np      # For number computing

import csv
import json
from textblob import TextBlob
import re


def twitter_setup():

    consumer_key = 'zTFZjapZSzHgzIxRQ5cyqECYt'
    consumer_secret = 'GKxU8xmHEdc2531Jrf02fFuljU8FwAnHl5bX89Uzj3Wu6FBk5T'
    access_token = '920561539869966337-OGUtRuTfpUtpQbp6knq6uB23yoyWNZX'
    access_secret = 'duL0iMaDygMMXzKGwzmMk5i4VjWwlaCbiLmeEjfF9CnYI'

    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

def extractTweetsbyAccount(accountName):

    csvFile = open(accountName+'_tweets.csv', 'a', encoding='utf-8',newline='')
    csvWriter = csv.writer(csvFile)

    extractor = twitter_setup()

    alltweets = []

    # We create a tweet list as follows:
    new_tweets = extractor.user_timeline(screen_name=accountName, count=200, tweet_mode="extended")

    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    # print("Number of tweets extracted: {}.\n".format(len(tweets)))

    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = extractor.user_timeline(screen_name=accountName, count=200, tweet_mode="extended", max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    for tweet in alltweets:

        sentiment = get_tweet_sentiment(tweet)
        csvWriter.writerow(["'"+tweet.id_str,"'"+tweet.id_str,tweet.created_at, tweet.source, tweet.full_text
                               , tweet.retweet_count, tweet.favorite_count,sentiment])

def clean_tweet(tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w +:\ / \ / \S +)", " ", tweet).split())

def get_tweet_sentiment(tweet):

    analysis = TextBlob(tweet.full_text)
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


if __name__ == '__main__':
    extractTweetsbyAccount("EmmanuelMacron")