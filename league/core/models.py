from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

class League(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    rules = models.TextField(blank=True)
    roster_lock = models.BooleanField(default=False)
    moderators = models.ManyToManyField('auth.User')
    #Regular season start/end date (not including playoffs)
    start = models.DateTimeField()
    end = models.DateTimeField()
    playoff = models.BooleanField(default=False)
    
class Division(models.Model):
    league = models.ForeignKey('League')
    name = models.CharField(max_length=50)
    
class DivisionNews(models.Model):
    news = models.TextField()
    author = models.ForeignKey('auth.User')
    date = models.DateTimeField(auto_now_add=True)
    
class Game(models.Model):
    name = models.CharField(max_length=50)
    
class Team(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey('auth.User')
    date_created = models.DateField(default=datetime.now)
    recruiting = models.BooleanField(default=False)
    #URLField is basically deprecated so no point in using it
    url = models.CharField(max_length=200, blank=True)
    players = models.ManyToManyField('auth.User')
    leader = models.ForeignKey('auth.user')
    captains = models.ManyToManyField('auth.User')
    details = models.TextField()
    division = models.ForeignKey('Team')
    tag = models.CharField(max_length=25)
    
    #Hooray for precalculated values
    wins = models.PositiveSmallIntegerField()
    losses = models.PositiveSmallIntegerField()
    draws = models.PositiveSmallIntegerField()
    forfiets = models.PositiveSmallIntegerField()
    points_forward = models.PositiveIntegerField()
    points_against = models.PositiveIntegerField()
    
class Match(models.Model):
    RESULT_CHOICES = (
        ('1', 'Away Team Wins!')
        ('2', 'Home Team Wins!')
        ('3', 'Draw!')
    )
    
    league = models.ForeignKey('League')
    away = models.ForeignKey('Team')
    away_score = models.PositiveSmallIntegerField(blank=True)
    away_accept = models.BooleanField(default=False)
    home = models.ForeignKey('Team', blank=True, null=True)
    home_score = models.PositiveSmallIntegerField(blank=True)
    home_accept = models.BooleanField(default=False)
    play_by = models.DateTimeField()
    date = models.DateTimeField(blank=True)
    result = models.CharField(max_length=1, choices=RESULT_CHOICES)
    playoff = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('away', 'home')
    
class MatchMessage(models.Model):
    match = models.ForeignKey('Match')
    user = models.ForeignKey('auth.User')
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    
class UniqueID(models.Model):
    user = models.ForeignKey('auth.User')
    game = models.ForeignKey('Game')
    name = models.CharField(max_length=30)
    
    class Meta:
        unique_together = ('game', 'name')
    