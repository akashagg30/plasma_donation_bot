# Generated by Django 2.2.7 on 2021-05-20 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20210520_2339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donor',
            name='action_time',
        ),
        migrations.AddField(
            model_name='donor',
            name='shown_time',
            field=models.DateTimeField(null=True),
        ),
    ]
