from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
from celery.task import periodic_task
from django.conf import settings
from calfit.helper_methods import *
from django.core.mail import send_mail


@periodic_task(run_every=crontab(hour=8, minute=0))
def notification_every_morning():
    today_date = timezone.now().date()
    users = User.objects.all()
    for user in users:
        if is_new_user(user, today_date):
            continue

        past_steps, past_goals = get_past_steps_and_goals(user, today_date)
        if len(past_steps) <= 4:
            send_mail(subject="[Calfit] Data Update Reminder",
                      message="Hi {username}! We have not had your activity data for {num_days} days. Are you okay?"
                      .format(username=user.username, num_days=7-len(past_steps)),
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[user.email,] + RESEARCHERS_EMAIL_LIST,
                      fail_silently=False # FIXME: When online this should be changed to "True"
                      )
    return


@periodic_task(run_every=crontab(hour=23, minute=00))
def update_data_every_night():
    # TODO: Update date from Wearable Device
    return