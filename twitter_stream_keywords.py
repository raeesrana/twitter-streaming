
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


access_token = "2780730379-oMGPWHcSkK4AP1k4tsKiZvTpQPLNVU6Rda5b9Z3"
access_token_secret = "8xAzSYmSeRwqb5DNd05C8a31YXy18mqpUpiRIE4aHXbSS"
consumer_key = "4HSfjqHoPp15I6OLWQJQdMAsI"
consumer_secret = "JXuHcNjrpmcbdQHmKHB8f4jCf7xjXy3kXdbRVIbWCdpz33yNsY"

class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True
    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    stream = Stream(auth, l)
    #search by keywords
    stream.filter(track=['comsats','d4interactive'])
    #search by twitter ID corresponding to the twitter user name / screen name

    # check user ID by username or screen name on the following Url : http://gettwitterid.com/
    # user ID for D4 Interactive : 4626158241

    stream.filter(follow=['4626158241'])


