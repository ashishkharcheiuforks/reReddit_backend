# Generated by Django 2.1.5 on 2019-02-03 18:25

from django.db import migrations
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20190203_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=django_bleach.models.BleachField(max_length=150),
        ),
    ]