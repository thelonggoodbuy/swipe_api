# Generated by Django 3.2.20 on 2023-07-16 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
