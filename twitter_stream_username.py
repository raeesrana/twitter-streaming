import tweepy #twitter streaming API
import pandas as pd  # data structures and data analysis tool - used to analyze tweets data
import numpy as np   # used for numeric computation and data storage and display
from IPython.display import display     # dynamic display terminal
import matplotlib.pyplot as plt
import sys

# twitter API credentials
access_token = "2780730379-oMGPWHcSkK4AP1k4tsKiZvTpQPLNVU6Rda5b9Z3"
access_token_secret = "8xAzSYmSeRwqb5DNd05C8a31YXy18mqpUpiRIE4aHXbSS"
consumer_key = "4HSfjqHoPp15I6OLWQJQdMAsI"
consumer_secret = "JXuHcNjrpmcbdQHmKHB8f4jCf7xjXy3kXdbRVIbWCdpz33yNsY"

def twitter_setup():

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  # authorize API credentials using OAuthHandler from tweepy api
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)       # initialize and return API
    return api

extract = twitter_setup()

tweets = extract.user_timeline(screen_name = "Saaqi__",count = 20)   # take twitter user screen name and minimum tweet count to extract
print("number of tweets extracted: {}.\n".format(len(tweets)))   # display the count of extracted tweets - count = 20

print("5 recent tweets:\n")
for tweet in tweets [:5]:      # display the last 5 tweets in the array (which are the most recent 5 tweets)
    print(tweet.text)
    print()

# use pandas framework to extract tweets data such as the tweet text, ID, length, date created etc.
# store the extracted data in numpy array to display as a table
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns = ['Tweets'])

data['Tweets'] = np.array([tweet.text for tweet in tweets])
data['len']  = np.array([len(tweet.text) for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
display(data.head(10))      # display the first 10 entries


#if __name__ == "__main__":


