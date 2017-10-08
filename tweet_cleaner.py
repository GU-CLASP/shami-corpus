from alphabet_detector import AlphabetDetector
import preprocessor as tweet_processor
import re


emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)

arabic_diacritics = re.compile(""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)


def tokenize(s):
    return tokens_re.findall(s)


def normalize_arabic(text):
    text = remove_diacritics(text)
    # text = re.sub("[إأآا]", "ا", text)
    # text = re.sub("ى", "ي", text)
    # text = re.sub("ؤ", "ء", text)
    # text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text


def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', text)
    return text


def remove_repeating_char(text):
    # return re.sub(r'(.)\1+', r'\1', text)     # keep only 1 repeat
    return re.sub(r'(.)\1+', r'\1\1', text)     # keep 2 repeat


def remove_repeated_letters(word):
    # pre process
    return word


def get_repeated_letters(text):
    repeated_letters = list()
    # find letters
    for letter in text:
        pass
        # if letter is repeated :
        # repeated_letters.append(letter)
    repeated_letters = set(repeated_letters)
    return repeated_letters


def get_words(letter, words):
    selected_words = list()
    for word in words:
        if letter in word:
            selected_words.append(word)
    return set(selected_words)


def keep_only_arabic(words):
    ad = AlphabetDetector()
    tokens = [token for token in words if ad.is_arabic(token)]
    tweet = ' '.join(tokens)
    return tweet


def clean_tweet(tweet):
    tweet_processor.set_options(tweet_processor.OPT.URL,
                                tweet_processor.OPT.MENTION,
                                tweet_processor.OPT.HASHTAG,
                                tweet_processor.OPT.RESERVED,
                                tweet_processor.OPT.NUMBER
                                )
    tweet = tweet.lower()
    tweet = tweet_processor.clean(tweet)
    tweet = tweet.replace(" : ", " ")
    tweet = tweet.replace("\n", " ").strip()
    tokens = tokenize(tweet)
    tokens = [token if emoticon_re.search(token) else token for token in tokens]
    tweet = ' '.join(tokens)
    tweet = tweet.replace("/ ", " ")
    return tweet
