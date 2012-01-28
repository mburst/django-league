from django.db import models
from django.contrib.auth.models import User

class League(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    rules = models.TextField(blank=True)
    roster_lock = models.BooleanField(default=False)
    moderators = models.ManyToManyField('auth.User', related_name='moderates', blank=True)
    game = models.ForeignKey('Game', related_name='leagues')
    start = models.DateTimeField(blank=True)
    weeks = models.PositiveSmallIntegerField(blank=True)
    playoff = models.ForeignKey('Playoff', default=None, blank=True, null=True)
    finished = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s' % self.name
    
class Division(models.Model):
    league = models.ForeignKey('League', related_name='divisions')
    name = models.CharField(max_length=50)
    teams = models.ManyToManyField('Team', related_name='division')
    
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        unique_together = ('league', 'name')
    
class DivisionNews(models.Model):
    title = models.CharField(max_length=100)
    news = models.TextField()
    author = models.ForeignKey('auth.User', related_name='division_news')
    date = models.DateTimeField(auto_now_add=True)
    
class Game(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return u'%s' % self.name
    
class Team(models.Model):
    name = models.CharField(max_length=50)
    players = models.ManyToManyField('auth.User', related_name='teams', blank=True)
    leader = models.ForeignKey('auth.user', related_name='leads', blank=True)
    captains = models.ManyToManyField('auth.User', related_name='captain_of', blank=True)
    date_created = models.DateField(auto_now_add=True)
    recruiting = models.BooleanField(default=False)
    #URLField is basically deprecated so no point in using it
    url = models.CharField(max_length=200, blank=True)
    details = models.TextField(blank=True)
    game = models.ForeignKey('Game', related_name="teams", editable=False)
    tag = models.CharField(max_length=25)
    
    #Hooray for precalculated values
    wins = models.PositiveSmallIntegerField(default=0)
    losses = models.PositiveSmallIntegerField(default=0)
    draws = models.PositiveSmallIntegerField(default=0)
    forfiets = models.PositiveSmallIntegerField(default=0)
    points_forward = models.PositiveIntegerField(default=0)
    points_against = models.PositiveIntegerField(default=0)
    
class Playoff(models.Model):
    PLAYOFF_CHOICES = (
        ('D', 'Double Elimination'),
        ('R', 'Round Robin'),
        ('S', 'Single Elimination'),
    )
    
    teams = models.ManyToManyField('PlayoffTeam') #8, 16, 32
    type = models.CharField(max_length=1, choices=PLAYOFF_CHOICES)
    rounds = models.PositiveSmallIntegerField() #sqrt(teams)
    
class PlayoffRound(models.Model):
    number = models.PositiveSmallIntegerField()
    matches = models.ManyToManyField('PlayoffMatch')
    
class PlayoffTeam(models.Model):
    team = models.ForeignKey('Team')
    seed = models.PositiveSmallIntegerField()
    wins = models.PositiveSmallIntegerField(default=0)
    losses = models.PositiveSmallIntegerField(default=0)
    eliminated = models.BooleanField(default=False)
    
#Because I hate model inheritance
class PlayoffMatch(models.Model):
    RESULT_CHOICES = (
        ('1', 'Away Team Wins!'),
        ('2', 'Home Team Wins!'),
        ('4', 'Pending'),
    )
    
    away = models.ForeignKey('PlayoffTeam', related_name='away_matches', blank=True, null=True)
    away_score = models.PositiveSmallIntegerField(blank=True)
    away_accept = models.BooleanField(default=False)
    home = models.ForeignKey('PlayoffTeam', related_name='home_matches', blank=True, null=True)
    home_score = models.PositiveSmallIntegerField(blank=True)
    home_accept = models.BooleanField(default=False)
    play_by = models.DateTimeField()
    date = models.DateTimeField(blank=True)
    result = models.CharField(max_length=1, default='4', choices=RESULT_CHOICES)
    message = models.ManyToManyField('MatchMessage', blank=True)
    
class Match(models.Model):
    RESULT_CHOICES = (
        ('1', 'Away Team Wins!'),
        ('2', 'Home Team Wins!'),
        ('3', 'Draw!'),
        ('4', 'Pending'),
    )
    
    league = models.ForeignKey('League', related_name='matches')
    away = models.ForeignKey('Team', related_name='away_matches')
    away_score = models.PositiveSmallIntegerField(blank=True)
    away_accept = models.BooleanField(default=False)
    home = models.ForeignKey('Team', related_name='home_matches', blank=True, null=True)
    home_score = models.PositiveSmallIntegerField(blank=True)
    home_accept = models.BooleanField(default=False)
    play_by = models.DateTimeField()
    date = models.DateTimeField(blank=True)
    result = models.CharField(max_length=1, default='4', choices=RESULT_CHOICES)
    message = models.ManyToManyField('MatchMessage', blank=True)
    
    class Meta:
        unique_together = ('away', 'home')
    
class MatchMessage(models.Model):
    user = models.ForeignKey('auth.User', related_name='match_comments')
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    
class UniqueID(models.Model):
    user = models.ForeignKey('auth.User')
    game = models.ForeignKey('Game')
    name = models.CharField(max_length=30)
    
    class Meta:
        unique_together = ('game', 'name')
        
class TeamInvitation(models.Model):
    user = models.ForeignKey('auth.User', related_name='invitations')
    team = models.ForeignKey('Team', related_name='pending_invites')
    