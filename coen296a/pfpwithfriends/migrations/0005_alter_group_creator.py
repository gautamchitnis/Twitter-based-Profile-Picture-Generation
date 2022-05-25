# Generated by Django 4.0.4 on 2022-05-25 07:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pfpwithfriends', '0004_alter_group_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='creator',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
