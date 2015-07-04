# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20150510_2220'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymenthistory',
            old_name='payment_plan',
            new_name='previous_payment_plan',
        ),
        migrations.AddField(
            model_name='paymenthistory',
            name='current_payment_plan',
            field=models.ForeignKey(to='payment.PaymentPlan', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 7, 3, 16, 9, 9, 318155)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymentplan',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2015, 7, 3, 16, 9, 9, 317470)),
            preserve_default=True,
        ),
    ]
