# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-07-10 08:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import fnpdjango.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('migdal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=b'entry/photo/', verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='PhotoGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Entry_event',
            fields=[
            ],
            options={
                'verbose_name': 'entry: events',
                'proxy': True,
                'verbose_name_plural': 'entries: events',
            },
            bases=('migdal.entry',),
        ),
        migrations.AddField(
            model_name='entry',
            name='place_en',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='place'),
        ),
        migrations.AddField(
            model_name='entry',
            name='place_pl',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='place'),
        ),
        migrations.AddField(
            model_name='entry',
            name='time_en',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='time'),
        ),
        migrations.AddField(
            model_name='entry',
            name='time_pl',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='time'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='body_en',
            field=fnpdjango.utils.fields.TextileField(blank=True, help_text='Use <a href="https://txstyle.org/article/44/an-overview-of-the-textile-syntax">Textile</a> syntax.', null=True, rendered_field=True, verbose_name='body'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='body_pl',
            field=fnpdjango.utils.fields.TextileField(blank=True, help_text='Use <a href="https://txstyle.org/article/44/an-overview-of-the-textile-syntax">Textile</a> syntax.', null=True, rendered_field=True, verbose_name='body'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='lead_en',
            field=fnpdjango.utils.fields.TextileField(blank=True, help_text='Use <a href="https://txstyle.org/article/44/an-overview-of-the-textile-syntax">Textile</a> syntax.', null=True, rendered_field=True, verbose_name='lead'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='lead_pl',
            field=fnpdjango.utils.fields.TextileField(blank=True, help_text='Use <a href="https://txstyle.org/article/44/an-overview-of-the-textile-syntax">Textile</a> syntax.', null=True, rendered_field=True, verbose_name='lead'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='type',
            field=models.CharField(choices=[(b'news', 'news'), (b'publications', 'publications'), (b'info', 'info'), (b'event', 'events')], db_index=True, max_length=16),
        ),
        migrations.AddField(
            model_name='photo',
            name='gallery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='migdal.PhotoGallery'),
        ),
        migrations.AddField(
            model_name='entry',
            name='gallery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='migdal.PhotoGallery'),
        ),
    ]
