import sys
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
import argparse
import api_keys
from my_listener import MyListener


parser = argparse.ArgumentParser(description='collect tweets based on following twitter users')
parser.add_argument('-u', '--users', type=argparse.FileType(mode='r', encoding='utf-8'),
                    help='twitter user ids file. Get ids from tweeterid.com',
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


def get_tweets(users, outfile, stop_num):
    auth, api = login()
    twitter_stream = Stream(auth, MyListener(outfile, stop_num))
    twitter_stream.filter(follow=users, async=True)


if __name__ == '__main__':
    args = parser.parse_args()
    users = args.users.readlines()
    stopAtNumber = args.number
    outfile = args.json
    get_tweets(users, outfile, stopAtNumber)


