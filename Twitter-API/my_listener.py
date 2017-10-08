import tweepy
import time
import os
import sys
import json


class MyListener(tweepy.StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, outfile, stop_at):
        self.stopAt = stop_at
        self.tweets_collected = 0
        self.tweets_streamed = 0
        time_string = time.strftime("%Y_%m_%d_%H%M%S")
        filename, ext = os.path.splitext(outfile)
        self.json_file_name = "{}_{}.json".format(filename, time_string)
        print("your output files are:")
        print(self.json_file_name)
        sys.stdout.write("\rTweets collected: {0}\t Tweets streamed: {1}".
                         format(self.tweets_collected, self.tweets_streamed))
        sys.stdout.flush()

    def on_status(self, status):
        return True

    def on_data(self, data):
        self.tweets_streamed += 1
        sys.stdout.write(
            "\rTweets collected: {0}\t Tweets streamed: {1}".format(self.tweets_collected, self.tweets_streamed))
        sys.stdout.flush()
        tweet = json.loads(data)
        with open(self.json_file_name, mode='a', encoding='utf-8') as json_writer:
            json_writer.write(data)
        self.tweets_collected += 1
        sys.stdout.write(
            "\rTweets collected: {0}\t Tweets streamed: {1}".format(self.tweets_collected, self.tweets_streamed))
        sys.stdout.flush()
        if self.tweets_collected >= self.stopAt:
            print("\ndone!")
            return False
        else:
            return True  # Don't kill the stream

    def on_error(self, status):
        print(status)
        if status == 420:
            return False # returning False in on_data disconnects the stream
        return True  # Don't kill the stream