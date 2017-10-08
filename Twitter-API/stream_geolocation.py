import argparse
import sys

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream

import api_keys
from my_listener import MyListener

parser = argparse.ArgumentParser(description='collect tweets based on geographic location')
parser.add_argument('-l', '--geo-locations', type=str,
                    help='geo location coordinates from http://boundingbox.klokantech.com '
                         'copy and past using csv option',
                    required=True)
parser.add_argument('-j', '--json', type=str,
                    help='the the json output file.', required=True)
parser.add_argument('-n', '--number', type=int,
                    help='the number of tweets that you want to collect', required=True)


def login():
    if api_keys.consumer_key == '' or api_keys.consumer_secret == '' \
            or api_keys.access_token == '' or api_keys.access_secret == '':
        print("API key not found. Please check api_keys.py file")
        sys.exit(-1)
    auth = OAuthHandler(api_keys.consumer_key, api_keys.consumer_secret)
    auth.set_access_token(api_keys.access_token, api_keys.access_secret)
    api = tweepy.API(auth)
    return auth, api


def get_tweets(my_locations, outfile, stop_num):
    auth, api = login()
    twitter_stream = Stream(auth, MyListener(outfile, stop_num))
    # Bounding boxes for geo-locations
    # http://boundingbox.klokantech.com/
    # Online-Tool to create boxes (c+p as raw CSV):
    twitter_stream.filter(locations=my_locations, async=True)


if __name__ == '__main__':
    args = parser.parse_args()
    my_locations = [float(x) for x in args.geo_locations.split(',')]
    stopAtNumber = args.number
    outfile = args.json
    get_tweets(my_locations, outfile, stopAtNumber)