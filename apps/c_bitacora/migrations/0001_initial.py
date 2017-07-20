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
            name='BitacoraClp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cedula_new', models.IntegerField()),
                ('cedula_old', models.IntegerField()),
                ('nombres_new', models.CharField(max_length=50, null=True, blank=True)),
                ('nombres_old', models.CharField(max_length=50, null=True, blank=True)),
                ('sexo_new', models.CharField(max_length=1, null=True, blank=True)),
                ('sexo_old', models.CharField(max_length=1, null=True, blank=True)),
                ('edad_new', models.CharField(max_length=5, null=True, blank=True)),
                ('edad_old', models.CharField(max_length=5, null=True, blank=True)),
                ('tlf_new', models.CharField(max_length=11, null=True, blank=True)),
                ('tlf_old', models.CharField(max_length=11, null=True, blank=True)),
                ('fecha_update', models.DateTimeField(auto_now=True, null=True)),
                ('user_update', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
