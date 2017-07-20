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
                ('p_nombre_old', models.CharField(max_length=50)),
                ('s_nombre_old', models.CharField(max_length=50, null=True, blank=True)),
                ('p_apellido_old', models.CharField(max_length=50)),
                ('s_apellido_old', models.CharField(max_length=50, null=True, blank=True)),
                ('twitter_old', models.CharField(max_length=50, null=True, blank=True)),
                ('telefono_old', models.CharField(max_length=11)),
                ('cedula_new', models.IntegerField()),
                ('p_nombre_new', models.CharField(max_length=50)),
                ('s_nombre_new', models.CharField(max_length=50, null=True, blank=True)),
                ('p_apellido_new', models.CharField(max_length=50)),
                ('s_apellido_new', models.CharField(max_length=50, null=True, blank=True)),
                ('twitter_new', models.CharField(max_length=50, null=True, blank=True)),
                ('telefono_new', models.CharField(max_length=11)),
                ('cod_ubch_old', models.IntegerField()),
                ('cod_ubch_new', models.IntegerField()),
                ('fecha_update', models.DateTimeField(auto_now=True, null=True)),
                ('user_update', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
