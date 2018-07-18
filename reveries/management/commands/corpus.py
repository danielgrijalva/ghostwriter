from django.core.management.base import BaseCommand, CommandError
from random import shuffle 

from reveries.models import Tweet


class Command(BaseCommand):  

    def handle(self, *args, **options):
        all_tweets = [tweet.text for tweet in Tweet.objects.all()]
        shuffle(all_tweets)

        train, test, val = self.split(all_tweets)

        self.save('train.txt', train)
        self.save('test.txt', test)
        self.save('validation.txt', val)

    def split(self, data):
        length = len(data)
        train_length = round(length * 0.8)
        val_length = round(train_length * 0.2)

        train = data[:train_length]
        test = data[train_length:]
        val = train[:val_length]
        train = train[val_length:]

        return train, test, val

    def save(self, filename, data):
        text = '\n\n'.join(data)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
            