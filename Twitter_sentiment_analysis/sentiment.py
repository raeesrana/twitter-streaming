import sys
import csv
import tweepy
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')
import json
from collections import Counter
from aylienapiclient import textapi
from tkinter import *
from tkinter import messagebox
import tkinter.scrolledtext as tkst
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

if sys.version_info[0] < 3:
    input = raw_input


def launch():
    left.delete(1.0, END)
    query = entry_person.get()
    number = int(entry_tweet.get())

    hist = open("history.csv", "w")
    global history_number
    history_number = history_number + 1
    hist.write(str(history_number))
    hist.close()

    ## Twitter credentials enter details from developer website.
    consumer_key = "pAd4Av8mFrYbl8cbZ6p9h3IaA"
    consumer_secret = "BmeLouZrCKwQkC9KKNe89k45bY3keCSatrfOIHG1GXKib7OpFi"
    access_token = "883033980-sVGLhoF0sZxmtxKihKDfylJeDByf0QFkNHifgPZr"
    access_token_secret = "WBluOosuLm5w3OKrL1GHNEzk96NWZ6nRkuD8h7u88YHls"

    ## AYLIEN credentials from the website, get the ID and Key.
    application_id = "781305f2"
    application_key = "fcdad30830e8a1ac7f26089a218b617a"

    ## set up an instance of Tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    ## set up an instance of the AYLIEN Text API
    client = textapi.Client(application_id, application_key)

    ## search Twitter for something that interests you
    # query = input("What subject do you want to analyze for this example? \n")
    # number = input("How many Tweets do you want to analyze? \n")

    results = api.search(
        lang="en",
        q=query,
        count=number,
        result_type="mixed"
    )

    print("--- Gathered Tweets \n")

    ## open a csv file to store the Tweets and their sentiment
    file_name = 'Sentiment_Analysis_of_{}_Tweets_About_{}.csv'.format(number, query)

    with open(file_name, 'w') as csvfile:
        csv_writer = csv.DictWriter(
            f=csvfile,
            fieldnames=["Tweet", "Sentiment", "Place", "Time", "Likes", "Retweets"]
        )
        csv_writer.writeheader()

        print("--- Opened a CSV file to store the results of your sentiment analysis... \n")

        ## tidy up the Tweets and send each to the AYLIEN Text API
        for c, result in enumerate(results, start=1):
            tweet = result.text
            tweet_json = result._json
            tweet_place = ""

            try:
                tweet_place = tweet_json['place']['full_name'] + "," + tweet_json['place']['country']
            except:
                tweet_place = tweet_json['place']

            tweet_created_at = ""

            try:
                tweet_created_at = tweet_json["created_at"]
            except:
                tweet_created_at = ""

            tweet_co_ords = ""
            try:
                tweet_co_ords = "lon:" + tweet_json["coordinates"][0] + "lat:" + tweet_json["coordinates"][1]
                tweet_co_ords = tweet_json["place"]["id"]
            except:
                tweet_co_ords = ""

            retweet_count = tweet_json["retweet_count"]
            likes_count = tweet_json["favorite_count"]
            # /////////////////////////////////////////////
            tweet_hashtags = ""
            try:
                tweet_hashtags = tweet_json["entities"]["hashtags"]
                hashtags_holder = ""
                for hashtag in tweet_hashtags:
                    hashtag_string = hashtag["text"] + ","
                    hashtags_holder += hashtag_string
                tweet_hashtags = hashtags_holder
            except:
                tweet_hashtags = ""
            # //////////////////////////////////////////////////

            tidy_tweet = tweet.strip().encode('ascii', 'ignore')

            if len(tweet) == 0:
                print('Empty Tweet')
                continue

            response = client.Sentiment({'text': tidy_tweet})
            csv_writer.writerow({
                'Tweet': response['text'],
                'Sentiment': response['polarity'],
                'Place': tweet_place,
                'Time': tweet_created_at,
                'Likes': likes_count,
                'Retweets': retweet_count

            })
            left.insert(INSERT, "Tweet: {} \n".format(response['text']))
            left.insert(INSERT, "Sentiment: {} \n".format(response['polarity']))
            left.insert(INSERT, "Place: {} \n".format(tweet_place))
            left.insert(INSERT, "Likes: {} \n".format(likes_count))
            left.insert(INSERT, "Retweets: {} \n\n\n".format(retweet_count))

            print("Analyzed Tweet {}".format(c))

    ## count the data in the Sentiment column of the CSV file
    with open(file_name, 'r') as data:
        counter = Counter()
        for row in csv.DictReader(data):
            counter[row['Sentiment']] += 1

        positive = counter['positive']
        negative = counter['negative']
        neutral = counter['neutral']

    ## declare the variables for the pie chart, using the Counter variables for "sizes"
    colors = ['green', 'red', 'grey']
    sizes = [positive, negative, neutral]
    labels = 'Positive', 'Negative', 'Neutral'

    fig = plt.Figure()
    ax = fig.add_axes((0, 0, 1, 1), frameon=False)

    ## use matplotlib to plot the chart
    ax.pie(
        x=sizes,
        shadow=True,
        colors=colors,
        labels=labels,
        startangle=90
    )

    # plt.show()
    right_text.config(text="Sentiment of {} Tweets about {}".format(number, query))
    right_text.config(font=("Courier", 16))
    canvas = FigureCanvasTkAgg(fig, master=right_draw)
    canvas.show()
    canvas.get_tk_widget().pack()
    canvas.draw()

    hist_details = open(str(history_number) + ".txt", "w")
    hist_details.write(
        "Keyword used : " + query + " || with a number of tweets : " + str(number) + "\n\n" + left.get(1.0, END))


def history_launch():
    hist_tk = Tk()
    hist_tk.minsize(600, 350)
    cont_pann = PanedWindow(hist_tk, orient=HORIZONTAL)
    cont_pann.pack(fill=BOTH, expand=1)
    cont = tkst.ScrolledText(hist_tk)
    cont_pann.add(cont)
    content_ = ""
    for i in range(1, history_number + 1):
        content_ = content_ + "-------------------------\n"
        with open(str(i) + ".txt", "r") as fp:
            line = fp.readline()
            while line:
                content_ = content_ + line
                line = fp.readline()
    print(content_)
    cont.insert(INSERT, content_)
    hist_tk.mainloop()
    # messagebox.showinfo("History" , content_)


history_file = open("history.csv", "r")
global history_number
history_number = int(history_file.readline())
print(history_number)
global root
root = Tk()
root.minsize(960, 500)

main = PanedWindow(root, orient=VERTICAL)
main.pack(fill=BOTH, expand=1)

top = PanedWindow(main, orient=HORIZONTAL)

history_but = Button(main, text='History', command=history_launch)

global person
person = Label(main, text="Person to analyse ")
global entry_person
entry_person = Entry(main, width=20)
num_tweet = Label(main, text="Number of tweets ")
entry_tweet = Entry(main, width=20)
search_but = Button(main, text='SEARCH', command=launch)  # , command=onok)
top.add(history_but)
top.add(person)
top.add(entry_person)
top.add(num_tweet)
top.add(entry_tweet)
top.add(search_but)

main.add(top)

bottom = PanedWindow(main)
global left
left = tkst.ScrolledText(bottom, width=60)
global right
right = PanedWindow(bottom, orient=VERTICAL)

global right_text
right_text = Label(main, text="")

global right_draw
right_draw = Canvas(right, width=40, height=100)
right_draw.pack()

right.add(right_text)
right.add(right_draw)

bottom.add(left)
bottom.add(right)
main.add(bottom)

root.mainloop()
