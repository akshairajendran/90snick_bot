__author__ = 'Akshai Rajendran'

import gen_tweet
import auto_follow
import time
import random

#infinite loop that sleeps for a random time between 4 and 8hrs
#tweets on average every 6 hours or 4 times a day
def run():
    while True:
        gen_tweet.tweet()
        auto_follow.follow()
        time.sleep(random.randint(7200,21600))


