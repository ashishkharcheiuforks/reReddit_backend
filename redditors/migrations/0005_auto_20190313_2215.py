# Generated by Django 2.1.6 on 2019-03-13 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redditors', '0004_auto_20181113_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
