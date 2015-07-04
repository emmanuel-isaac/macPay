# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_auto_20150703_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 7, 4, 3, 40, 17, 826088)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='sum_paid',
            field=models.DecimalField(null=True, max_digits=100, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymentplan',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2015, 7, 4, 3, 40, 17, 825632)),
            preserve_default=True,
        ),
    ]
