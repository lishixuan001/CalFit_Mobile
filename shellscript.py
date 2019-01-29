import django
django.setup()

from calfit.models import Record
from django.contrib.auth.models import User

from django.utils import timezone

print("User Objects: ")
for user in User.objects.all():
    print("---> {}".format(user))
print("\n")

print("Record Objects: ")
for record in Record.objects.all():
    print("---> {}".format(record))
print("\n")
