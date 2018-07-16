from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from reveries.models import Tweet
import tweepy


class Command(BaseCommand):
    help = 'Update host\'s narrative.'

    def __init__(self):
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def handle(self, *args, **options):
        # get first page of list (20 tweets)
        twitter_list = self.api.list_timeline(
            owner_screen_name=settings.LIST_OWNER,
            slug=settings.LIST_NAME,
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
                    
                    # save to db or exit if already exists
                    try:
                        new.save()
                        print('Successfully saved a story from @{}'.format(new.user))
                    except Exception as e:
                        print('Reached previous reveries. Exiting...')
                        break

            except AttributeError as e:
                pass
