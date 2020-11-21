import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200, null=False)
    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.question_text
    
    def short_string(self):
        if len(self.question_text) <= 27:
            return self.question_text
        return self.question_text[:28] + '...'

    def index_is_odd(self):
        q_index = 0
        objects = self.objects.all()
        for index,item in enumerate(objects):
            if(item.pk == self.pk):
                q_index = index
        return q_index % 2 == 0

    def when_was_published(self):
        """
        Return a string saying when a question was published, from minutes up to years
        """
        now = timezone.now()
        difference = now - self.pub_date
        print(difference)

        unit_of_time_str = ""
        unit_of_time_num = 0

        if (difference.days > 0):
            if (difference.days == 1):
                unit_of_time_str = "day"
                unit_of_time_num = 1
            elif (1 < difference.days < 7):
                unit_of_time_str = "days"
                unit_of_time_num = difference.days
            elif (7 <= difference.days < 14):
                unit_of_time_str = "week"
                unit_of_time_num = difference.days // 7
            elif (14 <= difference.days < 30):
                unit_of_time_str = "weeks"
                unit_of_time_num = difference.days // 7
            elif (30 <= difference.days < 60):
                unit_of_time_str = "month"
                unit_of_time_num = difference.days // 30
            elif (60 <= difference.days < 365):
                unit_of_time_str = "months"
                unit_of_time_num = difference.days // 30
            elif (365 <= difference.days < 730):
                unit_of_time_str = "year"
                unit_of_time_num = difference.days // 365
            else:
                unit_of_time_str = "years"
                unit_of_time_num = difference.days // 365
        elif (difference.days == 0):
            if (difference.seconds < 300):
                return "Posted just now"
            elif (300 <= difference.seconds < 3600):
                unit_of_time_str = "minutes"
                unit_of_time_num = difference.seconds // 60
            elif (3600 <= difference.seconds < 7200):
                unit_of_time_str = "hour"
                unit_of_time_num = difference.seconds // 3600
            elif (7200 <= difference.seconds < 86400):
                unit_of_time_str = "hours"
                unit_of_time_num = difference.seconds // 3600
            
        return "Posted %i %s ago" % (unit_of_time_num, unit_of_time_str)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def total_votes(self):
        choices = self.choice_set.all()
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
        if(self.question.total_votes() > 0):
            return (self.votes / self.question.total_votes()) * 100
        else:
            return (self.votes / 1) * 100


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.content[:11] + '...'