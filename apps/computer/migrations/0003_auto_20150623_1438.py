# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('computer', '0002_auto_20150610_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computerimage',
            name='height',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='computerimage',
            name='original_filename',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='computerimage',
            name='public_id',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='computerimage',
            name='secure_url',
            field=models.URLField(max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='computerimage',
            name='width',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
