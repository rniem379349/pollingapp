import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

from pollingapp.mixins import WhenWasObjectCreatedMixin

# Create your models here.
class Question(WhenWasObjectCreatedMixin, models.Model):
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

    def create_when_was_posted_string(self):
        """
        Return a string saying when a question was published, from minutes up to years
        """
        when_was_created = self.when_was_created(self.pub_date)
        if when_was_created == "just now":
            return "Created %s" % (when_was_created)
        return "Created %s ago" % (when_was_created)

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


class Comment(WhenWasObjectCreatedMixin, MPTTModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='children')

    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now())
    
    class MPTTMeta:
        order_insertion_by = ['date_posted']

    def __str__(self):
        return self.content[:11] + '...'
    
    def create_when_was_posted_string(self):
        """
        Return a string saying when a comment was posted, from minutes up to years
        """
        when_was_posted = self.when_was_created(self.date_posted)
        if when_was_posted == "just now":
            return "Posted %s" % (when_was_posted)
        return "Posted %s ago" % (when_was_posted)