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
                                                               type="goal_decrease_for_two_consecutive_weeks").exists()
    if goal_decrease_for_two_consecutive_weeks() and not today_goal_decrease_message_exist:
        for i in range(7):
            future_date = today_date - timezone.timedelta(days=i)
            goal_decrease_message_template = goal_decrease_message_templates[i]

            future_message = Message(user=user, date=future_date, type="goal_decrease_for_two_consecutive_weeks",
                                     message_title=goal_decrease_message_template["message_title"],
                                     message_content=goal_decrease_message_template["message_content"],
                                     message_repond_yes=goal_decrease_message_template["message_repond_yes"],
                                     message_repond_no=goal_decrease_message_template["message_repond_no"])
            past_record_exist = Record.objects.filter(user=user, date=past_date).exists()
            past_goal_exist = Goal.objects.filter(user=user, date=past_date).exists()

            if past_record_exist and past_goal_exist:
                date_past_steps = Record.objects.get(user=user, date=past_date).get_steps()
                date_past_goal = Goal.objects.get(user=user, date=past_date).get_goal()

                past_steps.append(date_past_steps)
                past_goals.append(date_past_goal)

    # Check if there's any reminding message today
    today_message_exist = Message.objects.filter(user=user, date=today_date).exists()
    if today_message_exist:
        messages = Message.objects.filter(user=user, date=today_date)
        for message in messages:
            context["message"].append(message)





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

class MessageInfo:
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
    :return: Past dates' steps and goals (in seperate lists) -> skip invalid (incomplete) data dates
    """
    # TODO: Get previous 7 days' steps, if not enough days' data is available, do our best & send message
    # TODO: After each calculation, create 7 Goal objects
    past_steps = []
    past_goals = []

    # FIXME: Current strategy -> retrieve by days, when some day's data is not available, deem it as terminal (not under-update)
    # FIXME: -> Only consider data (days) which has both past_step and past_goal
    # FIXME: -> If recent data is empty, count it as 0
    for i in range(7):
        past_date = today_date - timezone.timedelta(days=i+1)

        past_record_exist = Record.objects.filter(user=user, date=past_date).exists()
        past_goal_exist = Goal.objects.filter(user=user, date=past_date).exists()

        if past_record_exist and past_goal_exist:
            date_past_steps = Record.objects.get(user=user, date=past_date).get_steps()
            date_past_goal = Goal.objects.get(user=user, date=past_date).get_goal()

            past_steps.append(date_past_steps)
            past_goals.append(date_past_goal)

    return past_steps, past_goals


def get_last_week_records(user, today_date):
    """
    :param user: Current Logged In User
    :param today_date: Today's Date
    :return: [HistoryRecord0, HistoryRecord1, ...]
    """
    last_week_records = []

    for i in range(7):
        past_date = today_date - timezone.timedelta(days=i+1)
        date_past_steps = date_past_goal = None

        past_record_exist = Record.objects.filter(user=user, date=past_date).exists()
        past_goal_exist = Goal.objects.filter(user=user, date=past_date).exists()

        if past_record_exist:
            date_past_steps = Record.objects.get(user=user, date=past_date).get_steps()
        if past_goal_exist:
            date_past_goal = Goal.objects.get(user=user, date=past_date).get_goal()

        last_week_records.append(HistoryRecord(past_date, date_past_steps, date_past_goal))

    return last_week_records


def convert_to_k(data):
    """
    :param data: [num0, num1, ...] A list of data to be converted to K count-unit
    :return: Transitioned list of data . [1000, 1100] -> [1.0, 1.1]
    """
    return list(map(lambda x: x / 1000, data))


def convert_from_k(data):
    """
    :param data: [num0, num1, ...] A list of data to be converted from K count-unit
    :return: Transitioned list of data. [1.0, 1.1] -> [1000, 1100]
    """
    return list(map(lambda x: int(x * 1000), data))


def save_goals_for_next_week(user, today_date, goals_for_next_week):
    """
    :param user: Current Logged In User
    :param today_date: Today's Date
    :param goals_for_next_week: [goal0, goal1, ...] A list of goals for next week (from today on, include)
    :return: The goal for today (based on the newly calculated)
    """
    for i in range(len(goals_for_next_week)):
        new_date = today_date + timezone.timedelta(days=i)
        new_goal = Goal(user=user, date=new_date, goal=goals_for_next_week[i])
        new_goal.save()
    return goals_for_next_week[0]

class HistoryRecord:
    def __init__(self, date, steps, goal):
        self.date = date
        self.steps = steps
        self.goal = goal

    def get_date(self):
        return timezone.datetime.strftime(self.date, "%b %d, %Y")

goal_decrease_message_templates = [
    dict(message_title=)
]