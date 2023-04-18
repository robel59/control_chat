# Generated by Django 3.2.6 on 2023-03-03 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webuser', '0015_promo_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo_type',
            name='per_user',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='promo_type',
            name='valid',
            field=models.BooleanField(default=False),
        ),
    ]
