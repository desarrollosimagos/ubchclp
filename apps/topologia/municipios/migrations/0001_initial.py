# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estados', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('municipio', models.CharField(max_length=50, verbose_name=b'Municipio')),
                ('cod_municipio', models.IntegerField(null=True)),
                ('user', models.CharField(max_length=15, null=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_update', models.DateTimeField(auto_now=True, null=True)),
                ('estado', models.ForeignKey(related_name='estado_municipio', on_delete=django.db.models.deletion.SET_NULL, to_field=b'cod_estado', to='estados.Estado', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
