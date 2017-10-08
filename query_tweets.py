import argparse
import argcomplete
import json
import os
import time

from nltk.twitter import Query, credsfromfile

parser = argparse.ArgumentParser(description='collect tweets based on keywords')
parser.add_argument('-k', '--keywords-file', type=argparse.FileType(mode='r', encoding='utf-8'),
                    help='keywords or hashtags file. The file should contain one keyword/hashtag per line',
                    required=True)
parser.add_argument('-o', '--outfile', type=argparse.FileType(mode='a', encoding='utf-8'),
                    help='the output json file.', required=True)
parser.add_argument('-n', '--number', type=int,
                    help='the number of tweets that you want to collect', required=True)

# cwd = os.getcwd()
# set environmental variable
current_dir = os.path.dirname(os.path.realpath(__file__))
os.environ["TWITTER"] = current_dir + os.path.sep + "twitter-files"


def dump_tweets(tweets, json_writer):
    count = 0
    try:
        for tweet in tweets:
            json.dump(tweet, json_writer)
            json_writer.write("\n")
            count += 1
    except IOError as err:
        print("error: {0}".format(err))
    except BaseException as err:
        print("error: {0}".format(err))
    if count > 1:
        print("{} tweets found".format(count))
    else:
        print('no tweets found')


def collect_tweets(my_keyword, json_writer, stop_num):
    my_keyword = my_keyword.strip()
    print('finding tweets with {} keyword'.format(my_keyword))
    oauth = credsfromfile()
    client = Query(**oauth)
    tweets = client.search_tweets(keywords=my_keyword, limit=stop_num)
    dump_tweets(tweets, json_writer)


if __name__ == '__main__':
    args = parser.parse_args()
    argcomplete.autocomplete(parser)
    queries = args.keywords_file.read().splitlines()
    outfile = args.outfile
    number = args.number
    for query in queries:
        collect_tweets(my_keyword=query, json_writer=outfile, stop_num=number)