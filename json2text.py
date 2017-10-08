import argparse
import json
import os
import sys

import tweet_cleaner

parser = argparse.ArgumentParser(description='extract tweet texts from json')
parser.add_argument('-i', '--json-dir', type=str,
                    help='tweets json directory', required=True)
parser.add_argument('-o', '--out-dir', type=str,
                    help='the output directory.', required=True)
parser.add_argument('--exclude-redundant',
                    help='exclude redundant tweets', action='store_true')
parser.add_argument('--include-id',
                    help='include tweet id', action='store_true')
parser.add_argument('-n', '--normalize',
                    help='normalize text', action='store_true')
parser.add_argument('--remove-repeated-letters',
                    help='removed repeated letters (+2 consecutive) from text', action='store_true')
parser.add_argument('--keep-only-arabic',
                    help='only keep Arabic words', action='store_true')


def extract_tweets_from_json(json_reader, text_writer):
    json_tweets = json_reader.readlines()
    print('tweets in json file: {} tweets'.format(len(json_tweets)))
    tweets_list = list()
    extracted_tweets_count = 0
    if args.include_id:
        text_writer.write("id\ttweet\n")
    for json_tweet in json_tweets:
        try:
            if json_tweet:
                # load it as Python dict
                tweet = json.loads(json_tweet)
                tid = tweet['id']
                text = tweet['text']
                text = tweet_cleaner.clean_tweet(text)
                if args.normalize:
                    text = tweet_cleaner.normalize_arabic(text)
                if args.remove_repeated_letters:
                    text = tweet_cleaner.remove_repeating_char(text)
                if args.keep_only_arabic:
                    text = tweet_cleaner.keep_only_arabic(text.split())
                if len(text.split()) > 2:
                    if args.exclude_redundant:
                        if text not in tweets_list:
                            tweets_list.append(text)
                            if args.include_id:
                                text_writer.write(str(tid) + "\t" + text + "\n")
                                # print('id:{}'.format(str(tid)))
                                # print('text:', text)
                                # print('tweet:', tweet['text'])
                                # input("press any key...")
                            else:
                                text_writer.write(text + "\n")
                            extracted_tweets_count += 1
                    else:
                        if args.include_id:
                            text_writer.write(str(tid) + "\t" + text + "\n")
                        else:
                            text_writer.write(text + "\n")
                        extracted_tweets_count += 1
        except json.decoder.JSONDecodeError as error:
            pass
        except UnicodeDecodeError as error:
            pass
    print('extracted tweets: {} tweets'.format(extracted_tweets_count))


def extract_tweets_from_json_files(json_dir, text_dir):
    for json_file in os.listdir(json_dir):
        if json_file.endswith('.json'):
            json_file = os.path.join(json_dir, json_file)
            filename, ext = os.path.splitext(json_file)
            text_file = os.path.join(text_dir, os.path.basename(filename) + '.txt')
            with open(json_file, mode='r', encoding='utf-8') as json_reader, open(text_file, mode='w',
                                                                                  encoding='utf-8') as text_writer:
                print('extract tweets from {}'.format(json_file))
                extract_tweets_from_json(json_reader, text_writer)
                print('tweets extracted to {}'.format(text_file))
                print('--------------------')


if __name__ == '__main__':
    args = parser.parse_args()
    json_dir = args.json_dir
    out_dir = args.out_dir
    if json_dir == out_dir:
        print('error: input and output directories can not be the same.')
        sys.exit(-1)
    extract_tweets_from_json_files(json_dir, out_dir)
