# Generated by Django 4.2.3 on 2023-08-07 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cryptocurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.CharField(default=0)),
                ('amount', models.CharField(default=0)),
                ('worth', models.CharField(default=0)),
                ('total_profit_loss', models.CharField(default=0)),
                ('total_profit_loss_percent', models.CharField(default=0)),
                ('profit_loss_24h', models.CharField(default=0)),
                ('profit_loss_percent_24h', models.CharField(default=0)),
                ('participation_in_portfolio', models.CharField(default=0)),
                ('date', models.CharField(default='', max_length=25)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crypto', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
