__author__ = 'arajendran'
import tweepy
import cPickle as pickle

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

#set username
user_name = keys_list[4]

#start getting tweets
new_tweets = api.user_timeline(screen_name = user_name, count=200)
all_tweets = [tweets for tweets in new_tweets]

#set id for oldest tweet
oldest = all_tweets[-1].id - 1

#start loop to get beyond 200
while len(new_tweets) > 0:
    new_tweets = api.user_timeline(screen_name = user_name, count=200,max_id = oldest)
    all_tweets.extend(new_tweets)
    oldest = all_tweets[-1].id - 1

#create list with just tweet text
all_tweets_txt = [tweets.text for tweets in all_tweets]

#remove tags from all_tweets_txt
all_tweets_txt_notag = []
for i in range(len(all_tweets_txt)):
    new_string = " ".join(word for word in all_tweets_txt[i].split() if not '@' in word)
    all_tweets_txt_notag.append(new_string)

#dump list to pickle db
pickle.dump(all_tweets_txt_notag, open('all_tweets.p','wb'))