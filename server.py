import os
import re
import time 
import tweepy
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


api_key = os.environ.get("api_key")
api_secret = os.environ.get("api_secret")
bearer_token = os.environ.get("bearer_token")
access_token = os.environ.get("access_token")
access_token_secret = os.environ.get("access_token_secret")

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)
regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

search_terms = ["UFFS", "uffs", "Universidade Federal da Fronteira Sul", "UNIVERSIDADE FEDERAL DA FRONTEIRA SUL", "UFFSEDU"]

class MyStream(tweepy.StreamingClient):
  def on_connect(self):
    print ("Connected")
  
  def on_tweet(self, tweet):
    control = 0
    if tweet.referenced_tweets == None:
      tmp = tweet.text.split(" ")
      if(len(tmp) >= 3):
        for x in tmp:
          if(x.lower() =='en' or x.lower() =='caliente' 
            or x.lower() == 'con' or x.lower() == 'del'
            or x.lower() == 'tan' or x.lower() == 'ganas'
            or x.lower() == 'otra' or x.lower() == 'otro'
            or x.lower() == 'otras' or x.lower() == 'otros'
            or x.lower() == 'ustedes' or x.lower() == 'vosotros'
            or x.lower() == 'nosotros' or x.lower() == 'tambien'
            or x.lower() == 'hacer' or x.lower() == 'hoy'
            or x.lower() == 'novio' or x.lower() == 'novia' 
            or x.lower() == 'coño' or x.lower() == 'pinza' 
            or x.lower() == 'aun' or x.lower() == 'y' 
            or x.lower() == 'los' or x.lower() == 'las' 
            or x.lower() == 'lo' or x.lower() == 'la' 
            or x.lower() == 'cojer' or x.lower() == 'caña'
            or x.lower() == 'no' or x.lower() == 'un'
            or x.lower() == 'si' or x.lower() == 'sí'
            or x.lower() == 'el' or x.lower() == 'tan' 
            or x.lower() == 'muy' or x.lower() == 'una'):
            control = 1
        if(control == 0):
          if re.findall(regex, tweet.text):
            print(tweet.text)
            control = 1
            print('pulltaria')
          else:
            client.retweet(tweet.id)
            client.like(tweet.id)
            control = 0
        else:
          print('ignored content')
      else:
        control = 1
        print('payload error')
      time.sleep(0.5)

stream = MyStream(bearer_token=bearer_token)
for term in search_terms:
  stream.add_rules(tweepy.StreamRule(term)) 

stream.filter(tweet_fields=["referenced_tweets"])
stream.filter(place_fields=['brazil','55'])