# Generated by Django 4.1.7 on 2023-03-23 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webuser', '0035_alter_webservice_unique_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webservice',
            name='unique_field',
            field=models.CharField(default='64073348c41f485881e47b02d82f5f66', editable=False, max_length=32, unique=True),
        ),
    ]
