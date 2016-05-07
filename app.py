from __future__ import absolute_import, print_function

import os
import json
import time

from flask import Flask, render_template
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from config import Config
from utils import *

consumer_key = Config.get("TWITTER_CONSUMER_KEY")
consumer_secret = Config.get("TWITTER_CONSUMER_SECRET")
access_token = Config.get("TWITTER_ACCESS_TOKEN")
access_token_secret = Config.get("TWITTER_ACCESS_TOKEN_SECRET")

articles = []


class LikedTweetsListener(StreamListener):
    def on_data(self, data):
        print('On data called...')
        tweet = json.loads(data)

        if 'event' not in tweet:
            print('event not in tweet')
            return True

        event = tweet['event']
        print('event: %s' % event)

        if event != 'favorite':
            print('event not favorite')
            return True

        print(tweet)
        liked_tweet = tweet['target_object']
        liked_tweet_text = liked_tweet['text']
        story_url = extract_url(liked_tweet)
        if story_url:
            article = extract_article(story_url)
            if article:
                article['story_url'] = story_url
                article['liked_on'] = time.time()
                articles.append(article)

        return True

    def on_error(self, status):
        print('Error status received: {0}'.format(status))


# flask stuff
app = Flask(__name__)


@app.route('/')
def index():
    print('articles available: %s' % articles)
    return render_template(
        'index.html',
        articles=sorted(
            articles, key=lambda article: article['liked_on'], reverse=True)
        )


if __name__ == '__main__':
    l = LikedTweetsListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.userstream(async=True)

    app.run(debug=True, host='0.0.0.0')
