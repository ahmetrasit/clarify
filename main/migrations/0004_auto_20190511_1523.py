# Generated by Django 2.2.1 on 2019-05-11 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190511_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='logins',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_logins', to='main.UserLogin'),
        ),
    ]
