# Generated by Django 2.1.5 on 2019-02-04 16:12

import django.core.validators
from django.db import migrations
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20190203_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=django_bleach.models.BleachField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=django_bleach.models.BleachField(validators=[django.core.validators.MaxLengthValidator(150, message='The title can only be 150 characters in length.')]),
        ),
    ]
