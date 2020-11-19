import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200, null=False)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
    def short_string(self):
        if len(self.question_text) <= 27:
            return self.question_text
        return self.question_text[:28] + '...'
    
    def pk_is_odd(self):
        return self.pk % 2 == 0

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def total_votes(self):
        choices = self.choice_set.all()
        # print(str(self) + choices)
        total = 0
        for choice in choices:
            total += choice.votes
        return total
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, null=False)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
    
    def proportion_of_votes(self):
        return (self.votes / self.question.total_votes()) * 100


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.content[:11] + '...'