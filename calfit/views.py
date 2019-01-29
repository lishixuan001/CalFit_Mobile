from django.shortcuts import render
from django.contrib import auth
from django.http import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import time

def welcome(request):
    if request.method == 'GET':
        return render(request, 'welcome.html', {})

def registration(request):
    if request.method == 'GET':
        return render(request, 'registration.html', {})

    if request.method == 'POST':
        username = request.POST.get('username')

        # User object here is default by Django
        # TODO: Check if deplicated username

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if password matches
        if password == confirm_password and password is not "" or None:
            User.objects.create_user(username=username, password=password)
        return HttpResponseRedirect('/calfit/login')

def login(request):
    """
    :param request: request received
    :return: http response about logging in
    """
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/calfit/index')
        return render(request, 'login.html', {})

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check username and password, if valid, return a User object
        user = auth.authenticate(username=username, password=password)
        if user:
            # If success
            auth.login(request, user)
            return HttpResponseRedirect('/calfit/index/')
        else:
            context = {
                'login_error' : True,
            }
            return render(request, 'login.html', context)

@login_required(login_url='/calfit/welcome/')
def index(request):
    """
    :param request: request received
    :return: http redirection to index page if logged in
    """

    # Check and formulate local time -> cloud database should save as { "20180101" : "8741" } pattern
    date = time.strftime("%Y%m%d")

    # TODO: Create a Cloud Http Request for today's goal, if a goal does not exist yet, do a request for computing
    goal_today = 1234
    current_steps = 1200

    context = {
        'goal_today' : goal_today,
        'current_steps' : current_steps
    }
    return render(request, 'index.html', context)