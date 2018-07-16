from django.db import models

class Tweet(models.Model):
    tweet_id = models.BigIntegerField(unique=True)
    user = models.CharField(max_length=15)
    text = models.CharField(max_length=280)

    def __str__(self):
        return 'ID: {} - @{}'.format(self.tweet_id, self.user)