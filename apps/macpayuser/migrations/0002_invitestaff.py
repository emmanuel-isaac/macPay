# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('macpayuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteStaff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invite_id', models.CharField(max_length=30)),
                ('username', models.EmailField(max_length=75)),
                ('password', models.CharField(max_length=30)),
                ('date_created', models.DateTimeField()),
                ('expiry_date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
