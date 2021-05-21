# Generated by Django 2.2.7 on 2021-05-20 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_beneficiary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donor',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='users',
            name='can_donate',
        ),
        migrations.AddField(
            model_name='users',
            name='phone_number',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
