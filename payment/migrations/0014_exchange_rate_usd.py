# Generated by Django 3.2.6 on 2023-03-04 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0013_payment_request_valid'),
    ]

    operations = [
        migrations.CreateModel(
            name='exchange_rate_usd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('rday', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
