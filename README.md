# getusertweets
A script to download all the available tweets from a Twitter user

run as:

$ python getusertweets.py <username>

The output is written on the standard output in tab-separated format, one tweet per line. The fields are:

- tweet ID
- timestamp in UNIX epoch (seconds since 1/1/1970)
- username
- geographic coordinates, "None" is not provided
- text of the tweet

## configuration

At the moment the configuration is hard-coded at the top of the script.
You will need a valid Twitter developer API key to make it work. See https://dev.twitter.com/streaming/overview
