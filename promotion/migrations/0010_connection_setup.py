# Generated by Django 4.1.7 on 2023-03-23 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webuser', '0038_alter_webservice_unique_field'),
        ('promotion', '0009_vister_data_online'),
    ]

    operations = [
        migrations.CreateModel(
            name='connection_setup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('websocket_id', models.CharField(blank=True, max_length=255, null=True)),
                ('online', models.BooleanField(default=False)),
                ('rday', models.DateField(auto_now_add=True)),
                ('webservice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webuser.webservice')),
            ],
        ),
    ]
