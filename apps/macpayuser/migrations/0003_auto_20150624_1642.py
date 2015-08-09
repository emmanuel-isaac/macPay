# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('macpayuser', '0002_invitestaff'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invitestaff',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveField(
            model_name='invitestaff',
            name='id',
        ),
        migrations.RemoveField(
            model_name='invitestaff',
            name='password',
        ),
        migrations.RemoveField(
            model_name='invitestaff',
            name='username',
        ),
        migrations.AddField(
            model_name='invitestaff',
            name='user_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
