# Generated by Django 3.2.6 on 2023-03-03 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_rename_payment_payment_request_item_service_payment'),
        ('webuser', '0016_auto_20230303_1039'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='payment',
            new_name='service_payment',
        ),
        migrations.RenameField(
            model_name='payment_confermation',
            old_name='payment',
            new_name='service_payment',
        ),
    ]
