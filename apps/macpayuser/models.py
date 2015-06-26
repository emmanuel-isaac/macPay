from django.db import models
from django.contrib.auth.models import UserManager, User as DjangoUser
import datetime
from dateutil.relativedelta import relativedelta

from apps.computer.models import Computer
from apps.payment.models import PaymentPlan
from apps.payment.models import PaymentHistory

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


class InviteStaff(DjangoUser):
    invite_id = models.CharField(max_length=50)
    date_created = models.DateTimeField()
    expiry_date = models.DateTimeField()

    def __unicode__(self):
        return self.username


class Fellow(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    computer = models.ForeignKey(Computer, blank=True, null=True)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_payment_start_date(self):
        try:
            start_date = self.payment_histories.first().date
            return start_date
        except AttributeError, e:
            e = '--'
            return e

    payment_start_date = property(get_payment_start_date)

    def get_recent_payment_plan(self):
        try:
            payment_plan = self.payment_plans.last()
            return payment_plan
        except AttributeError, e:
            e = '--'
            return e

    recent_payment_plan = property(get_recent_payment_plan)

    def get_last_plan_change_date(self):
        try:
            last_plan_change_date = self.payment_plans.last().date_created
            return last_plan_change_date
        except AttributeError, e:
            e = '--'
            return e
        

    last_plan_change_date = property(get_last_plan_change_date)

    def get_amount_paid(self, filter=None):
        amount_paid = 0
        obj = self.payment_histories.all()
        if filter==None:
            if obj:
                for item in obj:
                    amount_paid = amount_paid + item.sum_paid
                    continue
            else:
                amount_paid = '--'
        else:
            try:
                current_obj = self.payment_histories.filter(date=filter)
                current_obj_id = current_obj[0].id
                for item in obj:
                    if item.id < current_obj_id:
                        amount_paid = amount_paid + item.sum_paid
                    continue
            except Exception, e:
                amount_paid = '--'
            
        return amount_paid

    def get_amount_paid_before_plan_change(self):
        amount_paid = self.get_amount_paid(self.last_plan_change_date)
        return amount_paid

    amount_paid = property(get_amount_paid)
    amount_paid_before_plan_change = property(get_amount_paid_before_plan_change)

    def get_due_balance(self):
        amount = self.amount_paid
        if amount != '--':
            computer_cost = self.computer.cost
            return computer_cost - amount
        else:
            return amount

    due_balance = property(get_due_balance)

    def get_monthly_payment(self):
        # monthly payment at any point 
        # should be the balance at that point divided by the number of months left on the plan
        if self.payment_histories.all():
            balance = self.due_balance
            number_of_months_left = self.recent_payment_plan.months_left_on_plan
            monthly_payment = 0
            if number_of_months_left > 0:
                monthly_payment = float(balance) / float(number_of_months_left)
            return round(monthly_payment, 2)
        elif self.computer and self.recent_payment_plan != '--':
            monthly_payment = float(self.computer.cost) / float(self.recent_payment_plan.months_left_on_plan)
            return round(monthly_payment, 2)
        else:
            return '--'

    monthly_payment = property(get_monthly_payment)


    def get_tentative_payment_end(self):
        last_plan_change_date = self.last_plan_change_date
        recent_payment_plan = self.recent_payment_plan
        tentative_payment_end = last_plan_change_date + relativedelta(months=int(recent_payment_plan.plan_duration))
        return tentative_payment_end

    
    tentative_payment_end = property(get_tentative_payment_end)
