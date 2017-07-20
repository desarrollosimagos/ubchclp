# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datos', '0003_datos_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='datos',
            name='grupo_usuario',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
