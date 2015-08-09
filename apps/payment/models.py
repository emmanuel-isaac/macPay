from django.db import models
from apps.macpayuser.models import Fellow
import datetime


# Create your models here.


class PaymentPlan(models.Model):
    plan_duration = models.PositiveIntegerField(blank=False)
    date_created = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        return '%s-month' % (self.plan_duration)


class PaymentHistory(models.Model):

    fellow = models.ForeignKey(Fellow)
    date = models.DateField(default=datetime.datetime.now())
    sum_paid = models.DecimalField(null=True, max_digits=100, decimal_places=2)
    previous_payment_plan = models.ForeignKey(PaymentPlan, null=False, blank=False, related_name='payments')
    current_payment_plan = models.ForeignKey(PaymentPlan, null=True, blank=False)

    def __str__(self):
        return '{} - {} paid the sum of {}'.format(self.date, self.fellow, self.sum_paid)
