from datetime import datetime, timedelta
from get_places import extract_places_of_interest
from pytz import timezone
import demoji
import requests
import os
import re
import json
import pandas as pd

def convert_to_timezone(tweet_date):
    date = datetime.strptime(tweet_date, '%Y-%m-%dT%H:%M:%S') - timedelta(hours=3)
    return date

def tweet_treatment(tweets):
    treated_tweets = []
    for tweet in tweets:
        extract_places_of_interest(tweet['text'])
        treated_tweets.append({
            'ID': tweet['id'],
            'Date': convert_to_timezone(tweet['created_at'][:-5]),
            'Author': 'BHTrans',
            'Text': demoji.replace(tweet['text'], '')
        })
    return treated_tweets

def auth():
    return 'AAAAAAAAAAAAAAAAAAAAAJqVJgEAAAAADLo4K6RwAUlzo5gEwi7tf9ERGGc%3DDVkP6FddSVL3G3O6PG0d3uYZRl2fTgkXZZU75wNfGP6353qqPo'

def create_url():
    query = "from:OficialBHTRANS"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    tweet_fields = "tweet.fields=author_id,created_at"
    max_results = "max_results=100"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}".format(
        query, tweet_fields, max_results
    )
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_tweets():
    bearer_token = auth()
    url = create_url()
    headers = create_headers(bearer_token)
    tweets = connect_to_endpoint(url, headers)
    return tweets['data']

def add_to_dataset(tweets):
    tweet_dataset = pd.DataFrame(tweets)
    return tweet_dataset

def save(df, filename):
    df.set_index('ID').sort_values(by=['Date']).to_csv(filename)

if __name__ == "__main__":
    tweets = tweet_treatment(get_tweets())
    dataset = add_to_dataset(tweets)
    save(dataset, 'transitobh.csv')