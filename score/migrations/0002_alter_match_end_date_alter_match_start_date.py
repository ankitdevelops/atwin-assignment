# Generated by Django 4.1.3 on 2022-12-05 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("score", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="match",
            name="end_date",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="match",
            name="start_date",
            field=models.DateTimeField(),
        ),
    ]
