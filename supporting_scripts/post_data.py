"""File to be invoked after data collection
"""
import preprocessor as p
from langdetect import detect
import os
import glob
import pandas as pd


CURRENT_WORKDIR = os.getcwd()
veteran_stats = dict()
civilian_stats = dict()

cleaned_veteran_tweets = list()
cleaned_civilian_tweets = list()


def pre_process_data(tweet, data_type="soldiers"):
    lang = ''
    
    try:
        lang = detect(tweet)
    except:
        print("Can't detect a lang")
    print(tweet[0:10], lang)
    if lang == 'en': #Only parsing English tweets
        aggregate_stats_from_tweet(tweet, data_type) #Data to be deduced from each tweet
        p.set_options(p.OPT.URL, p.OPT.EMOJI)
        cleaned_tweet = p.clean(tweet)
        cleaned_tweet = cleaned_tweet.replace("#", "")
        number_of_words = len(cleaned_tweet)
        if data_type == "soldiers":
            veteran_stats['words'] = number_of_words if veteran_stats.get('words') is None else (veteran_stats['words'] + number_of_words)
            cleaned_veteran_tweets.append(cleaned_tweet)
        else:
            civilan_stats['words'] = number_of_words if civilan_stats.get('words') is None else (civilan_stats['words'] + number_of_words)
            cleaned_civilian_tweets.append(cleaned_tweet)
    else:
        return


def aggregate_stats_from_df(vet_df, civ_df=None):
    veteran_stats['retweets'] = vet_df.retweets_count.sum()
    veteran_stats['replies'] = vet_df.replies_count.sum()
    veteran_stats['likes'] = vet_df.likes_count.sum()
    # civilian_stats['retweets'] = civ_df.retweets_count.sum()
    # civilian_stats['replies'] = civ_df.replies_count.sum()
    # civilian_stats['likes'] = civ_df.likes_count.sum()

def aggregate_stats_from_tweet(tweet, data_type):
    token_string = p.tokenize(tweet)
    number_of_hashtags = token_string.count('$HASHTAG$')
    number_of_emojis = token_string.count('$EMOJI$')
    number_of_urls = token_string.count('$URL$')
    number_of_mentions = token_string.count('$MENTION$')
    if data_type == "soldiers":
        veteran_stats['hashtags'] = number_of_hashtags if veteran_stats.get('hashtags') is None else (veteran_stats['hashtags'] + number_of_hashtags)
        veteran_stats['emojis'] = number_of_emojis if veteran_stats.get('emojis') is None else (veteran_stats['emojis'] + number_of_emojis)
        veteran_stats['urls'] = number_of_urls if veteran_stats.get('urls') is None else (veteran_stats['urls'] + number_of_urls)
        veteran_stats['mentions'] = number_of_mentions if veteran_stats.get('mentions') is None else (veteran_stats['mentions'] + number_of_mentions)
    else:
        civilan_stats['hashtags'] = number_of_hashtags if civilan_stats.get('hashtags') is None else(civilan_stats['hashtags'] + number_of_hashtags)
        civilan_stats['emojis'] = number_of_emojis if civilan_stats.get('emojis') is None else(civilan_stats['emojis'] + number_of_emojis)
        civilan_stats['urls'] = number_of_urls if civilan_stats.get('urls') is None else(civilan_stats['urls'] + number_of_urls)
        civilan_stats['mentions'] = number_of_mentions if civilan_stats.get('mentions') is None else(civilan_stats['mentions'] + number_of_mentions)

def process_data():
    pass

def get_combined_file(folder_name="soldiers", force_rewrite=False):
    os.chdir("{}/data/{}".format(CURRENT_WORKDIR, folder_name))
    all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]
    if not os.path.exists("combined_{}.csv".format(folder_name)) or force_rewrite:
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
        combined_csv.to_csv("combined_{}.csv".format(folder_name), index=False, encoding='utf-8-sig')
        print("combined_{}.csv saved".format(folder_name))
    else:
        print("File exists. Skipping. Use force_rewrite to overwrite.")

def get_dataframe(data_type="soldiers"):
    os.chdir("{}/data/{}".format(CURRENT_WORKDIR, data_type))
    return pd.read_csv("combined_{}.csv".format(data_type))

def clean_veteran_tweet_and_create_df(vet_df):
    vet_tweets = list(vet_df['tweet'])
    for i in range(len(vet_tweets)):
        print("{}/{}".format(i, len(vet_tweets)))
        pre_process_data(vet_tweets[i])
    cleaned_vet_tweet_df = pd.DataFrame({'tweets': cleaned_veteran_tweets})
    cleaned_vet_tweet_df.to_csv('cleaned_vet_tweet_df.csv')
    print('cleaned_vet_tweet_df.csv created')
    print(veteran_stats)

if __name__ == "__main__":
    get_combined_file()
    # get_combined_file("civilians")
    vet_df = get_dataframe()
    # civ_df = get_dataframe("civilians")
    

    vet_df = vet_df[['tweet', 'time', 'photos', 'replies_count', 'retweets_count', 'likes_count', 'retweet']]
    # civ_df = civ_df[['tweet', 'time', 'photos', 'replies_count', 'retweets_count', 'likes_count', 'retweet']]
    print(vet_df.shape)
    # print(civ_df.shape)
    
    vet_df = vet_df[(vet_df['retweet'] == False)]
    # civ_df = civ_df[(civ_df['retweet'] == False)]
    
    aggregate_stats_from_df(vet_df) # Stats directly extracted from the twitter data
    clean_veteran_tweet_and_create_df(vet_df)
    
    
    # civ_tweets = list(civ_df['tweet'])

    