# Generated by Django 4.2.3 on 2023-08-09 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApp', '0005_profile_streak'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='streak',
            new_name='current_streak',
        ),
        migrations.AddField(
            model_name='profile',
            name='highest_streak',
            field=models.IntegerField(default=0),
        ),
    ]
