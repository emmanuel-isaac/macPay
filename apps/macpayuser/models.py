from django.db import models
from django.contrib.auth.models import UserManager, User as DjangoUser
import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import timedelta

from apps.computer.models import Computer

# Create your models here.

DjangoUser._meta.get_field('first_name').max_length = 50
DjangoUser._meta.get_field('last_name').max_length = 50
DjangoUser._meta.get_field('email').max_length = 100
DjangoUser._meta.get_field('username').max_length = 100
DjangoUser._meta.get_field('is_staff').default = True
DjangoUser._meta.get_field('is_superuser').default = True

class StaffUser(models.Model):
    user = models.OneToOneField(DjangoUser)

    def __str__(self):
        return '{}'.format(self.user.username)

class InviteStaff(models.Model):
    user = models.OneToOneField(DjangoUser)
    invite_id = models.CharField(max_length=50)
    date_created = models.DateTimeField()
    expiry_date = models.DateTimeField()

    def __unicode__(self):
        return self.user.username

class Fellow(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    computer = models.ForeignKey(Computer, blank=True, null=True)
    payment_start_date = models.DateField(null=True)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)
