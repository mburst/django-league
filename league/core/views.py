from core.models import *
from core.forms import *

from django.shortcuts import render, redirect#, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.db.models import F
#from django.forms.models import modelformset_factory
from django.http import HttpResponse
#from django.db import connection, transaction

#from operator import attrgetter
#from datetime import datetime, timedelta
#import time

def home(request):
    hello = "hello world"
    return render(request, 'core/index.html', locals())
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            try:
                new_user = authenticate(username=new_user.username, password=request.POST['password2'])
                print new_user
                if new_user is not None:
                    login(request, new_user)
            except:
                pass
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', locals())
    
@login_required
def create_team(request, league_id=None):
    if request.method == 'POST':
        try:
            game = League.objects.get(id=league_id).game
        except:
            return HttpResponse("Sorry our servers our busy. Please try again later.")
        form = TeamForm(request.POST)        
        if form.is_valid():
            new_team = form.save(commit=False)
            leader = request.user
            new_team.leader = leader
            new_team.game = game
            new_team.save()
            new_team.players.add(leader)
            new_team.save()
            return redirect('home')
    else:
        form = TeamForm()
    return render(request, 'core/create_team.html', locals())

def manage_team(request, team_id=None):
    try:
        team = Team.objects.get(id=team_id)
    except:
        return redirect('/create_team/')
    if request.user == team.leader:
        if request.method == "POST":
            form = TeamForm(request.POST, instance=team)
            form.save()
        else:
            form = TeamForm(instance=team)
        return render(request, 'core/manage_team.html', locals())
    return redirect('home') #change to team_page

#def team_page(request, team_id):

def player_search(request):
    if request.is_ajax():
        #Bug with serializing defered objects so doing it manually
        results = User.objects.only('username').filter(username__istartswith=request.GET.get('term'))
        users = []
        for user in results:
            users.append({'id': user.id, 'value': user.username, 'label': user.username})
        return HttpResponse(simplejson.dumps(users), mimetype='application/json')
    else:
        redirect('home')
    
def generate_season(teams, weeks):
    count = len(teams)
    if count%2 == 1:
        count+=1
        teams.append("BYE")
    if count <= weeks:
           print "Too many weeks and not enough teams"
    table= [ [ 0 for i in range(count) ] for j in range(weeks) ]
    for x in range(weeks):
        for y in range(count):
            table[x][y] = (x+y)%count
    for row in table:
        print "Round " + `row[0]`
        for col in range(count/2):
            print `teams[row[col]]` + "vs" + `teams[row[-(col+1)]]`
        print "END ROUND " + `row[0]`
    print count
    
    