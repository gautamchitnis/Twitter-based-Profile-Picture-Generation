# Generated by Django 4.0.4 on 2022-05-26 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pfpwithfriends', '0006_membertags_grouptags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pfp',
            name='user',
        ),
    ]
