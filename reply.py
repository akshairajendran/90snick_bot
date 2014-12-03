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

#set username and bot name
user_name = keys_list[4]
bot_name = keys_list[5]

#OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

#create api interface
api = tweepy.API(auth)

#############################################################
#include this at the beginning of all twitter access scripts#
#############################################################

#reply_tweet function
def reply_tweet(text,users):
    #load tweets list and move random 2 tweets to front
    #this is a workaround to randomize starting state of Markov
    all_tweets = pickle.load(open("all_tweets.p","rb"))
    all_tweets.insert(0,text)
    random_index = random.randint(20,len(all_tweets)-1)
    all_tweets.insert(1,all_tweets.pop(random_index))
    random_index2 = random.randint(20,len(all_tweets)-1)
    all_tweets.insert(2,all_tweets.pop(random_index2))

    #tokenize
    tokens = []
    for string in all_tweets:
        tokens.append(nltk.word_tokenize(string))
    #we have a list of list of tokens and now we flatten that to one list
    tokens = [item for sublist in tokens for item in sublist]


    #create tweet model from tokens
    tweet_model = nltk.model.NgramModel(3,tokens)

    #create random tweet length and create tweet
    tweet_len = random.randint(5,15)
    tweet = " ".join(tweet_model.generate(tweet_len))

    #punctuation will have a space before it so remove that
    punctuation = [",", "!", ".", "'", "n't", ":", ";","&",")","?"]
    for punct in punctuation:
        tweet = tweet.replace(" " + punct, punct)
    tweet = tweet.replace("# ","#")
    tweet = users + " " + tweet

    #tweet!!
    api.update_status(tweet)

def reply():
    #refresh mentions files
    mentions.mention()

    #load mentions files
    all_mentions = pickle.load(open("all_mentions.p","rb"))
    new_mentions = pickle.load(open("new_mentions.p","rb"))
    if len(new_mentions) == 0:
        return
    else:
        #load up most recent mention, tokenize and split it
        #grab all users mentioned in mention
        #if the mention author is the bot itself, ignore
        #if the mention author isn't already in list, add him/her
        mention = new_mentions[-1].text
        mention_author = "@" + new_mentions[-1].author.screen_name
        mention_token = nltk.word_tokenize(mention)
        mention_split = mention.split()
        mention_pos = nltk.pos_tag(mention_split)
        mention_users = [word for word in mention_split if '@' in word]
        if new_mentions[-1].author.screen_name == bot_name:
            return
        else:
            pass
        for user in mention_users:
                if mention_author in user:
                    mention_users.remove(user)
                elif mention_author.lower() in user:
                    mention_users.remove(user)
                else:
                    pass

        #find verbs, proper nouns and pronouns in mention
        mention_verbs = [tuple[0] for tuple in mention_pos if tuple[1] == 'VB' or tuple[1] == 'VBD' or tuple[1] == 'VBG' or tuple[1] == 'VBN' or tuple[1] == 'VBP' or tuple[1] == 'VBZ']
        mention_proper_nouns = [tuple[0] for tuple in mention_pos if tuple[1] == 'NNP' or tuple[1] == 'NNPS']
        mention_pronouns = [tuple[0] for tuple in mention_pos if tuple[1] == 'PRP']
        mention_nouns = [tuple[0] for tuple in mention_pos if tuple[1] == 'NN' or tuple[1] == 'NNS']
        mention_all_nouns = mention_proper_nouns + mention_pronouns + mention_nouns
        mention_all_nouns = [word for word in mention_all_nouns if not '@' in word]

        #check if we've got verbs and nouns
        #if we do then generate first two words of tweet and users to tweet at
        #pass these into the actual tweeting function
        mention_binary = [len(mention_verbs) != 0, len(mention_all_nouns) != 0]
        if all(condition is True for condition in mention_binary):
            users = " ".join(mention_users)
            text = random.choice(mention_all_nouns) + ' ' + random.choice(mention_verbs)
            reply_tweet(text, users)
        else:
            return





