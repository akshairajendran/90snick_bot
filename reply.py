__author__ = 'Akshai Rajendran'

import tweepy
import cPickle as pickle
import nltk
import nltk.model
import nltk.probability
import random
import time
import os
import mentions


#open config file and create keys list from that
f = open('config.txt','r')
keys_list = [line[line.index(':')+1:len(line)].strip() for line in f]

#create api keys
consumer_key = keys_list[0]
consumer_secret = keys_list[1]
access_token = keys_list[2]
access_token_secret = keys_list[3]

#set username
user_name = keys_list[4]

#OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

#create api interface
api = tweepy.API(auth)

#############################################################
#include this at the beginning of all twitter access scripts#
#############################################################

#refresh mentions files
mentions.mention()

#load mentions files
all_mentions = pickle.load(open("all_mentions.p","rb"))
new_mentions = pickle.load(open("new_mentions.p","rb"))

text = nltk.word_tokenize("hello there")
print nltk.pos_tag(text)


