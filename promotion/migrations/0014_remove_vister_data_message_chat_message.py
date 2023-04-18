# Generated by Django 4.1.7 on 2023-03-27 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webuser', '0041_alter_webservice_unique_field'),
        ('promotion', '0013_vister_data_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vister_data',
            name='message',
        ),
        migrations.CreateModel(
            name='chat_message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('websocket_id', models.CharField(blank=True, max_length=255, null=True)),
                ('message', models.JSONField(null=True)),
                ('name', models.CharField(max_length=500, null=True)),
                ('email', models.CharField(max_length=500, null=True)),
                ('count', models.IntegerField(default=1)),
                ('online', models.BooleanField(default=False)),
                ('rday', models.DateField(auto_now_add=True)),
                ('webservice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webuser.webservice')),
            ],
        ),
    ]
