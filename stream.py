#!/usr/bin/env python

import requests
from requests_oauthlib import OAuth1
import json
import sys
import yaml

def get_keywords_stream(keywords, output_format, output_file):
    with open('config.yaml') as fd_conf:
        config = yaml.load(fd_conf)

    # OAuth 1 authentication
    auth = OAuth1(config['consumer_key'], 
                  config['consumer_secret'], 
                  config['oauth_token'], 
                  config['oauth_secret'])

    # POST data: list of keywords to search
    data = {'track':['vita','Roma','forza','alla','quanto','amore','Milano','Italia','fare','grazie','della','anche','periodo','bene','scuola','dopo','tutto','ancora','tutti','fatto']}
    response = requests.post(config['url_filter'], data=data, auth=auth, stream=True)

    for line in response.iter_lines():
        if line:
            print json.dumps(json.loads(line))
