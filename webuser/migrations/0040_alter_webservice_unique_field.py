# Generated by Django 4.1.7 on 2023-03-26 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webuser', '0039_alter_webservice_unique_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webservice',
            name='unique_field',
            field=models.CharField(default='64ff30f4d29343528b2d959bd3531e85', editable=False, max_length=32, unique=True),
        ),
    ]
