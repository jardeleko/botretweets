import tweepy
import time 

api_key = 'my_api_key***'
api_secret = 'my_api_key_secret***'
bearer_token = r'my_bearer***'
access_token = 'my_access_token***'
access_token_secret = 'my_token_secret***'

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

search_terms = ["UFFS", "uffs", "Universidade Federal da Fronteira Sul", "UNIVERSIDADE FEDERAL DA FRONTEIRA SUL"]

class MyStream(tweepy.StreamingClient):
  def on_connect(self):
    print ("Connected")
  
  def on_tweet(self, tweet):
    if tweet.referenced_tweets == None:
      print(tweet.text)
      client.retweet(tweet.id)
      client.like(tweet.id)
      time.sleep(0.5)
      
stream = MyStream(bearer_token=bearer_token)

for term in search_terms:
  stream.add_rules(tweepy.StreamRule(term)) 
  
stream.filter(tweet_fields=["referenced_tweets"])
