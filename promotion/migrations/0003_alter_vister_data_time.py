# Generated by Django 3.2.6 on 2023-03-15 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0002_auto_20230315_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vister_data',
            name='time',
            field=models.CharField(max_length=200, null=True),
        ),
    ]