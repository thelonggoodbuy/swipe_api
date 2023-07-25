# Generated by Django 3.2.20 on 2023-07-24 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_is_false_customuser_is_activated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='nontifications_status',
            field=models.CharField(choices=[('for_user', 'оповещения пользователю'), ('for_user_and_agent', 'оповещения пользователю и агенту'), ('for_agent', 'оповещению агенту'), ('disabled', 'отключить оповещения')], default='оповещения пользователю и агенту', max_length=200),
        ),
    ]
