# twittercrawler 

A script to download all the available tweets from a
Twitter user or from a list of keywords.

## Setup

First of all, install the dependencies:

    simplejson
    requests
    requests_oauthlib
    yaml

Then, fill in the authentication info in *config.yaml*. The config
file also contains a few default values for the script.

## Running

To download all* the tweets from a list of users run as:

    crawl.py -t user username1 [username2 ...]

To search for keywords in the stream of tweets run as:

    crawl.py -t keyword keyword1 [keyword2 ...]

By default, the output is written on the standard output in the JSON
format returned by the Twitter API. If the **-f tsv** option is
provided, the output is written on the standard output in
tab-separated format, one tweet per line. The fields are:

- tweet ID
- timestamp in UNIX epoch (seconds since 1/1/1970)
- username
- language code
- geographic coordinates, "None" is not provided
- text of the tweet

The **-o output_file** option specifies a file to write the output. If
existing, the file will be overwritten.

The **filter.py** module also acts as a command line filter, reading a 
JSON output file on its standard input and writing out the corresponding 
tab-separated format.

## Disclaimer

The copyright of the tweets belongs to Twitter. Please refer to
Twitter's [Terms of Service](https://twitter.com/tos?lang=en) for
information about what you can and cannot do with the tweets.

There is no guarantee that **all** the tweets relevant to the search
will be retrieved. The number of resulting tweets may be influenced by
the Twitter API's rate limit, the network infrastructure, etc.
