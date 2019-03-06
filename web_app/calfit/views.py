from django.shortcuts import render
from django.contrib import auth
from django.http import *
from django.contrib.auth.decorators import login_required
from calfit.calc import calc_goal
from calfit.helper_methods import *

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

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
        messages=[]
    )

    # TODO: When connect with cloud, update all incomplete local record steps data
    context["current_steps"] = 1200

    # Check and formulate local time -> cloud database should save as { "20180101" : "8741" } pattern
    user = auth.get_user(request)
    today_date = timezone.datetime.now(timezone.utc).date()

    today_goal_exist = Goal.objects.filter(user=user, date=today_date).exists()

    if today_goal_exist:
        context["goal_today"] = Goal.objects.get(user=user, date=today_date).get_goal()
    else:
        past_steps, past_goals = get_past_steps_and_goals(user, today_date)

        if len(past_steps) > 0 and len(past_goals) > 0:
            goals_for_next_week = calc_goal(convert_to_k(past_steps), convert_to_k(past_goals))
            goal_today = save_goals_for_next_week(user, convert_from_k(goals_for_next_week), today_date)
        else:
            goal_today = "[Error] Insufficient Data"

        context["goal_today"] = goal_today

    # Check if need to update "goal decrease for two weeks" messages
    today_goal_decrease_message_exist = Message.objects.filter(user=user, date=today_date,
                                                               type=MessageType.INTERACTIVE).exists()
    if goal_decrease_for_two_consecutive_weeks(user, today_date) and not today_goal_decrease_message_exist:
        for i in range(7):
            future_date = today_date - timezone.timedelta(days=i)
            goal_decrease_message_template = GOAL_DECREASE_MESSAGE_TEMPLATES[i]

            future_message = Message(user=user, date=future_date, type=MessageType.INTERACTIVE,
                                     message_title=MessageTitle.SURVEY,
                                     message_content=goal_decrease_message_template["message_content"],
                                     message_respond_yes=goal_decrease_message_template["message_respond_yes"],
                                     message_respond_no=goal_decrease_message_template["message_respond_no"])
            future_message.save()

    # Check if there's any reminding message today
    today_message_exist = Message.objects.filter(user=user, date=today_date).exists()
    if today_message_exist:
        messages = Message.objects.filter(user=user, date=today_date)
        for message in messages:
            if message.type == MessageType.INTERACTIVE:
                if message.responded is False:
                    context["messages"].append(message)
                message.responded = True
                message.save()

    return render(request, 'index.html', context)


@login_required(login_url='/calfit/welcome/')
def history(request):
    user = auth.get_user(request)
    today_date = timezone.datetime.now(timezone.utc).date()

    last_week_records = get_last_week_records(user, today_date) # [HistoryRecord0, HistoryRecord01, ...]

    context = dict(
        past_dates = [record.date for record in last_week_records],
        past_steps = [record.steps for record in last_week_records],
        past_gaps = [max(record.goal-record.steps, 0) if record.goal and record.steps else record.goal if record.goal else 0 for record in last_week_records]
    )

    return render(request, 'history.html', context)


@login_required(login_url='/calfit/welcome/')
def profile(request):
    # TODO
    pass


