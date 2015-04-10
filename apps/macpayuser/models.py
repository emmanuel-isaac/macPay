from django.db import models
from django.contrib.auth.models import UserManager, User as DjangoUser


from apps.computer.models import Computer
from apps.payment.models import PaymentPlan

# Create your models here.

DjangoUser._meta.get_field('first_name').max_length=50
DjangoUser._meta.get_field('last_name').max_length=50
DjangoUser._meta.get_field('email').max_length=100
DjangoUser._meta.get_field('username').max_length=100
DjangoUser._meta.get_field('is_staff').default=True
DjangoUser._meta.get_field('is_superuser').default=True



class StaffUser(models.Model):
    user = models.OneToOneField(DjangoUser)

    def __str__(self):
        return '{}'.format(self.user.username)


class Fellow(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    payment_start_date = models.DateField(null=True)
    computer = models.ForeignKey(Computer)
    payment_plan = models.ForeignKey(PaymentPlan)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
