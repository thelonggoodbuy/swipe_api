# Generated by Django 3.2.21 on 2023-10-03 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
