# Generated by Django 2.2.1 on 2019-05-17 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20190517_0205'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_ask',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='can_tell',
            field=models.BooleanField(default=False),
        ),
    ]