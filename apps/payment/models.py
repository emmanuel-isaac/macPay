from django.db import models

# Create your models here.


class PaymentPlan(models.Model):
    DURATION = (
        ('12', 'Twelve'),
        ('24', 'Twenty-four'),
        ('36', 'Thirty-six'),
        ('48', 'Forty-eight'),
    )
    plan_name = models.CharField(max_length=100)
    plan_duration = models.CharField(choices=DURATION, blank=False, null=False, max_length=5)

    def __str__(self):
        return '{} - {} months'.format(self.plan_name, self.plan_duration)


class PaymentHistory(models.Model):

    fellow = models.ForeignKey('macpayuser.Fellow')
    date = models.DateField()
    sum_paid = models.PositiveIntegerField(null=True)

    def __str__(self):
        return '{} - {} paid the sum of {}'.format(self.date, self.fellow, self.sum_paid)



