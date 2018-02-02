# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-01 09:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shoplist', '0003_auto_20180131_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='amount',
            field=models.IntegerField(help_text='Количество товара', verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='category',
            field=models.ForeignKey(help_text='Категория товара', on_delete=django.db.models.deletion.CASCADE, to='shoplist.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='name',
            field=models.CharField(help_text='Название товара', max_length=250, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='priority',
            field=models.ForeignKey(help_text='Приориет покупки товара', on_delete=django.db.models.deletion.CASCADE, to='shoplist.Priority', verbose_name='Приоритет'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='purchased',
            field=models.BooleanField(help_text='Товар куплен?', verbose_name='Куплен?'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='unit',
            field=models.ForeignKey(help_text='Единица измерения', on_delete=django.db.models.deletion.CASCADE, to='shoplist.Unit', verbose_name='Ед. изм.'),
        ),
    ]