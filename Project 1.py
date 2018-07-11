#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 14:24:34 2018

@author: eamonnkeane
"""

#--------------------------------------- Part A ---------------------------------------#

from twython import TwythonStreamer
import sys
import json
from pprint import pprint
from collections import Counter
 
tweets = []
 
class MyStreamer(TwythonStreamer):
    '''our own subclass of TwythonStreamer'''
 
    # overriding
    def on_success(self, data):
        if 'lang' in data and data['lang'] == 'en':
            tweets.append(data)
            print('received tweet #', len(tweets), data['text'][:100])
 
        if len(tweets) >= 10000:
            self.store_json()
            self.disconnect()
 
    # overriding
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()
 
    def store_json(self):
        with open('tweet_stream_{}_{}.json'.format(keyword, len(tweets)), 'w') as f:
            json.dump(tweets, f, indent=4)
 
if __name__ == '__main__':
 
    CONSUMER_KEY = "JY9tYsOGKlvqmEE8tkyfxuFoV"
    CONSUMER_SECRET = "adWL6WvLGoB1l4FFSVlgixrnv2TQwR9ZFcCEvdc7wXejSpa8NK"
    ACCESS_TOKEN = "973673059205853184-iLb9xPmtcAlhfLG3EHgpzCYiSZ8JpzT"
    ACCESS_TOKEN_SECRET = "j9Ictf8VEMaFoENAnHeBb0bPYUgDWmmY1FGxnuhih1ybM"
 
    stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
 
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    else:
        keyword = 'Instagram'
 
    stream.statuses.filter(track=keyword)
    
    
    
#--------------------------------------- Part B ---------------------------------------#
    
# a.) What are the ten most popular words with and without stop words?
    # remove punctations
    
import nltk
import string
from twython import TwythonStreamer
import sys
import json
from pprint import pprint
from collections import Counter
        
def popular_words(filename):
    with open(filename, 'r') as infile:
     data = json.load(infile)
     
     type(data[0])
     data[0].keys()
           
    lst_words = [] 
    for tweet in data: 
        lst_words.extend(tweet['text'].split())
   
    
    words = nltk.word_tokenize(str(lst_words).lower())
    stopwords = nltk.corpus.stopwords.words('english')
    
    extra_words = ['https', 'rt', 'facebook']
    stopwords.extend(extra_words)
    
 
    words = [''.join(c for c in s if c not in string.punctuation) for s in words]
    # Source: https://stackoverflow.com/questions/4371231/removing-punctuation-from-python-list-items
    words = [s for s in words if s]
    
    no_stopwords = []
    for w in words:
        if w not in stopwords and len(w) > 1:  
           no_stopwords.append(w)
           
    with_stopwords = []
    for w in words:
        if w != "'" and len(w) > 1:  
           with_stopwords.append(w)
    
    print("With Stop Words")
    freq = nltk.FreqDist(with_stopwords)
    freq.plot(10)
    
    print("Without Stop Words")
    freq1 = nltk.FreqDist(no_stopwords)
    
    freq1.plot(10)
    
popular_words("/Users/eamonnkeane/Desktop/UBC/Year 3/COMM 337/Project 1/tweet_stream_Instagram_10000.json")
popular_words("/Users/eamonnkeane/Desktop/UBC/Year 3/COMM 337/Project 1/tweet_stream_Snapchat_10000.json")
 
    
# b.) What are the ten most popular hashtags (#hashtag)?

def popular_hashtags(filename):
    with open(filename, 'r') as infile:
     data = json.load(infile)
     
     type(data[0])
     data[0].keys()
     
     mention_list = []
     for tweet in data:
         mentions = tweet['entities']['hashtags']
         for ment in mentions:
             mention_list.append(ment['text'])
             
    c = Counter(mention_list)
    
    return c.most_common(10)
     
 
popular_hashtags("/Users/eamonnkeane/Desktop/UBC/Year 3/COMM 337/Project 1/tweet_stream_Instagram_10000.json")
popular_hashtags("/Users/eamonnkeane/Desktop/UBC/Year 3/COMM 337/Project 1/tweet_stream_Snapchat_10000.json")

# c.) What are the ten most frequently appearing usernames (@username)?

def frequent_usernames(filename):
    with open(filename, 'r') as infile:
     data = json.load(infile)
     
     type(data[0])
     data[0].keys()
     
     mention_list = []
     for tweet in data:
         mentions = tweet['entities']['user_mentions']
         for ment in mentions:
             mention_list.append(ment['screen_name'])
             
    c = Counter(mention_list)
    
    return c.most_common(10)
     
 
frequent_usernames("/Users/eamonnkeane/Desktop/UBC/Year 3/COMM 337/Project 1/tweet_stream_Instagram_10000.json")
frequent_usernames("/Users/eamonnkeane/Desktop/UBC/Year 3/COMM 337/Project 1/tweet_stream_Snapchat_10000.json")


# d. Who is the most frequently tweeting person about the keyword?

def frequent_tweeter(filename):
    with open(filename, 'r') as infile:
     data = json.load(infile)
     
     type(data[0])
     data[0].keys()
     
     mention_list = []
     for tweet in data:
         mention_list.append(tweet['user']['screen_name'])
             
    c = Counter(mention_list)
    
    return c.most_common(1)
     
 
frequent_tweeter("/Users/eamonnkeane/Desktop/UBC/Year 3/COMM 337/Project 1/tweet_stream_Instagram_10000.json")
frequent_tweeter("/Users/eamonnkeane/Desktop/UBC/Year 3/COMM 337/Project 1/tweet_stream_Snapchat_10000.json")

# e. Which is the most influential tweet? (Let’s define that influence is the sum
# of retweet count, reply count, and quote count.)

def most_influential_tweet(filename):
    with open(filename, 'r') as infile:
     data = json.load(infile)
     
     type(data[0])
     data[0].keys()
          
     counts = []
     t_text = []
     for tweet in data:
         
         retweet_count = tweet['retweet_count']
         reply_count = tweet['reply_count']
         quote_count = tweet['quote_count']
         tweet_text = tweet['text']
         
         
         counts.append(retweet_count + reply_count + quote_count)
         t_text.append(tweet_text)
         
     return t_text[counts.index(max(counts))]
         
         
most_influential_tweet("/Users/eamonnkeane/Desktop/UBC/Year 3/COMM 337/Project 1/tweet_stream_Instagram_100.json")
most_influential_tweet("/Users/eamonnkeane/Desktop/UBC/Year 3/COMM 337/Project 1/tweet_stream_Snapchat_100.json")



#--------------------------------------- Part C ---------------------------------------#

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
import numpy as np
import matplotlib.pyplot as plt
from os import path
from PIL import Image

def word_cloud(filename):
    with open(filename, 'r') as infile:
     data = json.load(infile)
     
     type(data[0])
     data[0].keys()
          
    lst_words = [] 
    for tweet in data: 
        lst_words.extend(tweet['text'].split())

    stopwords = nltk.corpus.stopwords.words('english')
    new_stop_words = ['https', 'might']
    stopwords.extend(new_stop_words)
    
    text = lst_words
    text2 = ''

    for word in text:
        if len(word) == 1 or word in stopwords:
            continue
        if word.startswith('https'):
            continue
        if word.startswith('RT'):
            continue
        text2 += ' {}'.format(word)
    
    wordcloud = WordCloud().generate(text2)

    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
    plt.show()
                
 
word_cloud("/Users/eamonnkeane/Desktop/UBC/Year 3/COMM 337/Project 1/tweet_stream_Instagram_100.json")
word_cloud("/Users/eamonnkeane/Desktop/UBC/Year 3/COMM 337/Project 1/tweet_stream_Snapchat_100.json")

#--------------------------------------- Part D ---------------------------------------#

# Using TextBlob, calculate the polarity and
#subjectivity scores for each tweet in the 10K+10K tweet corpus. Summarize the
#calculated scores with histograms using Matplotlib, where X-axis is the score and
#Y-axis is the tweet count in the score bin. Also, provide the average of the
#polarity and subjectivity scores.

def polarity_and_subjectivity_scores(filename):
    from textblob import TextBlob
    with open(filename) as infile:
        content = infile.read()
        sentences = content.split('\n')
    
    print(len(sentences), sentences[0], sentences[-1], sep="\n")
    sub_list = []
    pol_list = []
    for s in sentences:
        tb = TextBlob(s)
        sub_list.append(tb.sentiment.subjectivity)
        pol_list.append(tb.sentiment.polarity)
    import matplotlib.pyplot as plt
    
    plt.hist(sub_list, bins=10) #, normed=1, alpha=0.75)
    plt.xlabel('Subjectivity Score')
    plt.ylabel('Sentence Count')
    plt.grid(True)
    plt.savefig('subjectivity.pdf')
    plt.show()
    
    plt.hist(pol_list, bins=10) #, normed=1, alpha=0.75)
    plt.xlabel('Polarity Score')
    plt.ylabel('Sentence Count')
    plt.grid(True)
    plt.savefig('polarity.pdf')
    plt.show()


polarity_and_subjectivity_scores("/Users/eamonnkeane/Desktop/UBC/Year 3/COMM 337/Project 1/tweet_stream_Instagram_100.json")
polarity_and_subjectivity_scores("/Users/eamonnkeane/Desktop/UBC/Year 3/COMM 337/Project 1/tweet_stream_Snapchat_100.json")