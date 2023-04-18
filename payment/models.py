from django.conf import settings
from django.db.models import CASCADE
from django.db import models
from website.models import *
from webuser.models import *
import json

#manual
class exchange_rate_usd(models.Model):
    amount = models.DecimalField(max_digits = 15,decimal_places = 2, default=0)
    rday = models.DateTimeField(auto_now_add=True)

#manual
class payment_on(models.Model):
    name = models.CharField(null=True, unique=False, max_length=20)
    rday = models.DateTimeField(auto_now_add=True)


#manual
class bank_account(models.Model):
    name = models.CharField(null=True, unique=False, max_length=20)
    account = models.CharField(null=True, unique=False, max_length=20)
    active = models.BooleanField(default=True)
    rday = models.DateTimeField(auto_now_add=True)

#auto
class auto_account(models.Model):
    name = models.CharField(null=True, unique=False, max_length=20)
    account = models.CharField(null=True, unique=False, max_length=20)
    active = models.BooleanField(default=True)
    rday = models.DateTimeField(auto_now_add=True)

#webservice payment request 
class payment_request(models.Model):
    total = models.DecimalField(max_digits = 15,decimal_places = 2, default=0)
    vat = models.DecimalField(max_digits = 15,decimal_places = 2, default=0)
    amount = models.DecimalField(max_digits = 15,decimal_places = 2, default=0)
    descount = models.DecimalField(max_digits = 15,decimal_places = 2, default=0)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    domainname_selected = models.ForeignKey(domainname_selected, on_delete=CASCADE, blank=True, null=True)
    payment_type = models.ForeignKey(payment_type, on_delete=CASCADE, blank=True, null=True)
    info = models.TextField(null=True)
    paied = models.BooleanField(default=False)
    valid = models.BooleanField(default=False)
    rday = models.DateTimeField(auto_now_add=True)

#webservice payment request 
class payment_request_item(models.Model):
    total = models.DecimalField(max_digits = 15,decimal_places = 2, default=0)
    amount = models.DecimalField(null = True, max_digits = 15,decimal_places = 2)
    qunt = models.CharField(null=True, unique=False, max_length=20)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    promo_selected = models.ForeignKey(promo_selected, on_delete=CASCADE, blank=True, null=True)#promotion selected for the website
    selected_email = models.ForeignKey(selected_email, on_delete=CASCADE, blank=True, null=True)#email selected for the website
    domainname_selected = models.ForeignKey(domainname_selected, on_delete=CASCADE, blank=True, null=True)#domain name selected
    payment_request = models.ForeignKey(payment_request, on_delete=CASCADE, blank=True, null=True)
    service_payment = models.ForeignKey(service_payment, on_delete=CASCADE, blank=True, null=True)#webservice selected
    name = models.CharField(null=True, unique=False, max_length=20)
    info = models.TextField(null=True)
    paied = models.BooleanField(default=False)
    rday = models.DateTimeField(auto_now_add=True)


class discount_main(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=True, unique=False, max_length=20)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    rate = models.DecimalField(null = True, max_digits = 5,decimal_places = 4)
    valid = models.BooleanField(default=False)
    eday = models.DateTimeField(null = True)
    rday = models.DateTimeField(auto_now_add=True)


#webservice payment request 
class payment_made(models.Model):
    total = models.DecimalField(max_digits = 15,decimal_places = 2, default=0)
    payment_on = models.ForeignKey(payment_on, on_delete=CASCADE, blank=True, null=True)
    vat = models.DecimalField(max_digits = 15,decimal_places = 2, default=0)
    amount = models.DecimalField(max_digits = 15,decimal_places = 2, default=0)
    discount_main = models.DecimalField(max_digits = 15,decimal_places = 2, default=0)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    payment_type = models.ForeignKey(payment_type, on_delete=CASCADE, blank=True, null=True)
    info = models.TextField(null=True)
    paied = models.BooleanField(default=False)
    valid = models.BooleanField(default=False)
    rday = models.DateTimeField(auto_now_add=True)

#webservice payment request 
class payment_made_item(models.Model):
    total = models.DecimalField(max_digits = 15,decimal_places = 2, default=0)
    amount = models.DecimalField(null = True, max_digits = 15,decimal_places = 2)
    qunt = models.CharField(null=True, unique=False, max_length=20)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    promo_selected = models.ForeignKey(promo_selected, on_delete=CASCADE, blank=True, null=True)#promotion selected for the website
    selected_email = models.ForeignKey(selected_email, on_delete=CASCADE, blank=True, null=True)#email selected for the website
    domainname_selected = models.ForeignKey(domainname_selected, on_delete=CASCADE, blank=True, null=True)#domain name selected
    payment_made = models.ForeignKey(payment_made, on_delete=CASCADE, blank=True, null=True)
    service_payment = models.ForeignKey(service_payment, on_delete=CASCADE, blank=True, null=True)#webservice selected
    name = models.CharField(null=True, unique=False, max_length=20)
    info = models.TextField(null=True)
    paied = models.BooleanField(default=False)
    rday = models.DateTimeField(auto_now_add=True)


class wrong_paid(models.Model):
    payment_request = models.ForeignKey(payment_request, on_delete=CASCADE, blank=True, null=True)
    webservice = models.ForeignKey(webservice, on_delete=CASCADE, blank=True, null=True)
    amount = models.DecimalField(null = True, max_digits = 15,decimal_places = 2)
    paid_amount = models.DecimalField(null = True, max_digits = 15,decimal_places = 2)
    payment_on = models.ForeignKey(payment_on, on_delete=CASCADE, blank=True, null=True)
    rday = models.DateTimeField(auto_now_add=True)


class notification_payment(models.Model):
    name = models.CharField(null=True, unique=False, max_length=20)
    info = models.TextField(null=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null = True)
    payment_request = models.ForeignKey(payment_request, on_delete=CASCADE, blank=True, null=True)
    rday = models.DateTimeField(auto_now_add=True)