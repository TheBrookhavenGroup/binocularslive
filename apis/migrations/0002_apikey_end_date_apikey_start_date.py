# Generated by Django 5.0.6 on 2024-06-18 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apikey',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
