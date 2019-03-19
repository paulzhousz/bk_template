# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_initial_user_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='bkuser',
            name='is_enable',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u542f\u7528'),
        ),
        migrations.AddField(
            model_name='bkuser',
            name='is_in_app',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u8be5APP\u7528\u6237'),
        ),
        migrations.AlterField(
            model_name='bkuser',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='\u90ae\u7bb1', blank=True),
        ),
    ]
