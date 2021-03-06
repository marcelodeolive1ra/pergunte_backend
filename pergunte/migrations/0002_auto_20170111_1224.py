# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-11 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pergunte', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.IntegerField()),
                ('semestre', models.IntegerField()),
                ('nomeDisciplina', models.CharField(max_length=200)),
                ('codigoInscricao', models.CharField(max_length=30)),
                ('professor', models.ManyToManyField(to='pergunte.Professor')),
            ],
        ),
        migrations.CreateModel(
            name='Pergunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField()),
                ('pergunta', models.TextField()),
                ('respostaCorreta', models.CharField(max_length=1)),
                ('disponivel', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternativa', models.CharField(max_length=1)),
                ('textoResposta', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='pergunta',
            name='respostas',
            field=models.ManyToManyField(to='pergunte.Resposta'),
        ),
    ]
