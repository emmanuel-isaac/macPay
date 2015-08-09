# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20150703_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentplan',
            name='fellow',
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 7, 3, 17, 22, 36, 588643)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='fellow',
            field=models.ForeignKey(to='macpayuser.Fellow'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymentplan',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2015, 7, 3, 17, 22, 36, 588182)),
            preserve_default=True,
        ),
    ]
