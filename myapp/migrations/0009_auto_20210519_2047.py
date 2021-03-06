# Generated by Django 2.2.7 on 2021-05-19 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20210519_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='donor',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='donor',
            name='blood_group',
            field=models.CharField(max_length=3),
        ),
    ]
