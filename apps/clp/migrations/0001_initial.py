# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nac', models.CharField(default=b'V', max_length=1, verbose_name=b'Nacionalidad', choices=[(b'V', b'Venezolano'), (b'E', b'Extranjero')])),
                ('cedula', models.IntegerField()),
                ('nombres', models.CharField(max_length=150, verbose_name=b'Nombres')),
                ('sexo', models.CharField(max_length=1, null=True, verbose_name=b'Sexo', choices=[(b'M', b'Masculino'), (b'F', b'Femenino')])),
                ('edad', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=50)),
                ('nomb_centro', models.CharField(max_length=200, verbose_name=b'Nombre Agrupacion')),
                ('cod_estado', models.IntegerField()),
                ('cod_municipio', models.IntegerField()),
                ('cod_parroquia', models.IntegerField()),
                ('cod_circulo', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
