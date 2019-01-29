import csv
import json
import nltk
from nltk.corpus import stopwords
from collections import Counter
import string
import operator
from nltk.tokenize import RegexpTokenizer
import time

punctuation = list(string.punctuation)
text_file = open("french_stopwords.txt", "r")
stop = stopwords.words('french') + text_file.read().split(',') + punctuation + ['the','for','der','it','their','they','to','rt', 'and','our','of','we','in','is','via', 'https', 'plus', 'co','abo', 'les', 'a', 'la', 'le', 'ou']
count_all = Counter()
tokenizer = RegexpTokenizer(r'\w+')

tweet_file = open("tweet_text.txt", 'r', encoding='utf-8',newline='')
tweet = tweet_file.readline()

while (tweet.strip() != ""):
        terms = tokenizer.tokenize(tweet)
        word_count = Counter(w.title() for w in terms if w.lower() not in stop)
        count_all.update(word_count)
        tweet = tweet_file.readline()
        print(tweet)

print(count_all)