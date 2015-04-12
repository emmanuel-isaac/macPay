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
                ('date', models.DateField(default=datetime.datetime(2015, 4, 12, 9, 50, 58, 547477))),
                ('sum_paid', models.PositiveIntegerField()),
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
                ('plan_duration', models.CharField(max_length=5, choices=[(b'12', b'12'), (b'24', b'24'), (b'36', b'36'), (b'48', b'48')])),
                ('date_created', models.DateField(default=datetime.datetime(2015, 4, 12, 9, 50, 58, 546725))),
                ('fellow', models.ForeignKey(related_name='payment_plans', to='macpayuser.Fellow')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='paymenthistory',
            name='payment_plan',
            field=models.ForeignKey(to='payment.PaymentPlan'),
            preserve_default=True,
        ),
    ]
