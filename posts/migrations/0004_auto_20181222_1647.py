# Generated by Django 2.1.2 on 2018-12-22 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20181206_2134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='sub',
            new_name='subreddit',
        ),
    ]
