"""This module contains  Question, Choice and Vote models for the Polls app."""
import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Django model Object for Question."""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end_date')

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """if the question was published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """if the question is published."""
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """if the question is in polling period."""
        now = timezone.now()
        if self.end_date:
            return self.is_published and now <= self.end_date
        return self.is_published()

    def __str__(self):
        """return question string."""
        return self.question_text

    def get_voted_choice(self, user):
        """Get the choice that is already voted."""
        for choice in self.choice_set.all():
            if Vote.objects.filter(choice=choice, user=user).exists():
                return choice
        return None


class Choice(models.Model):
    """Choice model for creating choices."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def votes(self):
        """count total number of this choice."""
        return Vote.objects.filter(choice=self).count()

    def __str__(self):
        """Return Choice string."""
        return self.choice_text


class Vote(models.Model):
    """Vote model for check authenticated user vote"""
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def question(self):
        """Question of this choice."""
        return self.choice.question
