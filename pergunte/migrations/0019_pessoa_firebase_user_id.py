# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 23:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pergunte', '0018_perguntarespondida_data_hora_resposta'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoa',
            name='firebase_user_id',
            field=models.CharField(max_length=100, null=True, verbose_name='Firebase ID'),
        ),
    ]
