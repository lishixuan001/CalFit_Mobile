from django.utils import timezone
from calfit.models import *
from calfit.calc import *
from enum import Enum
import time, re

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

    for i in range(6, -1, -1):
        past_date = today_date - timezone.timedelta(days=i+1)
        date_past_steps = date_past_goal = 0

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

def steps_updated_in_last_three_days(user, today_date):
    """
    :param user: Current Logged In User
    :param today_date: Today's Date
    :return: [bool] -> if steps data were uploaded to cloud in last consecutive three days
    """
    lost_count = 0
    for i in range(3):
        past_date = today_date - timezone.timedelta(days=i+1)
        past_record_exist = Record.objects.filter(user=user, date=past_date).exists()
        if not past_record_exist:
            lost_count += 1
    return lost_count < 3

class HistoryRecord:
    def __init__(self, date, steps, goal):
        self.date = timezone.datetime.strftime(date, "%m/%d") # 02/14
        self.steps = steps
        self.goal = goal

class MessageType:
    PLAINTEXT = 0
    INTERACTIVE = 1

class MessageTitle:
    REMINDER = "Reminder"
    SURVEY = "Progress Survey"

class MessageStruct:
    def __init__(self, title, content, type, message_respond_yes, message_respond_no):
        self.title = title
        self.content = content
        self.type = type
        self.message_respond_yes = message_respond_yes
        self.message_respond_no = message_respond_no

GOAL_DECREASE_MESSAGE_TEMPLATES = [
    dict(
        message_content="Have you let everyone around you know that you are trying to become more active so that they can help you meet your goal?",
        message_respond_yes="Nice work!",
        message_respond_no="Let others know your activity goal",
    ),
    dict(
        message_content="Do you take time to reflect on the progress you have made since beginning this study?",
        message_respond_yes="You're on the right track!",
        message_respond_no="Remind yourself of your progress every day!",
    ),
    dict(
        message_content="If you lose motivation to stay physically active, do you have a support system to help you stay motivated?",
        message_respond_yes="Nothing can stop you now!",
        message_respond_no="When you lose motivation, ask a friend or family member to help you get back on track. Remind yourself of your progress every day!",
    ),
    dict(
        message_content="If it's hard to achieve your weekly goal, you can break it up into smaller chunks of time during the day. Are you able to take a 20 minute walk in the next 2 hours?",
        message_respond_yes="Wonderful! Great job!",
        message_respond_no="Try just a 10 minute walk. You can do this!",
    ),
    dict(
        message_content="Have you set a regular time to exercise every day?",
        message_respond_yes="Now you've got it!",
        message_respond_no="Set a regular time to exercise. It makes it easier to meet your goal!",
    ),
    dict(
        message_content="Many people become physically INACTIVE on weekends. A key wqeis to plan physical activity ahead of time. Can you take a 60 minute walk this weekend?",
        message_respond_yes="I'm proud of you!",
        message_respond_no="How about a 30 minute walk this weekend? You can do it!",
    ),
    dict(
        message_content="Do you remind yourself about the changes that you want to make in your physical health?",
        message_respond_yes="Keep up the good work!",
        message_respond_no="Think about how you will feel physically when you get more exercise.",
    ),
]

STEP_DATA_UPLOAD_3_DAY_REMINDER = "We have not had your activity data for 3 days. Are you okay?"

# TODO -- Email List
RESEARCHERS_EMAIL_LIST = ["calfit.system@gmail.com"]
# RESEARCHERS_EMAIL_LIST = ["Yoshimi.Fukuoka@ucsf.edu"]