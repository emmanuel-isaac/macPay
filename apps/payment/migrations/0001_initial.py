# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('macpayuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.datetime(2015, 5, 10, 22, 20, 11, 951398))),
                ('sum_paid', models.DecimalField(max_digits=100, decimal_places=2)),
                ('fellow', models.ForeignKey(related_name='payment_histories', to='macpayuser.Fellow')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plan_duration', models.PositiveIntegerField()),
                ('date_created', models.DateField(default=datetime.datetime(2015, 5, 10, 22, 20, 11, 950652))),
                ('fellow', models.ForeignKey(related_name='payment_plans', to='macpayuser.Fellow')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='paymenthistory',
            name='payment_plan',
            field=models.ForeignKey(related_name='payments', to='payment.PaymentPlan'),
            preserve_default=True,
        ),
    ]
