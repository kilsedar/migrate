# -*- coding: utf-8 -*-
import json
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from forms import PlayerForm, UserForm
from questionnaire.models import Question
from models import Profile, Player

# Create your views here.
@csrf_protect
def register(request):
    uform = UserForm(request.POST or None)
    form = PlayerForm(request.POST or None)
    if uform.is_valid() and form.is_valid():
        dj_user= uform.save()
        player = form.save(commit=False)
        player.user = dj_user
        prof = Profile()
        prof.save()
        player.profile = prof
        player.save()
        #authenticate user
        #dj_user = authenticate(username=uform.cleaned_data['username'],
        #                       password=uform.cleaned_data['password'],
        #                      )
        #login(request, dj_user)
        #success sends to map and the questions..
        return redirect(reverse('login'))
    #register invalid.. go back to register (test registration errors!! probably fix css for errors)
    return render(request, 'registration/register.html', context={'form': form, 'uform': uform})


@login_required
def player_profile(request):
    player = Player.objects.get(user=request.user)
    return render(request, 'registration/profile.html', context={'player': player})