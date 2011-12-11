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
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)        
        if form.is_valid():
            new_team = form.save(commit=False)
            leader = request.user
            new_team.leader = leader
            new_team.save()
            new_team.players.add(leader)
            new_team.save()
            return redirect('home')
    else:
        form = TeamForm()
    return render(request, 'core/create_team.html', locals())

def manage_team(request, team_id=None):
    return render(request, 'core/manage_team.html', locals())

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
    
    