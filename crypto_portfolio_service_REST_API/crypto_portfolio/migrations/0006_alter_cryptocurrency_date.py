# Generated by Django 4.2.2 on 2023-07-20 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_portfolio', '0005_alter_cryptocurrency_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocurrency',
            name='date',
            field=models.CharField(default='20/07/2023 18:11:06', max_length=25),
        ),
    ]
