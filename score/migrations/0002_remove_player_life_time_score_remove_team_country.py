# Generated by Django 4.1.3 on 2022-12-07 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("score", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="player",
            name="life_time_score",
        ),
        migrations.RemoveField(
            model_name="team",
            name="country",
        ),
    ]