# Generated by Django 3.2.6 on 2023-03-03 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0012_payment_request_item_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment_request',
            name='valid',
            field=models.BooleanField(default=False),
        ),
    ]
