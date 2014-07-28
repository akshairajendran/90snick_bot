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

def tweet():
    #load tweets list and move random 2 tweets to front
    #this is a workaround to randomize starting state of Markov
    all_tweets = pickle.load(open("all_tweets.p","rb"))
    random_index = random.randint(20,len(all_tweets)-1)
    all_tweets.insert(0,all_tweets.pop(random_index))
    random_index2 = random.randint(20,len(all_tweets)-1)
    all_tweets.insert(1,all_tweets.pop(random_index2))

    #tokenize
    tokens = []
    for string in all_tweets:
        tokens.append(nltk.word_tokenize(string))
    #we have a list of list of tokens and now we flatten that to one list
    tokens = [item for sublist in tokens for item in sublist]


    #create tweet model from tokens
    tweet_model = nltk.model.NgramModel(2,tokens)

    #create random tweet length and create tweet
    tweet_len = random.randint(5,15)
    tweet = " ".join(tweet_model.generate(tweet_len))

    #punctuation will have a space before it so remove that
    punctuation = [",", "!", ".", "'", "n't", ":", ";","&",")","?"]
    for punct in punctuation:
        tweet = tweet.replace(" " + punct, punct)
    tweet = tweet.replace("# ","#")

    #tweet!!
    api.update_status(tweet)


