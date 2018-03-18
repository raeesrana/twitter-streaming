from tweepy import OAuthHandler, API, StreamListener
from tweepy import Stream
import json
import logging


access_token = "2780730379-oMGPWHcSkK4AP1k4tsKiZvTpQPLNVU6Rda5b9Z3"
access_token_secret = "8xAzSYmSeRwqb5DNd05C8a31YXy18mqpUpiRIE4aHXbSS"
consumer_key = "4HSfjqHoPp15I6OLWQJQdMAsI"
consumer_secret = "JXuHcNjrpmcbdQHmKHB8f4jCf7xjXy3kXdbRVIbWCdpz33yNsY"

auth_handler = OAuthHandler(consumer_key, consumer_secret)
auth_handler.set_access_token(access_token, access_token_secret)

twitter_client = API(auth_handler)

logging.getLogger("main").setLevel(logging.INFO)


class PyStreamListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        try:
            publish = True

            if tweet.get('lang') and tweet.get('lang') != 'en':
                publish = False

            if publish:
                twitter_client.retweet(tweet['id'])
                logging.debug("RT: {}".format(tweet['text']))

        except Exception as ex:
            logging.error(ex)

        return True

    def on_error(self, status):
        print( status)



if __name__ == '__main__':
    listener = PyStreamListener()
    stream = Stream(auth_handler, listener)
    stream.filter(track=['d4interactive'])