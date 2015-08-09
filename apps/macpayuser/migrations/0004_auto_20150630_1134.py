# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('macpayuser', '0003_auto_20150624_1642'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invitestaff',
            options={},
        ),
        migrations.RemoveField(
            model_name='invitestaff',
            name='user_ptr',
        ),
        migrations.AddField(
            model_name='invitestaff',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invitestaff',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invitestaff',
            name='invite_id',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
