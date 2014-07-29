__author__ = 'Akshai Rajendran'

import tweepy
import cPickle as pickle
import nltk
import nltk.model
import nltk.probability
import random
import time
import os


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

def mention():
    #mentions list
    mentions = api.mentions_timeline()
    new_mentions = []

    #load all_mentions file, if it doesn't exist, create it
    #append new mentions to this file
    #recreate new mentions file with only new mentions
    if os.path.exists("all_mentions.p"):
        all_mentions = pickle.load(open("all_mentions.p","rb"))
        all_id = [mention.id for mention in all_mentions]
        for mention in mentions:
            if not mention.id in all_id:
                all_mentions.append(mention)
                new_mentions.append(mention)
            else:
                pass
        pickle.dump(all_mentions, open('all_mentions.p','wb'))
        pickle.dump(new_mentions,open('new_mentions.p','wb'))
    else:
        pickle.dump(mentions, open('all_mentions.p','wb'))
        pickle.dump(mentions, open('new_mentions.p','wb'))


