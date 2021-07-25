#!/usr/bin/env python
import sys
import datetime
import json


# Convert a Tweet in JSON format to a tab-separated format
def json2tab(tweet, retweets):
    try:
        # Ignore Retweets
        if (not retweets) and ("retweeted_status" in tweet):
            return None, None

        id_str = tweet["id_str"]

        # tweet text (escape double quotes, remove newlines and tabs)
        if "extended_tweet" in tweet:
            text = tweet["extended_tweet"]["full_text"]
        else:
            text = tweet["full_text"]
        text = text.replace("\"", "\\\"").replace("\n", "")
        text = text.replace("\t", " ")

        # User
        username = tweet["user"]["screen_name"]

        # Location
        if tweet['coordinates']:
            coordinates = tweet['coordinates']['coordinates']
        else:
            coordinates = None

        language = tweet['lang']

        # Timestamp
        timestamp = datetime.datetime.strptime(
                    tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y") \
            .timestamp()

        # Write record in CSV format (if language is Italian)
        return "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(id_str, timestamp,
            username, language, coordinates, text.encode("utf-8")), tweet["id"]

    # Tweet is unreadable
    except Exception as e:
        sys.stderr.write("error parsing tweet\n")
        print(e)
        return None, None


# This module can also be called on the command line as a filter
if __name__ == "__main__":
    for line in sys.stdin:
        tweet = json.loads(line)
        tweet_tab, _ = json2tab(tweet, True)
        sys.stdout.write(tweet_tab)
