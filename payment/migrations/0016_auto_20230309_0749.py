# Generated by Django 3.2.6 on 2023-03-09 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0015_discount_main_payment_made_payment_made_item_payment_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment_made_item',
            name='payment_request',
        ),
        migrations.AddField(
            model_name='payment_made_item',
            name='payment_made',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.payment_made'),
        ),
    ]
