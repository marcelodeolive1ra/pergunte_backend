# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-14 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pergunte', '0007_auto_20170114_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='materias',
            field=models.ManyToManyField(blank=True, to='pergunte.Materia', verbose_name='Matérias inscritas'),
        ),
        migrations.AlterField(
            model_name='materia',
            name='perguntas',
            field=models.ManyToManyField(blank=True, to='pergunte.Pergunta', verbose_name='Perguntas'),
        ),
    ]