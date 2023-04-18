# Generated by Django 3.2.6 on 2023-02-26 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_template_type_price'),
        ('webuser', '0009_webservice_temp_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='webservice',
            name='template_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.template_type'),
        ),
    ]
