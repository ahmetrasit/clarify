# Generated by Django 2.2.1 on 2019-05-15 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20190515_0220'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_confirmed',
            new_name='email_confirmed',
        ),
        migrations.AddField(
            model_name='user',
            name='phone_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='EmailConfirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_key', models.CharField(max_length=16)),
                ('status', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('confirmed_on', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
