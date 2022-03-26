#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 10:08:40 2018

@author: pippo
"""

import os
import tweepy
import unicodedata
import unicodecsv as csv
import json


def csv_writer(filename, to_write):
    headers = to_write.keys()
    file_exists = os.path.isfile(filename)

    with open(filename,'ab') as f:
        writer = csv.DictWriter(f, delimiter=',',fieldnames=headers)

        if not file_exists:
            writer.writeheader()

        writer.writerow(to_write)


def get_hashtags(entities):
        hashtags = ''
        try:
            for ht in entities['hashtags']:
                hashtags = hashtags+ '#'+normalize_text(ht['text'])+' '

        except:
            hashtags = 'None'

        return hashtags

def get_citations(entities):
    citations = ''
    try:
        for ct in entities['user_mentions']:
            citations = citations+'@'+ct['screen_name']+' '

    except:
        citations = 'None'
    return citations


def normalize_text( text):
    output = unicodedata.normalize('NFD', text).encode('ascii', 'ignore')
    return output


def assemble_tweet(single_tweet):
        tweet = {'author': normalize_text(single_tweet.author.name).decode('utf-8'),
         'aut_scrname': normalize_text(single_tweet.author.screen_name).decode('utf-8'),
         'tweet_id':str(single_tweet.id),
         'retweeted_status': '',
         'full_text': normalize_text(single_tweet.full_text).decode('utf-8'),
         'reply': single_tweet.in_reply_to_screen_name,
         'created_at': single_tweet.created_at,
         'retweet_count': single_tweet.retweet_count,
         'favorite_count': single_tweet.favorite_count,
         'hashtags': get_hashtags(single_tweet.entities),
         'citations' : get_citations(single_tweet.entities),
         'key' : searchQuery,
         'coordinates': single_tweet.coordinates,
         'source': single_tweet.source,
         'place': single_tweet.place,
         'geo': single_tweet.geo,
         'aut_location':single_tweet.author.location,
         'aut_statuses':single_tweet.author.statuses_count,
         'aut_friendcount':single_tweet.author.friends_count,
         'aut_followerscount':single_tweet.author.followers_count,
         'aut_verified':single_tweet.author.verified,
         'aut_created': single_tweet.author.created_at,
             }
        try:
            tweet['retweeted_status'] = normalize_text(single_tweet.retweeted_status.full_text).decode('utf-8')
        except:
            tweet['retweeted_status'] =''
        return tweet



terms =['mes']


for term in terms:

    searchQuery = term  # this is what we're searching for
    maxTweets = 1000000000 # Some arbitrary large number
    tweetsPerQry = 100  # this is the max the API permits
    filename = 'mes_2020.csv' # We'll store the tweets in a text file.
    lang='it'

    with open('twitter_credentials.json') as cred_data:
        info = json.load(cred_data)
        access_token = info['ACCESS_KEY']
        access_token_secret = info['ACCESS_SECRET']
        consumer_key =  info['CONSUMER_KEY']
        consumer_secret = info['CONSUMER_SECRET']

    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True,
    				   wait_on_rate_limit_notify=True, retry_count=3, retry_delay=5)


    # If results from a specific ID onwards are read, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = -1

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))


    while tweetCount < maxTweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery,lang=lang, count=tweetsPerQry,tweet_mode='extended')
                    else:
                        new_tweets = api.search(q=searchQuery,lang=lang, count=tweetsPerQry,tweet_mode='extended',
                                                since_id=sinceId)
                else:
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery,lang=lang, count=tweetsPerQry,tweet_mode='extended',
                                                max_id=str(max_id - 1))
                    else:
                        new_tweets = api.search(q=searchQuery,lang=lang, count=tweetsPerQry,tweet_mode='extended',
                                                max_id=str(max_id - 1),
                                                since_id=sinceId)
                if not new_tweets:
                    print("No more tweets found")
                    break
                for raw_tweet in new_tweets:
                    tweet = assemble_tweet(raw_tweet)
                    csv_writer(filename,tweet)


    #                f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
    #                        '\n')
                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break

    print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, filename))
