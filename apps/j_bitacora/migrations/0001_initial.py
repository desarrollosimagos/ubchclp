# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bitacora',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cedula_old', models.IntegerField()),
                ('nombre_old', models.CharField(max_length=50)),
                ('telefono_old', models.CharField(max_length=11)),
                ('cedula_new', models.IntegerField()),
                ('nombre_new', models.CharField(max_length=50)),
                ('telefono_new', models.CharField(max_length=11)),
                ('fecha_update', models.DateTimeField(auto_now=True, null=True)),
                ('user_update', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
