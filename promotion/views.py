from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.http import HttpResponse
from .models import *
from webuser.models import *
import json
import jwt
from django.core.files.storage import FileSystemStorage
import os
from PIL import Image
import shutil
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.storage import default_storage
from django.contrib import messages #import messages
from payment.models import *
from decimal import *
from .models import *
from datetime import datetime, timedelta
from json import dumps

from django.urls import reverse

import socket
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import geoip2.database

def get_country_from_ip(ip_address):
    # replace 'GeoLite2-Country.mmdb' with the path to your own MaxMind database file
    reader = geoip2.database.Reader('/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/myproject/GeoLite2/GeoLite2-City.mmdb')

    try:
        response = reader.city(ip_address)
        loc = str(response.location.latitude)+","+str(response.location.longitude)
        return [response.country.name, response.country.iso_code, loc]
    except geoip2.errors.AddressNotFoundError:
        # handle error if IP address not found in database
        return ""


@csrf_exempt
def getdatareport(request):
    if request.method == "POST":
         try:
            data = json.loads(request.body)
            try:
               payme = webservice.objects.get(unique_field = data['id'])
               cunt = get_country_from_ip(data['ip'])
               try:
                  payoome = vister_data.objects.get(webservice = payme, ip = data['ip'], rday = datetime.today())

                  payoome.count = payoome.count + 1
                  payoome.online = True
                  payoome.save()

               except vister_data.DoesNotExist:

                  payoome = vister_data.objects.create(webservice = payme,ref = data['ref'],country = cunt[0],cun = cunt[1], ip = data['ip'],location=cunt[2],time=data['visit_time'], online = True)
            except webservice.DoesNotExist:
               pass
            return JsonResponse({'foo':'bar'})
         except json.decoder.JSONDecodeError:
           return JsonResponse({'foo':'bar'})

    return HttpResponse('name')


@csrf_exempt
def newuser(request, id):
   if request.method == "POST":
      try:
         received_json_data = json.loads(request.body)
         credential = received_json_data['credential']
         decoded = jwt.decode(credential, verify=False)
         user_data1 = {
               "name": decoded['name'],
               "email": decoded['email'],
               "given_name": decoded['given_name'],
               "family_name": decoded['family_name'],
               "pic": decoded['picture'],
               "count":1
            }
         try:
            payme = webservice.objects.get(unique_field = id)
            try:
               payoome = user_data.objects.get(webservice = payme)
               fun = True
               for i in payoome.data['data']:
                  if i['email'] == decoded['email']:
                     fun = False
                     i['count'] = i['count']+1
                     payoome.save()
                     break
               if fun == True:
                  payoome.data['data'].append(user_data1)
                  payoome.save()
            except user_data.DoesNotExist:
               payoome = user_data.objects.create(webservice = payme, data={'data':[user_data1]})
         except webservice.DoesNotExist:
            pass
         return JsonResponse({'foo':'bar'})
      except json.decoder.JSONDecodeError:
         return JsonResponse({'foo':'bar'})



@csrf_exempt
def storedata(request, id):
   if request.method == "POST":
      try:
         data = json.loads(request.body)
         try:
            payme = webservice.objects.get(unique_field = id)
            try:
               payoome = store_data.objects.get(webservice = payme)
               payoome.data['data'].append(data)
               payoome.save()
            except store_data.DoesNotExist:
               payoome = store_data.objects.create(webservice = payme, data={'data':[data]})
         except webservice.DoesNotExist:
            pass
         return JsonResponse({'foo':'bar'})
      except json.decoder.JSONDecodeError:
         return JsonResponse({'foo':'bar'})

