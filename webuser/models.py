from django.conf import settings
from django.db.models import CASCADE
from django.db import models
from website.models import *
import json
import uuid

class notiffication(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null = True)
    name = models.CharField(null=True, unique=False, max_length=20)
    info = models.TextField(null=True)
    active = models.BooleanField(default=True)
    rday = models.DateTimeField(auto_now_add=True)

class webservice(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null = True)
    unique_field = models.CharField(max_length=32,unique=True,default=uuid.uuid4().hex,editable=False)
    temp_type = models.ForeignKey(temp_type, on_delete=CASCADE, blank=True, null=True)
    name = models.CharField(null=True, unique=False, max_length=20)
    port = models.CharField(null=True, unique=False, max_length=20)
    dname = models.CharField(null=True, unique=False, max_length=100)
    sbdname = models.CharField(null=True, unique=False, max_length=100)
    web_templates = models.ForeignKey(web_templates, on_delete=CASCADE, blank=True, null=True)
    template_type = models.ForeignKey(template_type, on_delete=CASCADE, blank=True, null=True)
    deploy = models.FileField(upload_to='file/deploy', null = True)
    state = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    active_pay = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    eday = models.DateTimeField(null=True)
    rday = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=webservice)
def set_up_wensite(sender, instance, created, **kwargs):
  if created:
    web = instance
    web.deploy = web.web_templates.deploy
    web.save()

    parent_dir = "/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/"
    path = os.path.join(parent_dir, web.name)
    os.mkdir(path)
    pathname = parent_dir+str(web.name)+"/web/"
    with zipfile.ZipFile(web.deploy, 'r') as zip_ref:
        zip_ref.extractall(pathname)
    
    temp = template_name.objects.filter(web_templates = web.web_templates)
    for i in temp:
        with open(pathname + i.json_name) as file:
            data = json.load(file)
        webservice_template.objects.create(template_name = i, webservice = web, Jsonfield = data, name = i.json_name)


class store_data(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    data  =  models.JSONField(null=True)
    rday = models.DateTimeField(auto_now_add=True)

class user_data(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    data  =  models.JSONField(null=True)
    rday = models.DateTimeField(auto_now_add=True)


class webservice_template(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    template_name = models.ForeignKey(template_name, on_delete=CASCADE, blank=True, null=True)
    Jsonfield  =  models.JSONField(null=True)
    name = models.CharField(null=True, unique=False, max_length=20)

class promo_type(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=True, unique=False, max_length=200)
    cost = models.DecimalField(null = True, max_digits = 15,decimal_places = 2)
    per_user = models.DecimalField(null = True, max_digits = 15,decimal_places = 2)
    info = models.TextField(null=True)
    valid = models.BooleanField(default=False)
    rday = models.DateTimeField(auto_now_add=True)

class promo_service(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    promo_type = models.ForeignKey(promo_type, on_delete=CASCADE, blank=True, null=True)
    info = models.TextField(null=True)
    rday = models.DateTimeField(auto_now_add=True)

class promo_selected(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    promo_type = models.ForeignKey(promo_type, on_delete=CASCADE, blank=True, null=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    cost = models.DecimalField(null = True, max_digits = 15,decimal_places = 2)
    info = models.TextField(null=True)
    rday = models.DateTimeField(auto_now_add=True)

class search_word(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=True, unique=False, max_length=200)
    promo_selected = models.ForeignKey(promo_selected, on_delete=CASCADE, blank=True, null=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)

class email_type(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=True, unique=False, max_length=200)
    cost = models.DecimalField(null = True, max_digits = 15,decimal_places = 2)
    info = models.TextField(null=True)
    rday = models.DateTimeField(auto_now_add=True)


class selected_email(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    email_type = models.ForeignKey(email_type, on_delete=CASCADE, blank=True, null=True)
    cost = models.DecimalField(null = True, max_digits = 15,decimal_places = 2)
    valid = models.BooleanField(default=False)
    info = models.TextField(null=True)
    rday = models.DateTimeField(auto_now_add=True)

class domainname_cost(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    cost = models.DecimalField(null = True, max_digits = 15,decimal_places = 2)
    name = models.CharField(null=True, unique=False, max_length=200)
    rday = models.DateTimeField(auto_now_add=True)


class domainname_list(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    name = models.CharField(null=True, unique=False, max_length=200)
    rday = models.DateTimeField(auto_now_add=True)


class domainname_found_list(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    name = models.CharField(null=True, unique=False, max_length=200)
    cost = models.DecimalField(null = True, max_digits = 15,decimal_places = 2)
    valid = models.BooleanField(default=False)
    info = models.TextField(null=True)
    rday = models.DateTimeField(auto_now_add=True)

class domainname_selected(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    domainname_found_list = models.ForeignKey(domainname_found_list, on_delete=CASCADE, blank=True, null=True)
    name = models.CharField(null=True, unique=False, max_length=20)
    rday = models.DateTimeField(auto_now_add=True)


class payment_type(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=True, unique=False, max_length=20)
    nodays = models.IntegerField(null=True, unique=False)
    rate = models.DecimalField(null = True, max_digits = 5,decimal_places = 4)

class discount(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=True, unique=False, max_length=20)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    rate = models.DecimalField(null = True, max_digits = 5,decimal_places = 4)
    valid = models.BooleanField(default=False)
    eday = models.DateTimeField(null = True)
    rday = models.DateTimeField(auto_now_add=True)


class payment_way(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=True, unique=False, max_length=20)

class service_payment(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    payment_type = models.ForeignKey(payment_type, on_delete=CASCADE, blank=True, null=True)
    amount = models.DecimalField(null = True, max_digits = 15,decimal_places = 2)
    next_payment = models.DateTimeField(null=True)
    rday = models.DateTimeField(auto_now_add=True)

class payment_confermation(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    service_payment = models.ForeignKey(service_payment, on_delete=CASCADE, blank=True, null=True)
    payment_way = models.ForeignKey(payment_way, on_delete=CASCADE, blank=True, null=True)
    amount = models.DecimalField(null = True, max_digits = 5,decimal_places = 4)
    rday = models.DateTimeField(auto_now_add=True)


class add_type(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=True, unique=False, max_length=20)

class selected_add(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    add_type = models.ForeignKey(add_type, on_delete=CASCADE, blank=True, null=True)
    payment_way = models.ForeignKey(payment_way, on_delete=CASCADE, blank=True, null=True)
    cost = models.DecimalField(null = True, max_digits = 5,decimal_places = 4)
    stared = models.DateTimeField(null=True)
    ended = models.DateTimeField(null=True)
    rday = models.DateTimeField(auto_now_add=True)

class add_payment_confermation(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    selected_add = models.ForeignKey(selected_add, on_delete=CASCADE, blank=True, null=True)
    payment_way = models.ForeignKey(payment_way, on_delete=CASCADE, blank=True, null=True)
    amount = models.DecimalField(null = True, max_digits = 5,decimal_places = 4)
    rday = models.DateTimeField(auto_now_add=True)