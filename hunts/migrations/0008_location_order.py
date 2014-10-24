# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hunts', '0007_auto_20141024_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
