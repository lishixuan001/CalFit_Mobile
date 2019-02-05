from django.shortcuts import render
from django.contrib import auth
from django.http import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from calfit.models import *
from calfit.calc import *
from calfit.helper_methods import *
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
        message=[]
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
        # TODO: Send Message if recent steps are not uploaded
        past_steps, past_goals = get_past_steps_and_goals(user, today_date)
        goals_for_next_week = calc_goal(convert_to_k(past_steps), convert_to_k(past_goals))
        goal_today = save_goals_for_next_week(user, today_date, convert_from_k(goals_for_next_week))
        context["goal_today"] = goal_today

    # Check if need to update "goal decrease for two weeks" messages
    today_goal_decrease_message_exist = Message.objects.filter(user=user, date=today_date,
                                                               type=MessageType.GOAL_DECREASE).exists()
    if goal_decrease_for_two_consecutive_weeks() and not today_goal_decrease_message_exist:
        for i in range(7):
            future_date = today_date - timezone.timedelta(days=i)
            goal_decrease_message_template = GOAL_DECREASE_MESSAGE_TEMPLATES[i]

            future_message = Message(user=user, date=future_date, type=MessageType.GOAL_DECREASE,
                                     message_title=MessageTitle.SURVEY,
                                     message_content=goal_decrease_message_template["message_content"],
                                     message_repond_yes=goal_decrease_message_template["message_repond_yes"],
                                     message_repond_no=goal_decrease_message_template["message_repond_no"])
            future_message.save()

    # Check if there's any reminding message today
    today_message_exist = Message.objects.filter(user=user, date=today_date).exists()
    if today_message_exist:
        messages = Message.objects.filter(user=user, date=today_date)
        for message in messages:
            context["message"].append(message)

    # TODO: When connect with cloud, update all incomplete local record steps data


    return render(request, 'index.html', context)


@login_required(login_url='/calfit/welcome/')
def history(request):
    user = auth.get_user(request)
    today_date = timezone.now().date()

    last_week_records = get_last_week_records(user, today_date)

    context = dict(
        last_week_records=last_week_records
    )

    return render(request, 'history.html', context)



@login_required(login_url='/calfit/welcome/')
def profile(request):
    # TODO
    pass
