__author__ = 'Akshai Rajendran'

import tweepy
import cPickle as pickle
import nltk
import nltk.model
import nltk.probability
import random


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

def follow():
    #create me and my followers and friends lists
    me = api.me()
    followers = api.followers_ids(me.name)
    friends = api.friends_ids(me.name)

    #if my friends/followers is less than .7, find the people whole follow me
    #that I don't follow, and select one of them randomly to follow
    if float(me.friends_count)/float(me.followers_count) < .7:
        potential_friend = [follower for follower in followers if follower not in friends]
        new_friend = random.choice(potential_friend)
        api.create_friendship(new_friend)
    else:
        pass

