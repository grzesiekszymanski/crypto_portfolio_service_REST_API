# Generated by Django 4.2.1 on 2023-06-21 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
