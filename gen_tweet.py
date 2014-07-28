__author__ = 'Akshai Rajendran'

import tweepy
import cPickle as pickle
import nltk
import nltk.util
import nltk.model

#open config file and create keys list from that
f = open('config.txt','r')
keys_list = [line[line.index(':')+1:len(line)].strip() for line in f]

#create api keys
consumer_key = keys_list[0]
consumer_secret = keys_list[1]
access_token = keys_list[2]
access_token_secret = keys_list[3]

#OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

#create api interface
api = tweepy.API(auth)

#############################################################
#include this at the beginning of all twitter access scripts#
#############################################################

#load tweets list
all_tweets = pickle.load(open("all_tweets.p","rb"))

tokens = []
#tokenize
for string in all_tweets:
    tokens.append(nltk.word_tokenize(string))
tokens = [item for sublist in tokens for item in sublist]
print tokens

#trainer from tokens?
trainer = nltk.model.NgramModel(3,tokens).generate(5)
