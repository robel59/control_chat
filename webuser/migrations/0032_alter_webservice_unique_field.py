# Generated by Django 3.2.6 on 2023-03-18 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webuser', '0031_alter_webservice_unique_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webservice',
            name='unique_field',
            field=models.CharField(default='b79aba5bd223457ab743d55363d74791', editable=False, max_length=32, unique=True),
        ),
    ]
