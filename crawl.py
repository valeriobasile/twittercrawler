#!/usr/bin/env python

from optparse import OptionParser
from user import get_users_tweets
from stream import get_keywords_stream, get_sample_stream
import sys
import yaml
from requests_oauthlib import OAuth1

with open('config.yaml') as fd_conf:
    config = yaml.load(fd_conf)

# OAuth 1 authentication (insert your data here)
# OAuth 1 authentication
auth = OAuth1(config['consumer_key'], 
              config['consumer_secret'], 
              config['oauth_token'], 
              config['oauth_secret'])

# parse command line options
parser = OptionParser()
parser.add_option('-t',
                  '--type',
                  dest='crawl_type',
                  help='REQUIRED: type of crawl, either \'user\' (default), \'keyword\' or \'sample\'',
                  default='user')
parser.add_option('-f',
                  '--format',
                  dest='format',
                  help='output format, either \'raw\' (default) or \'tsv\'',
                  default='raw')
parser.add_option('-o',
                  '--output',
                  dest='output_file',
                  help='output file. Default: standard output',
                  default='stdout')

(options, args) = parser.parse_args()
if options.output_file != 'stdout':
    fd_out = open(options.output_file, 'w')
else:
    fd_out = sys.stdout

if options.crawl_type == 'user':
    get_users_tweets(auth, args, config, options.format, fd_out)
elif options.crawl_type == 'keyword':
    get_keywords_stream(auth, args, config, options.format, fd_out)
elif options.crawl_type == 'sample':
    get_sample_stream(auth, config, options.format, fd_out)
else:
    sys.stderr.write('unknown crawl type: {}\n'.format(options.crawl_type))
    sys.exit(1)
fd_out.close()
