from django.conf import settings
from django.db import models
from django.db.models import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver

import zipfile
import os


#main webpage
class temp_type(models.Model):

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=True, unique=False, max_length=20)


#main webpage
class template(models.Model):

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=True, unique=False, max_length=20)
    photo = models.FileField(upload_to='file/webimage', null = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    show = models.FileField(upload_to='file/view', null = True)
    temp_type = models.ManyToManyField(temp_type)
    code = models.CharField(null=True, unique=False, max_length=20)

#web type
class web_templates(models.Model):

    id = models.AutoField(primary_key=True, unique=True)
    temp_type = models.ManyToManyField(temp_type)
    template = models.ForeignKey(template, on_delete=CASCADE, blank=True, null=True)
    name = models.CharField(null=True, unique=False, max_length=20)
    photo = models.FileField(upload_to='file/webimage', null = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    deploy = models.FileField(upload_to='file/deploy', null = True)
    show = models.FileField(upload_to='file/view', null = True)
    code = models.CharField(null=True, unique=False, max_length=20)


@receiver(post_save, sender=web_templates)
def set_up_wensite(sender, instance, created, **kwargs):
  if created:
    parent_dir = "/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/"
  
    path = os.path.join(parent_dir, str(instance.id))
    
    os.mkdir(path)

    with zipfile.ZipFile(instance.show, 'r') as zip_ref:
        zip_ref.extractall(parent_dir+str(instance.id)+"/")


class template_type(models.Model):

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=True, unique=False, max_length=20)
    price = models.CharField(null=True, unique=False, max_length=20)
    web_templates = models.ForeignKey(web_templates, on_delete=CASCADE, blank=True, null=True)
    show = models.FileField(upload_to='file/view', null = True)
    offer  =  models.JSONField(null=True)
    

class template_name(models.Model):
  id = models.AutoField(primary_key=True, unique=True)
  web_templates = models.ForeignKey(web_templates, on_delete=CASCADE, blank=True, null=True)
  temp_name = models.CharField(null=True, unique=False, max_length=20)
  json_name = models.CharField(null=True, unique=False, max_length=20)
  
