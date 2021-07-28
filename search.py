#!/usr/bin/env python
import sys
import json
from time import sleep
from process import json2tab
from requests import get


# Retrieve 'count' Tweets from the Twitter API
def get_tweets(auth, query, config, max_id=None):
    args = {
        'include_entities': 'true',
        'q': query,
        'count': config['count'],
        'max_id': max_id,
        'tweet_mode': 'extended'}
    response = get(
        config['url_search'], params=args, auth=auth, stream=True)
    return response.json()


# Iteratively downloads batches of Tweets from the user screen_name until
# there are no more Tweets
def get_search_tweets(auth, queries, config, output_format, output_file):
    for query in queries:
        sys.stderr.write("retrieving tweets for query: {0}\n".format(query))
        retrieved = 0
        max_id = None
        end = False

        # Loop until there's no more Tweets
        while not end:
            # Tweets come from the most recent to the oldest,
            # thus at each iteration we update max_id
            new_tweets = get_tweets(auth, query, config, max_id)["statuses"]
            if len(new_tweets) == 0:
                end = True
            for tweet in new_tweets:
                tweet_tab, last_id = json2tab(tweet, config['retweets'])
                if tweet_tab:
                    # write out the tweet
                    if output_format == 'tsv':
                        output_file.write(tweet_tab)
                    else:
                        output_file.write(json.dumps(tweet))
                        output_file.write('\n')
                    retrieved += 1
                    max_id = last_id - 1
                else:
                    end = True

            # let's not put too much pressure on the API
            sleep(config['wait'])
        sys.stderr.write("retrieved {0} tweets\n".format(retrieved))
