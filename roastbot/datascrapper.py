import tweepy
import pandas as pd
import praw

class FetchData(object):

    #API KEYS
    twitter_api_key = "0YdBcutzCNYC9zFasuB6ok88G"
    twitter_api_key_secret = "f1TYaTTBJZuWtcghqVS3YlhkT4uWmYA2AACByHdo4hGKvDiZAU"

    reddit_api_key = "6pT8rJ3M7DJSiZ7fOxU0Eg"
    reddit_api_key_secret = "QVACoIC-HstocS-DTegj8URIsEfl6w"

    def fetch_twitter(api, api_secret, count):
        #Returns a list of tweet text fetched from twitter
        #Authentication
        auth = tweepy.OAuthHandler(api, api_secret)
        api = tweepy.API(auth=auth, wait_on_rate_limit=True)

        query = "#roasts -filter:retweets"

        tweets = tweepy.Cursor(api.search_tweets, 
                                q = query,
                                lang = "en").items(count)
        tweet_text = []

        for tweet in tweets:
            tweet_text.append(tweet.text)
        return tweet_text
    
    def fetch_reddit():

