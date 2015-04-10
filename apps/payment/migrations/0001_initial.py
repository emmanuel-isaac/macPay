# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('macpayuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('sum_paid', models.PositiveIntegerField(null=True)),
                ('fellow', models.ForeignKey(to='macpayuser.Fellow')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plan_name', models.CharField(max_length=100)),
                ('plan_duration', models.CharField(max_length=5, choices=[(b'12', b'Twelve'), (b'24', b'Twenty-four'), (b'36', b'Thirty-six'), (b'48', b'Forty-eight')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
