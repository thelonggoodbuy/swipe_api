# Generated by Django 3.2.20 on 2023-08-22 13:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ads', '0015_auto_20230822_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='favorites_for',
            field=models.ManyToManyField(related_name='favourites_adds', to=settings.AUTH_USER_MODEL),
        ),
    ]
