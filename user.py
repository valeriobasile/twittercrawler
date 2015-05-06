#!/usr/bin/env python
import sys
import simplejson as json
import requests
from requests_oauthlib import OAuth1
import datetime
from time import sleep
import yaml

with open('config.yaml') as fd_conf:
    config = yaml.load(fd_conf)

# OAuth 1 authentication (insert your data here)
# OAuth 1 authentication
auth = OAuth1(config['consumer_key'], 
              config['consumer_secret'], 
              config['oauth_token'], 
              config['oauth_secret'])

# convert a tweet in JSON format to a tab-separated format
def json2tab(tweet):
    try:
        # ignore re-tweets
        if "retweeted_status" in tweet:
            return None, None
        
        id_str = tweet["id_str"]
        
        # tweet text (escape double quotes, remove newlines)  
        text = tweet["text"]
        text = text.replace("\"","\\\"").replace("\n","")
        
        # user (escape double quotes, remove newlines)  
        username = tweet["user"]["screen_name"]
        
        # geolocation
        if tweet['coordinates']:
            coordinates = tweet['coordinates']['coordinates']
        else:
            coordinates = None
        
        # timestamp
        created_at = datetime.datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y") #  Wed Feb 08 22:49:40 +0000 2012
        timestamp = datetime.datetime.strftime(created_at, "%s")
        
        # write record in CSV format (if language is Italian)
        return "{0}\t{1}\t{2}\t{3}\t{4}\n".format(id_str, timestamp, username, coordinates, text.encode("utf-8")), tweet["id"]
            
    # tweet is unreadable
    except:
        sys.stderr.write("error parsing tweet\n")
        return None, None
        
# retrieve 'count' tweets from the Twitter API
def getTweets(screen_name, count, max_id=None):
    args = {
        'include_entities':'true',
        'include_rts':'true',
        'screen_name':screen_name,
        'count':count,
        'max_id':max_id}
    response = requests.get(config['url_user'], params=args, auth=auth, stream=True)
    return response.json()

# iteratively downloads batches of tweets from the user screen_name until
# there are no more tweet
def getTweetsByScreenname(screen_name):
    sys.stderr.write("retrieving tweets for screen name: {0}\n".format(screen_name))
    retrieved = 0
    tweets = []
    max_id = None
    end = False
    # loop until there's no more tweet
    while not end:
        # tweets come from the most recent to the oldest, thus at each iteration
        # we update max_id
        new_tweets = getTweets(screen_name, config['count'], max_id)
        if len(new_tweets) == 0:
            end = True
        for tweet in new_tweets:
            tweet_tab, last_id = json2tab(tweet)
            if tweet_tab:
                # write out the tweet
                sys.stdout.write(tweet_tab)
                retrieved += 1
                max_id = last_id - 1
            else:
                end = True

        # let's not put too much pressure on the API
        sleep(config['wait'])
    sys.stderr.write("retrieved {0} tweets\n".format(retrieved))

if __name__=="__main__":
    getTweetsByScreenname(sys.argv[1])

