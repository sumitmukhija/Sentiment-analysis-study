"""File to be invoked after data collection
"""
import time
import preprocessor as p
from langdetect import detect
from profanity_check import predict
import os
import glob
import json
import pandas as pd
import datetime as dt


CURRENT_WORKDIR = os.getcwd()

class Preprocess(object):

    def __init__(self):
        self.veteran_stats = dict()
        self.civilian_stats = dict()
        self.cleaned_veteran_tweets = list()
        self.cleaned_civilian_tweets = list()
        self.list_of_pages = list()

    def pre_process_data(self, tweet, data_type="soldiers"):
        lang = 'na'
        try:
            lang = detect(tweet)
        except:
            print("Can't detect a lang")
        finally:
            if lang == 'en' or lang == 'na':  #Only parsing English tweets
                self.check_profanity(tweet, data_type=data_type)
                self.aggregate_stats_from_tweet(tweet, data_type=data_type)
                p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION)
                cleaned_tweet = p.clean(tweet)
                cleaned_tweet = cleaned_tweet.replace("#", "")
                number_of_words = len(cleaned_tweet)
                if data_type == "soldiers":
                    self.veteran_stats['words'] = number_of_words if self.veteran_stats.get('words') is None else (self.veteran_stats['words'] + number_of_words)
                    self.cleaned_veteran_tweets.append(cleaned_tweet)
                else:
                    self.civilian_stats['words'] = number_of_words if self.civilian_stats.get(
                        'words') is None else (self.civilian_stats['words'] + number_of_words)
                    self.cleaned_civilian_tweets.append(cleaned_tweet)

    def check_profanity(self, tweet, data_type):
        if predict([tweet]) == 1:
            if data_type == 'soldiers':
                self.veteran_stats['curses'] = 1 if self.veteran_stats.get(
                    'curses') is None else(self.veteran_stats['curses'] + 1)
            else:
                self.civilian_stats['curses'] = 1 if self.civilian_stats.get(
                    'curses') is None else(self.civilian_stats['curses'] + 1)

    def aggregate_stats_from_df(self, vet_df, civ_df):
        self.veteran_stats['retweets'] = vet_df.retweets_count.sum()
        self.veteran_stats['replies'] = vet_df.replies_count.sum()
        self.veteran_stats['likes'] = vet_df.likes_count.sum()
        self.civilian_stats['retweets'] = civ_df.retweets_count.sum()
        self.civilian_stats['replies'] = civ_df.replies_count.sum()
        self.civilian_stats['likes'] = civ_df.likes_count.sum()

    def aggregate_stats_from_tweet(self, tweet, data_type):
        token_string = p.tokenize(tweet)
        number_of_hashtags = token_string.count('$HASHTAG$')
        number_of_emojis = token_string.count('$EMOJI$')
        number_of_urls = token_string.count('$URL$')
        number_of_mentions = token_string.count('$MENTION$')
        if data_type == "soldiers":
            self.veteran_stats['hashtags'] = number_of_hashtags if self.veteran_stats.get(
                'hashtags') is None else (int(self.veteran_stats['hashtags']) + number_of_hashtags)
            self.veteran_stats['emojis'] = number_of_emojis if self.veteran_stats.get(
                'emojis') is None else (self.veteran_stats['emojis'] + number_of_emojis)
            self.veteran_stats['urls'] = number_of_urls if self.veteran_stats.get(
                'urls') is None else (self.veteran_stats['urls'] + number_of_urls)
            self.veteran_stats['mentions'] = number_of_mentions if self.veteran_stats.get(
                'mentions') is None else (self.veteran_stats['mentions'] + number_of_mentions)
        else:
            self.civilian_stats['hashtags'] = number_of_hashtags if self.civilian_stats.get(
                'hashtags') is None else(self.civilian_stats['hashtags'] + number_of_hashtags)
            self.civilian_stats['emojis'] = number_of_emojis if self.civilian_stats.get(
                'emojis') is None else(self.civilian_stats['emojis'] + number_of_emojis)
            self.civilian_stats['urls'] = number_of_urls if self.civilian_stats.get(
                'urls') is None else(self.civilian_stats['urls'] + number_of_urls)
            self.civilian_stats['mentions'] = number_of_mentions if self.civilian_stats.get(
                'mentions') is None else(self.civilian_stats['mentions'] + number_of_mentions)

    def process_data(self):
        pass

    def get_combined_file(self, folder_name="soldiers", force_rewrite=False):
        os.chdir("{}/data/{}".format(CURRENT_WORKDIR, folder_name))
        all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]
        if not os.path.exists("combined_{}.csv".format(folder_name)) or force_rewrite:
            combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
            combined_csv.to_csv("combined_{}.csv".format(folder_name), index=False, encoding='utf-8-sig')
            print("combined_{}.csv saved".format(folder_name))
        else:
            print("File exists. Skipping. Use force_rewrite to overwrite.")

    def get_dataframe(self, data_type="soldiers"):
        os.chdir("{}/data/{}".format(CURRENT_WORKDIR, data_type))
        return pd.read_csv("combined_{}.csv".format(data_type))

    def clean_veteran_tweet_and_create_df(self, vet_df):
        vet_tweets = list(vet_df['tweet'])
        for i in range(len(vet_tweets)):
            if i % 100 == 0:
                print("{}/{}".format(i, len(vet_tweets)))
            if 'http://pandora.com/' in vet_tweets[i]:
                continue
            self.pre_process_data(vet_tweets[i], "soldiers")
        self.cleaned_vet_tweet_df = pd.DataFrame(
            {'tweets': self.cleaned_veteran_tweets})
        self.cleaned_vet_tweet_df.to_csv(
            'cleaned_vet_tweet_df.csv', header=False, mode='a')
        print("veteran stats: {}".format(self.veteran_stats))
        print('cleaned_vet_tweet_df.csv created')
        with open('{}.txt'.format(dt.datetime.utcnow()), 'w') as file:
            file.write(json.dumps(self.veteran_stats))

    def clean_civilian_tweet_and_create_df(self, civ_df):
        civ_tweets = list(civ_df['tweet'])
        for i in range(len(civ_tweets)):
            if i % 100 == 0:
                print("{}/{}".format(i, len(civ_tweets)))
                self.pre_process_data(vet_tweets[i], "civilians")
        self.cleaned_civ_tweet_df = pd.DataFrame(
            {'tweets': self.cleaned_civilian_tweets})
        self.cleaned_civ_tweet_df.to_csv(
            'cleaned_civ_tweet_df.csv', header=False, mode='a')
        print("civilian stats: {}".format(self.civilian_stats))
        print('cleaned_civ_tweet_df.csv created')
        with open('{}.txt'.format(dt.datetime.utcnow()), 'w') as file:
            file.write(json.dumps(self.civilian_stats))

if __name__ == "__main__":
    # start_time = time.time()
    # pr = Preprocess()
    # vet_df = pr.get_dataframe()
    # vet_df = vet_df[['tweet', 'time', 'photos', 'replies_count', 'retweets_count', 'likes_count', 'retweet']]
    # vet_df = vet_df[(vet_df['retweet'] == False)]
    # print("Vet Shape: {}".format(vet_df.shape))
    # pr.clean_veteran_tweet_and_create_df(vet_df)
    # print("--- %s seconds ---" % (time.time() - start_time))
    

    start_time = time.time()
    pr = Preprocess()
    civ_df = pr.get_dataframe(data_type="civilians")
    civ_df = civ_df[['tweet', 'time', 'photos', 'replies_count', 'retweets_count', 'likes_count', 'retweet']]
    civ_df = civ_df[(civ_df['retweet'] == False)]
    print("Civ Shape: {}".format(civ_df.shape))

    # pr.clean_veteran_tweet_and_create_df(vet_df)
    # print("--- %s seconds ---" % (time.time() - start_time))

    # pr.aggregate_stats_from_df(vet_df, civ_df) # Stats directly extracted from the twitter data