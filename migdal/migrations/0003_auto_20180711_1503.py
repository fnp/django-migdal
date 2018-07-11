# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-07-11 15:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('migdal', '0002_auto_20180710_0849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='gallery',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='gallery',
        ),
        migrations.AddField(
            model_name='photo',
            name='entry',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='migdal.Entry'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(default=0, upload_to=b'entry/photo/', verbose_name='image'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='PhotoGallery',
        ),
    ]
