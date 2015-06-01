#!/usr/bin/env python
import sys
import datetime
import yaml
import json

# convert a tweet in JSON format to a tab-separated format
def json2tab(tweet, retweets):
    try:
        # ignore re-tweets
        if (not retweets) and ("retweeted_status" in tweet):
            return None, None
        
        id_str = tweet["id_str"]
        
        # tweet text (escape double quotes, remove newlines and tabs)  
        text = tweet["text"]
        text = text.replace("\"","\\\"").replace("\n","")
        text = text.replace("\t"," ")
        
        # user  
        username = tweet["user"]["screen_name"]
        
        # geolocation
        if tweet['coordinates']:
            coordinates = tweet['coordinates']['coordinates']
        else:
            coordinates = None
        
        language = tweet['lang']

        # timestamp
        created_at = datetime.datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y") #  Wed Feb 08 22:49:40 +0000 2012
        timestamp = datetime.datetime.strftime(created_at, "%s")
        
        # write record in CSV format (if language is Italian)
        return "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(id_str, timestamp, username, language, coordinates, text.encode("utf-8")), tweet["id"]
            
    # tweet is unreadable
    except:
        sys.stderr.write("error parsing tweet\n")
        return None, None
        
# this module can also be called on the command line as a filter
if __name__ == "__main__":
    for line in sys.stdin:
        tweet = json.loads(line)
        tweet_tab, _ = json2tab(tweet, True)
        sys.stdout.write(tweet_tab)

