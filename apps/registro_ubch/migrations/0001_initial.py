# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UnoPorDiez',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cedula', models.IntegerField(unique=True)),
                ('p_nombre', models.CharField(max_length=50)),
                ('s_nombre', models.CharField(max_length=50, null=True, blank=True)),
                ('p_apellido', models.CharField(max_length=50)),
                ('s_apellido', models.CharField(max_length=50, null=True, blank=True)),
                ('cod_ubch', models.IntegerField()),
                ('cedula_jefe', models.IntegerField()),
                ('twitter', models.CharField(max_length=50, null=True, blank=True)),
                ('direcc_p', models.TextField(null=True, blank=True)),
                ('telefono', models.CharField(max_length=11)),
                ('estado', models.IntegerField(null=True, blank=True)),
                ('municipio', models.IntegerField(null=True, blank=True)),
                ('parroquia', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
