# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('first_name', models.CharField(max_length=254, verbose_name='first name')),
                ('last_name', models.CharField(max_length=254, verbose_name='last_name name')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address')),
                ('phone_number', models.CharField(default=b'', max_length=20, verbose_name='phone_number', blank=True)),
                ('gender', models.CharField(default=b'', max_length=1, blank=True, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('dob', models.DateField(default=b'9999-01-01', verbose_name='dob', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]