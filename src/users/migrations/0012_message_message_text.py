# Generated by Django 3.2.20 on 2023-07-31 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_delete_agent'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_text',
            field=models.TextField(default='default text'),
            preserve_default=False,
        ),
    ]
