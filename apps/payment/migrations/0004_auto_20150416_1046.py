# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20150416_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 4, 16, 10, 46, 13, 420593)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='payment_plan',
            field=models.ForeignKey(related_name='payments', to='payment.PaymentPlan'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymentplan',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2015, 4, 16, 10, 46, 13, 420084)),
            preserve_default=True,
        ),
    ]
