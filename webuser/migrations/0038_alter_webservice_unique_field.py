# Generated by Django 4.1.7 on 2023-03-23 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webuser', '0037_alter_webservice_unique_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webservice',
            name='unique_field',
            field=models.CharField(default='31be5fb95e6946b9a39517e6573ffb42', editable=False, max_length=32, unique=True),
        ),
    ]
