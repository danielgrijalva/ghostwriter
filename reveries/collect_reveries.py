from reveries.models import Tweet
import tweepy
from decouple import config

# Twitter keys

CONSUMER_KEY = config('CONSUMER_KEY')
CONSUMER_SECRET = config('CONSUMER_SECRET')
ACCESS_TOKEN = config('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET')

# Twiter OAuth

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def collect_reveries():
    
    # get first page of list (20 tweets)
    twitter_list = api.list_timeline(
        owner_screen_name='danielgrijalvas',
        slug='fiction',
        tweet_mode='extended',
    )

    # evaluate each tweet and save to db
    for t in twitter_list:
        tweet = t._json
        try:
            if (    not tweet.get('entities').get('media')
                and not tweet['entities']['user_mentions']
                and not tweet['is_quote_status']
                and not tweet.get('retweeted_status')
                and not tweet['in_reply_to_status_id']):

                new = Tweet(
                    tweet_id=tweet['id'],
                    user=tweet['user']['screen_name'],
                    text=tweet['full_text'],
                )
                
                # save or exit if already exists in db
                try:
                    new.save()
                    print(new)
                except Exception as e:
                    break

        except AttributeError as e:
            pass
    

if __name__=='__main__':
    collect_reveries()
