# Generated by Django 3.2.6 on 2023-03-03 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webuser', '0016_auto_20230303_1039'),
        ('payment', '0009_payment_request_item_qunt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment_request_item',
            name='payment_type',
        ),
        migrations.AddField(
            model_name='payment_request_item',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webuser.payment'),
        ),
    ]
