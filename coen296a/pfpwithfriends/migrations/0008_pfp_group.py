# Generated by Django 4.0.4 on 2022-05-26 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pfpwithfriends', '0007_remove_pfp_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='pfp',
            name='group',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='pfpwithfriends.group'),
            preserve_default=False,
        ),
    ]
