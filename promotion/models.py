from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import json
from schedule.models import Event as SchedulerEvent
from webuser.models import webservice as webservice
from django.db.models import CASCADE
from django_countries.fields import CountryField
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async



class connection_setup(models.Model):
    websocket_id = models.CharField(max_length=255, blank=True, null=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    online = models.BooleanField(default=False)
    rday = models.DateField(auto_now_add=True)

class daily_data(models.Model):
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    count = models.IntegerField(default=1)
    time_stamp  =  models.JSONField(null=True)
    rday = models.DateField(auto_now_add=True)

class country_data(models.Model):
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    cantry = models.CharField(null=True, unique=False, max_length=500)
    cun = CountryField(null = True)
    count = models.IntegerField(default=1)
    rday = models.DateField(auto_now_add=True)

class refral_data(models.Model):
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    ref = models.CharField(null=True, unique=False, max_length=500)
    count = models.IntegerField(default=1)
    rday = models.DateField(auto_now_add=True)


class chat_message(models.Model):
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    websocket_id = models.CharField(max_length=255, blank=True, null=True)
    message  =  models.JSONField(null=True)
    name = models.CharField(null=True, unique=False, max_length=500)
    email = models.CharField(null=True, unique=False, max_length=500)
    count = models.IntegerField(default=1)
    online = models.BooleanField(default=False)
    newmes = models.BooleanField(default=False)
    openmessage = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    rday = models.DateTimeField(auto_now_add=True)

class message_setup(models.Model):
    websocket_id = models.CharField(max_length=255, blank=True, null=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    chat_message = models.ForeignKey(chat_message, on_delete=CASCADE, blank=True, null=True)
    online = models.BooleanField(default=False)
    rday = models.DateField(auto_now_add=True)

class vister_data(models.Model):
    websocket_id = models.CharField(max_length=255, blank=True, null=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    ref = models.CharField(null=True, unique=False, max_length=500)
    country = models.CharField(null=True, unique=False, max_length=200)
    cun = CountryField(null = True)
    count = models.IntegerField(default=1)
    ip = models.CharField(null=True, unique=False, max_length=200)
    location = models.CharField(null=True, unique=False, max_length=200)
    online = models.BooleanField(default=False)
    time = models.CharField(null=True, unique=False, max_length=200)
    rday = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            gbhn = connection_setup.objects.get(webservice = self.webservice,online = True)
            gbhn.save()
        except connection_setup.DoesNotExist:
            pass
        try:
            payme = daily_data.objects.get(webservice = self.webservice, rday = self.rday)
            onlindat = vister_data.objects.filter(rday = self.rday, online = True)
            currentDateAndTime = datetime.now()
            dat = [len(onlindat), str(currentDateAndTime.strftime("%H:%M"))]
            payme.time_stamp['data'].append(dat)
            if self.online:
                payme.count += 1
            payme.save()
        except daily_data.DoesNotExist:
            onlindat = vister_data.objects.filter(rday = self.rday, online = True)
            currentDateAndTime = datetime.now()
            dat = [len(onlindat), str(currentDateAndTime.strftime("%H:%M"))]
            payme = daily_data.objects.create(webservice = self.webservice)#, time_stamp = {'data':dat})
            payme.time_stamp={'data':dat}
            payme.save()

        if self.online:

            try:
                payme11 = country_data.objects.get(webservice = self.webservice, cantry = self.country)
                payme11.count += 1
                payme11.save()
            except country_data.DoesNotExist:
                payme11 = country_data.objects.create(webservice = self.webservice, cun = self.cun,cantry = self.country)

            if self.ref != '':
                try:
                    payme22 = refral_data.objects.get(webservice = self.webservice, ref = self.ref)
                    payme22.count += 1
                    payme22.save()
                except refral_data.DoesNotExist:
                    payme22 = refral_data.objects.create(webservice = self.webservice,ref = self.ref)
            else:
                try:
                    payme22 = refral_data.objects.get(webservice = self.webservice, ref = "Direct")
                    payme22.count += 1
                    payme22.save()
                except refral_data.DoesNotExist:
                    payme22 = refral_data.objects.create(webservice = self.webservice,ref = "Direct")    

         
