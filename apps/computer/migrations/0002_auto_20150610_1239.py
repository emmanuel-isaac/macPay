# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('computer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComputerImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('secure_url', models.URLField(default=b'https://res.cloudinary.com/coder/image/upload/v1433933523/mac-pic-2015-06-1010:52:01.920384.jpg', max_length=500)),
                ('public_id', models.TextField(default=b'mac-pic-2015-06-1010:52:01.920384')),
                ('height', models.IntegerField(default=300)),
                ('width', models.IntegerField(default=300)),
                ('original_filename', models.TextField(default=b'mac-pic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='computer',
            name='comp_img',
            field=models.OneToOneField(null=True, to='computer.ComputerImage'),
            preserve_default=True,
        ),
    ]
