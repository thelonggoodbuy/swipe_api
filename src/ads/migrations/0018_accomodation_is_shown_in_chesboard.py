# Generated by Django 3.2.20 on 2023-08-22 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0017_auto_20230822_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='accomodation',
            name='is_shown_in_chesboard',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
