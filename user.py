#!/usr/bin/env python
import sys
import simplejson as json
import requests
from time import sleep
from process import json2tab

# retrieve 'count' tweets from the Twitter API
def get_tweets(auth, screen_name, config, max_id=None):
    args = {
        'include_entities':'true',
        'include_rts':'true',
        'screen_name':screen_name,
        'count':config['count'],
        'max_id':max_id}
    response = requests.get(config['url_user'], params=args, auth=auth, stream=True)
    return response.json()

# iteratively downloads batches of tweets from the user screen_name until
# there are no more tweet
def get_users_tweets(auth, screen_names, config, output_format, output_file):
    for screen_name in screen_names:
        sys.stderr.write("retrieving tweets for screen name: {0}\n".format(screen_name))
        retrieved = 0
        tweets = []
        max_id = None
        end = False
        # loop until there's no more tweet
        while not end:
            # tweets come from the most recent to the oldest, thus at each iteration
            # we update max_id
            new_tweets = get_tweets(auth, screen_name, config, max_id)
            if len(new_tweets) == 0:
                end = True
            for tweet in new_tweets:
                tweet_tab, last_id = json2tab(tweet)                
                if tweet_tab:
                    # write out the tweet
                    if output_format == 'tsv':
                        output_file.write(tweet_tab)
                    else:
                        output_file.write(json.dumps(tweet))
                    retrieved += 1
                    max_id = last_id - 1
                else:
                    end = True

            # let's not put too much pressure on the API
            sleep(config['wait'])
        sys.stderr.write("retrieved {0} tweets\n".format(retrieved))


