# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_auto_20150508_0529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 5, 9, 22, 30, 17, 366546)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymentplan',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2015, 5, 9, 22, 30, 17, 365500)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymentplan',
            name='plan_duration',
            field=models.PositiveSmallIntegerField(),
            preserve_default=True,
        ),
    ]
