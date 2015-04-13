from django.db import models
import datetime


# Create your models here.


class PaymentPlan(models.Model):
    DURATION = (
        ('12', '12'),
        ('24', '24'),
        ('36', '36'),
        ('48', '48'),
    )
    plan_duration = models.CharField(choices=DURATION, blank=False, null=False, max_length=5)
    fellow = models.ForeignKey('macpayuser.Fellow', related_name='payment_plans')
    date_created = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        return '{} - {} {}'.format(self.plan_duration, self.fellow.first_name, self.fellow.last_name)


class PaymentHistory(models.Model):

    fellow = models.ForeignKey('macpayuser.Fellow', related_name='payment_histories')
    date = models.DateField(default=datetime.datetime.now())
    sum_paid = models.DecimalField(null=False, blank=False)
    payment_plan = models.ForeignKey(PaymentPlan, null=False, blank=False)

    def __str__(self):
        return '{} - {} paid the sum of {}'.format(self.date, self.fellow, self.sum_paid)

    # I have to determine the last Payment History of a particular fellow






