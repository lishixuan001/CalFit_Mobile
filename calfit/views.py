from django.shortcuts import render
from django.contrib import auth
from django.http import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from calfit.models import *
from calfit.calc import *
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
        email = request.POST.get("email")

        context["username_value"] = username
        context["password_value"] = password
        context["confirm_password_value"] = confirm_password
        context["invalid_email"] = email

        # User object here is default by Django
        if username_exist(username):
            context["duplicated_username"] = True
            return render(request, "registration.html", context)

        # Check if username is in email format
        if not valid_email(email):
            context["invalid_email"] = True
            return render(request, "registration.html", context)

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if password matches
        if password == confirm_password and password is not "" or None:
            User.objects.create_user(username=username, password=password, email=email)
            return render(request, "login.html", context)
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
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/calfit/welcome/')


@login_required(login_url='/calfit/welcome/')
def index(request):
    """
    :param request: request received
    :return: http redirection to index page if logged in
    """
    context = dict(
        goal_today=0,
        current_steps=0,
        message=None
    )

    # TODO: Call API to get current steps
    # TODO: If previous dates' steps were not syncronized, update
    context["current_steps"] = 1200

    # Check and formulate local time -> cloud database should save as { "20180101" : "8741" } pattern
    user = auth.get_user(request)
    today_date = timezone.now().date()

    today_goal_exist = Goal.objects.filter(user=user, date=today_date).exists()

    if today_goal_exist:
        context["goal_today"] = Goal.objects.get(user=user, date=today_date).get_goal()
    else:
        past_steps, past_goals = get_past_steps_and_goals(user, today_date)
        goals_for_next_week = calc_goal(past_steps, past_goals)
        goal_today = save_goals_for_next_week(user, today_date, goals_for_next_week)


        context["goal_today"] = goal_today

    if goal_decrease_for_two_consecutive_weeks():
        # TODO: Create messages for next week (New Object -- Message)
        pass

    message = Message(title="Message Title", content="Message Content")
    context["message"] = message

    return render(request, 'index.html', context)


@login_required(login_url='/calfit/welcome/')
def history(request):
    # TODO
    pass


@login_required(login_url='/calfit/welcome/')
def profile(request):
    # TODO
    pass
# ==================================================== #
#                  Helper Functions                    #
# ==================================================== #

# TODO: Create "No Internet" present page  

def valid_email(address):
    """
    :param address: The email address to be tested
    :return: A bool indicating if the email address is in valid format
    """
    return re.match('^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?))$', address) is not None

def username_exist(username):
    """
    :param username: The username to be tested
    :return: A bool indicating if the username is taken
    """
    return User.objects.filter(username=username).exists()

class Message:
    def __init__(self, title, content):
        self.title = title
        self.content = content

def goal_decrease_for_two_consecutive_weeks():
    """
    :return: A bool indicating if goal decreases for two consecutive weeks for the user
    """
    # TODO: What is the principle of "decreasing for two consecutive weeks"
    return True

def get_past_steps_and_goals(user, today_date):
    """
    :param user: Current Logged In User
    :param today_date: Today's Date
    :return: Past dates' steps and goals (in seperate lists)
    """
    # TODO: Get previous 7 days' steps, if not enough days' data is available, do our best & send message
    # TODO: After each calculation, create 7 Goal objects
    past_steps = []
    past_goals = []

    # FIXME: Current strategy -> retrieve by days, when some day's data is not available, deem it as terminal (not under-update)
    # FIXME: -> Only consider data (days) which has both past_step and past_goal
    for i in range(7):
        past_date = today_date - timezone.timedelta(days=i + 1)

        past_record_exist = Record.objects.filter(user=user, date=past_date).exists()
        past_goal_exist = Goal.objects.filter(user=user, date=past_date).exists()

        if past_record_exist and past_goal_exist:
            date_past_steps = Record.objects.get(user=user, date=past_date).get_steps()
            date_past_goal = Goal.objects.get(user=user, date=past_date).get_goal()

            past_steps.append(date_past_steps)
            past_goals.append(date_past_goal)
        else:
            break
    return past_steps, past_goals

def save_goals_for_next_week(user, today_date, goals_for_next_week):
    """
    :param user: Current Logged In User
    :param today_date: Today's Date
    :param goals_for_next_week: [goal0, goal1, ...] A list of goals for next week (from today on, include)
    :return: The goal for today (based on the newly calculated)
    """
    for i in range(len(goal_for_next_week)):
        new_date = today_date + timezone.timedelta(days=i)
        new_goal = Goal(user=user, date=new_date)
        new_goal.save()
    return goal_for_next_week[0]