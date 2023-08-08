# Generated by Django 3.2.20 on 2023-08-07 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0003_auto_20230801_1006'),
        ('ads', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accomodation',
            name='house',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='houses.house'),
            preserve_default=False,
        ),
    ]
