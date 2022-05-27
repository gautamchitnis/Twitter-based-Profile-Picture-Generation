# Generated by Django 4.0.4 on 2022-05-26 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pfpwithfriends', '0005_alter_group_creator'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags', models.CharField(max_length=10000)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfpwithfriends.groupmember')),
            ],
        ),
        migrations.CreateModel(
            name='GroupTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags', models.CharField(max_length=10000)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfpwithfriends.group')),
            ],
        ),
    ]
