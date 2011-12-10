from core.models import *
from core.forms import *

from django.shortcuts import render#, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.db.models import F
#from django.forms.models import modelformset_factory
#from django.http import HttpResponse
#from django.db import connection, transaction

#from operator import attrgetter
#from datetime import datetime, timedelta
#import time

def home(request):
    hello = "hello world"
    return render(request, 'core/index.html', locals())
    
@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        new_team = form.save(commit=False)
        leader = request.user
        
        new_team.players.add(leader)
        new_team.leader = leader
        
        if new_team.is_valid():
            new_team.save()
            new_team.save_m2m()
            return redirect('home')
    else:
        form = TeamForm()
    return render(request, 'core/create_team.html', locals())