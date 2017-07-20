# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CentroVotacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estado', models.IntegerField(null=True)),
                ('municipio', models.IntegerField(null=True)),
                ('parroquia', models.IntegerField(null=True)),
                ('id_mun', models.IntegerField(null=True)),
                ('cod_n', models.IntegerField(null=True)),
                ('cod_v', models.CharField(max_length=1500, null=True)),
                ('c_votacion', models.TextField(max_length=1500)),
                ('direccion', models.TextField(max_length=1500)),
                ('user', models.CharField(max_length=15, null=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_update', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
