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

    def add_arguments(self, parser):        
        parser.add_argument(
            '--guest',
            nargs=1,
            dest='guest',
        )        

    def handle(self, *args, **options):
        if options['guest']:
            self.initialize(options['guest'][0])
        else:
            # get first page of list (20 tweets)
            twitter_list = self.api.list_timeline(
                owner_screen_name=settings.LIST_OWNER,
                slug=settings.LIST_NAME,
                tweet_mode='extended',
                include_rts=False,
                count=22, # for some reason it returns n-2
            )

            # evaluate each tweet and save to db
            for t in twitter_list:
                tweet = t._json
                try:
                    if self.filter(tweet):
                        new = Tweet(
                            tweet_id=tweet['id'],
                            user=tweet['user']['screen_name'],
                            text=self.clean(tweet['full_text'])
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


    def initialize(self, screen_name):
        ''' Retrieve all tweets from a user.
            https://gist.github.com/yanofsky/5436496
        '''

        # initialize a list to hold all the tweepy Tweets
        alltweets = []  
        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = self.api.user_timeline(screen_name=screen_name, count=200, include_rts=False, tweet_mode='extended')
        
        # save most recent tweets
        alltweets.extend(new_tweets)
     
        # save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0 and len(alltweets) < 1000:
            print('getting tweets before {}'.format(oldest))
            
            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = self.api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')
            
            # save most recent tweets
            alltweets.extend(new_tweets)
            
            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            
            print('...{} tweets downloaded so far'.format(len(alltweets)))
        
        # filter out tweets and save to db
        for t in alltweets:
            tweet = t._json
            try:
                if self.filter(tweet):
                    new = Tweet(
                        tweet_id=tweet['id'],
                        user=tweet['user']['screen_name'],
                        text=self.clean(tweet['full_text']),
                    )

                    try:
                        new.save()
                        print('Successfully saved a story from @{}'.format(new.user))
                    except Exception as e:
                        print('*** ALREADY EXISTS ***')

            except AttributeError as e:
                pass

        print(len(Tweet.objects.all()))      

    def clean(self, text):
        return text.replace('\n', ' ').replace('&amp;', '&').lower()
    
    def filter(self, tweet):
        if (    not tweet.get('entities').get('media')
            and not tweet['entities']['user_mentions']
            and not tweet['is_quote_status']
            and not tweet['in_reply_to_status_id']
            and not 'http' in tweet['full_text']
            and not '@' in tweet['full_text']
            and not '#' in tweet['full_text']
            and not '"' in tweet['full_text']):

            return True
        else:
            return False