import tweepy
import json 
from pushbullet import Pushbullet
import os
from os import environ

NickEh30_ID = "2733210014"
#NickEh30_ID = "1375069720089612292"
Push_api_key = environ['Push_api_key']

#Add your credentials here
twitter_keys = {
        'consumer_key':        environ['consumer_key'],
        'consumer_secret':     environ['consumer_secret'],
        'access_token_key':    environ['access_token_key'],
        'access_token_secret': environ['access_token_secret']
    }

#Setup access to API
auth = tweepy.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])

api = tweepy.API(auth)
pb = Pushbullet(Push_api_key)

def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if(from_creator(status)):
            print(status.text)
            push = pb.push_note("New Tweet", status.text)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

#filters only tweets from NickEh30
myStream.filter(follow=[NickEh30_ID], is_async=True)

