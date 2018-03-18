import tweepy
import csv #Import csv
import os
import sys
# Consumer keys and access tokens, used for OAuth
access_token = "2780730379-oMGPWHcSkK4AP1k4tsKiZvTpQPLNVU6Rda5b9Z3"
access_token_secret = "8xAzSYmSeRwqb5DNd05C8a31YXy18mqpUpiRIE4aHXbSS"
consumer_key = "4HSfjqHoPp15I6OLWQJQdMAsI"
consumer_secret = "JXuHcNjrpmcbdQHmKHB8f4jCf7xjXy3kXdbRVIbWCdpz33yNsY"

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)
# Open/Create a file to append data

users = []
user_name = sys.argv[1:]
for user_name in users:
    user = api.get_user(screen_name = user_name)
    print([user.screen_name, user.id, user.followers_count, user.description.encode('utf-8')])
