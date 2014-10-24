# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hunts', '0005_auto_20141024_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='treasurehunt',
            name='entryfee',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
