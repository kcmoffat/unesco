from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=512)

class Site(models.Model):
    unesco_id = models.IntegerField(max_length=11, blank=False, unique=True)
    name = models.CharField(max_length=512)
    country = models.ForeignKey(Country)
    site_url = models.CharField(max_length=512)
    image_url = models.CharField(max_length=512)
    brief_desc = models.TextField(max_length=1500)
    long_desc = models.TextField(max_length=32000)
    is_404 = models.BooleanField(blank=False)
    is_complete = models.BooleanField(blank=False)

class Quiz(models.Model):
    created_at = models.DateTimeField()
    session_key = models.CharField(max_length=40)

class Question(models.Model):
    created_at = models.DateTimeField()
    site = models.ForeignKey(Site)
    quiz = models.ForeignKey(Quiz)
    question_number = models.IntegerField(max_length=11)
    answered = models.BooleanField()
    correct = models.BooleanField()

class Choice(models.Model):
    created_at = models.DateTimeField()
    question = models.ForeignKey(Question)
    choice_number = models.IntegerField(max_length=11)
    country = models.ForeignKey(Country)

class Guess(models.Model):
    created_at = models.DateTimeField()
    choice = models.ForeignKey(Choice)
