from django.db import models
import datetime


# Create your models here.


class PaymentPlan(models.Model):
    plan_duration = models.PositiveSmallIntegerField(blank=False)
    fellow = models.ForeignKey('macpayuser.Fellow', related_name='payment_plans')
    date_created = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        return '{} - {} {}'.format(self.plan_duration, self.fellow.first_name, self.fellow.last_name)

    def get_months_left_on_plan(self):
        number_of_payments = self.payments.all().count()
        months_left = int(self.plan_duration) - number_of_payments
        return months_left

    months_left_on_plan = property(get_months_left_on_plan)


class PaymentHistory(models.Model):

    fellow = models.ForeignKey('macpayuser.Fellow', related_name='payment_histories')
    date = models.DateField(default=datetime.datetime.now())
    sum_paid = models.DecimalField(null=False, blank=False, max_digits=100, decimal_places=2)
    payment_plan = models.ForeignKey(PaymentPlan, null=False, blank=False, related_name='payments')

    def __str__(self):
        return '{} - {} paid the sum of {}'.format(self.date, self.fellow, self.sum_paid)
