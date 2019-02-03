from django.shortcuts import render
from django.contrib import auth
from django.http import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import time, re

def welcome(request):
    if request.method == 'GET':
        return render(request, 'welcome.html', {})

def registration(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'registration.html', context)

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        context["username_value"] = username
        context["password_value"] = password
        context["confirm_password_value"] = confirm_password

        # Check if username is in email format
        if not valid_email(username):
            context["invalid_username"] = True
            return render(request, "registration.html", context)

        # User object here is default by Django
        if username_exist(username):
            context["duplicated_username"] = True
            return render(request, "registration.html", context)

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if password matches
        if password == confirm_password and password is not "" or None:
            User.objects.create_user(username=username, password=password)
            return HttpResponseRedirect('/calfit/login')
        else:
            context["psw_not_match"] = True
            return render(request, "registration.html", context)

def login(request):
    """
    :param request: request received
    :return: http response about logging in
    """
    context = {}

    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/calfit/index')
        return render(request, 'login.html', context)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        context["username_value"] = username

        if not username_exist(username):
            context["user_not_exist"] = True
            return render(request, 'login.html', context)

        # Check username and password, if valid, return a User object
        user = auth.authenticate(username=username, password=password)
        if user:
            # If success
            auth.login(request, user)
            return HttpResponseRedirect('/calfit/index/')
        else:
            context["psw_not_match"] = True
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


# ==================================================== #
#                  Helper Functions                    #
# ==================================================== #
def valid_email(address):
    return re.match('^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?))$', address) is not None


def username_exist(username):
    return User.objects.filter(username=username).exists()