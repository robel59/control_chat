from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.http import HttpResponse
from .models import *
from webuser.models import *
from .deploy import *
from .post import *
from .sundomian import *
import json
import jwt
from django.core.files.storage import FileSystemStorage
import os
from PIL import Image
from .sundomian import *
import shutil
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.storage import default_storage
from django.contrib import messages #import messages
from payment.models import *
from decimal import *
from promotion.models import *
from datetime import datetime, timedelta
from json import dumps

from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse

import socket
import os
import shutil
import subprocess
import threading
import yaml
import docker

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import geoip2.database

def get_country_from_ip(ip_address):
    # replace 'GeoLite2-Country.mmdb' with the path to your own MaxMind database file
    reader = geoip2.database.Reader('/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/GeoLite2/GeoLite2-Country.mmdb')

    try:
        response = reader.country(ip_address)
        return [response.country.name, response.country.iso_code]
    except geoip2.errors.AddressNotFoundError:
        # handle error if IP address not found in database
        return ""
'''
messages.debug(request, '%s SQL statements were executed.' % count)
messages.info(request, 'Three credits remain in your account.')
messages.success(request, 'Profile details updated.')
messages.warning(request, 'Your account expires in three days.')
messages.error(request, 'Document deleted.')
'''

# Create your views here.
def home(request):
   return render(request,'home/test.html')


def vie(request):
   if request.method == "GET":
      context = {}
      context["web"] = web_templates.objects.all()
      return render(request,'view.html', context)
   
   if request.method == "POST":
      context = {}
      name= request.POST['name']
      id= request.POST['id']
      web = web_templates.objects.get(id = int(id))
      ser = webservice.objects.create(name = name, web_templates = web)

      return redirect('website:webeditpage',ser.id)

def registernew(request):
   if request.method == "POST":
      name= request.POST['name']
      if webservice.objects.filter(name = name).exists():
         messages.error(request, 'Project name alredy taken')
         return redirect('main:home')
      else:
         return redirect('website:selectweb_type',name)

@csrf_exempt
def getdatareport(request):
   if request.method == "POST":
      try:
         data = json.loads(request.body)
         print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGgg ")
         print(data)
         try:
            payme = webservice.objects.get(unique_field = data['id'])
            cunt = get_country_from_ip(data['ip'])
            print(cunt)
            payoome = vister_data.objects.create(webservice = payme,ref = data['ref'],country = cunt[0],cun = cunt[1], ip = data['ip'],location=data['location'],time=data['visit_time'])
         except webservice.DoesNotExist:
            pass
         return JsonResponse({'foo':'bar'})
      except json.decoder.JSONDecodeError:
         print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGgg ")
         return JsonResponse({'foo':'bar'})


@csrf_exempt
def newuser(request, id):
   if request.method == "POST":
      try:
         received_json_data = json.loads(request.body)
         print("SSSSSSSSSSSSSSSSSSSSSSSs ")
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
         print(decoded['name'])  
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
         return HttpResponse(content=decoded['name'])
      except json.decoder.JSONDecodeError:
         print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGgg ")
         return JsonResponse({'foo':'bar'})



@csrf_exempt
def storedata(request, id):
   if request.method == "POST":
      try:
         data = json.loads(request.body)
         print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGgg ")
         print(data)
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
         print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGgg ")
         return JsonResponse({'foo':'bar'})



def selectweb_type(request,name):
   if request.method == "GET":
      context = {}
      context["temp"] = temp_type.objects.all()
      context['name'] = name
      return render(request,'home/selecttype.html', context)

   if request.method == "POST":
      context = {}
      id= request.POST['id']
      return redirect('website:selecttemplate',name, int(id))

def selecttemplate(request, name, type1):
   if request.method == "GET":
      context = {}
      klop = temp_type.objects.get(id = int(type1))
      web = web_templates.objects.all()
      web1 = []
      for i in web:
         if klop in i.temp_type.all():
            web1.append(i)
      context["web"] = web1
      context['name'] = name
      return render(request,'home/templatelist.html', context)

def remove_server_setup(project_name):
    project_dir = r'/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/'+project_name
    client = docker.from_env()
    cmd = f'docker-compose -p {project_name} -f {project_dir}/docker-compose.yml down'

    # run the command in a container
    container = client.containers.run(
        'docker/compose:latest',
        command=cmd,
        remove=True,
        volumes={
            '/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'},
            f'{project_dir}': {'bind': '/app', 'mode': 'rw'}
        },
        detach=True
    )

    return True


def view_template(request, name, tmid):
   if request.method == "GET":
      context = {}
      web = web_templates.objects.get(id = int(tmid))
      context["web"] = web
      context["def"] = payment_type.objects.all()[0]
      context["type"] = payment_type.objects.all()[1:]
      context["service"] = template_type.objects.filter(web_templates = web)
      return render(request,'home/template-gital.html', context)

   if request.method == "POST":
      context = {}
      id= request.POST['payme']
      tpid= request.POST['tpid']
      temp = template_type.objects.get(id = int(tpid))
      ptyp = payment_type.objects.get(id = id)
      amount1 = float(temp.price) * float(ptyp.nodays) / 30

      try:
         ser = webservice.objects.get(client = request.user, name = name)
         if ser.active_pay == False or ser.active:
            if ser.template_type == temp:

               try:
                  payme = service_payment.objects.get(webservice = ser)
                  payme.payment_type = ptyp
                  payme.save()
               except service_payment.DoesNotExist:
                  payme = service_payment.objects.create(payment_type = ptyp, webservice = ser,amount = float(amount1))

            else:
               parent_dir = "/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/"
               pathname = parent_dir+str(ser.name)
               #remove all folder
               port = ser.port
               por = remove_server_setup(ser.name)
               if por:
                  try:
                     shutil.rmtree(pathname)
                  except:
                     pass
               ser.delete()
               ser = webservice.objects.create(
                  client = request.user,
                  sbdname = ser.name +".zufan.com",
                  port = port, 
                  name = name,
                  state = True,
                  active = True, 
                  web_templates = temp.web_templates,
                  template_type=temp
                  )
               payme = service_payment.objects.create(payment_type = ptyp, webservice = ser,amount = float(amount1))
         else:
            return redirect('website:payment', ser.id)
      except webservice.DoesNotExist:
         ser = webservice.objects.create(client = request.user, name = name, web_templates = temp.web_templates,template_type=temp)
         payme = service_payment.objects.create(payment_type = ptyp, webservice = ser,amount = float(amount1))

         #start the server
         por = setupserver(ser.name)
         #set up subdomain for the project
         ser.port = por
         
         hop = createsubdomain(ser.name, por)
      
         if hop:
            print("subdomian created")
            ser.sbdname = ser.name +".zufan.com"
         else:
            #need a way to recored all problem occered on the system
            print("subdomian not created")

         ser.state = True
         ser.active = True
         ser.save()

            
         
      return redirect('website:dataentrypage_main', ser.id)

def dataentrypage_main(request, id):
   if request.method == "GET":
      context = {}
      ser = webservice.objects.get(id = id)
      i = webservice_template.objects.filter(webservice = ser)[0]
      
      no = []
      key_list=list(i.Jsonfield.keys())
      table_key=list(i.Jsonfield['table_data'].keys())
      no.append(key_list)
      no.append(i.Jsonfield)
      no.append(i.id)
      no.append(table_key)
      no.append(i.Jsonfield['table_data'])

      
      context['file'] = ser
      context['dettemp'] = i
      context['notif'] = notiffication.objects.filter(client = request.user, active = True)
      context['temp'] = webservice_template.objects.filter(webservice = ser)
      context['data'] = no
      context['fileloc'] = "/media/deployedlist/"+ser.name+"/web"
      context['webid'] = ser.id
      context['host'] = "http://localhost:"+ser.port
      return render(request,"home/test.html",context)


def promotion(request, id):
   if request.method == "GET":
      context = {}
      ser = webservice.objects.get(id = id)
      try:
         dosel = promo_selected.objects.get(webservice = ser)
         i = domainname_list.objects.filter(webservice = ser)
         context['file'] = ser
         context['list'] = i
         context['notif'] = notiffication.objects.filter(client = request.user, active = True)
         context['temp'] = webservice_template.objects.filter(webservice = ser)
         context['found_dname'] = domainname_found_list.objects.filter(webservice = ser)
         context['webid'] = ser.id
         return render(request,"home/promotion.html",context)
      except promo_selected.DoesNotExist:
         i = promo_service.objects.all()
         context['file'] = ser
         context['list'] = i
         context['notif'] = notiffication.objects.filter(client = request.user, active = True)
         context['temp'] = webservice_template.objects.filter(webservice = ser)
         context['found_dname'] = domainname_found_list.objects.filter(webservice = ser)
         context['webid'] = ser.id
         return render(request,"home/promotion.html",context)

   if request.method == "POST":
      ser = webservice.objects.get(id = id)
      name= request.POST['name']
      dolist = domainname_list.objects.create(name=name, webservice = ser)
      return redirect('website:domain_name',id)



def domain_name(request, id):
   if request.method == "GET":
      context = {}
      ser = webservice.objects.get(id = id)
      try:
         dosel = domainname_selected.objects.get(webservice = ser)
         i = domainname_list.objects.filter(webservice = ser)
         context['file'] = ser
         context['list'] = i
         context['notif'] = notiffication.objects.filter(client = request.user, active = True)
         context['temp'] = webservice_template.objects.filter(webservice = ser)
         context['found_dname'] = domainname_found_list.objects.filter(webservice = ser)
         context['webid'] = ser.id
         return render(request,"home/domain_name.html",context)
      except domain_selected.DoesNotExist:
         i = domainname_list.objects.filter(webservice = ser)
         context['file'] = ser
         context['list'] = i
         context['notif'] = notiffication.objects.filter(client = request.user, active = True)
         context['temp'] = webservice_template.objects.filter(webservice = ser)
         context['found_dname'] = domainname_found_list.objects.filter(webservice = ser)
         context['webid'] = ser.id
         return render(request,"home/domain_name.html",context)

   if request.method == "POST":
      ser = webservice.objects.get(id = id)
      name= request.POST['name']
      dolist = domainname_list.objects.create(name=name, webservice = ser)
      return redirect('website:domain_name',id)


def domain_removemain(request, id):
   if request.method == "POST":
      id1= request.POST['id']
      dolist = domainname_list.objects.get(id =id1)
      dolist.delete()
      return redirect('website:domain_name',id)


def domain_selec(request, id):
   if request.method == "POST":
      ser = webservice.objects.get(id = id)
      id1= request.POST['id']
      dolist = domainname_found_list.objects.get(id =id1)
      try:
         dosel = domainname_selected.objects.get(webservice = ser)
         dosel.domainname_found_list = dolist
         dosel.name = dolist.name
         dosel.save()
      except domain_selected.DoesNotExist:
         dosel = domainname_selected.objects.create(webservice = ser, name = dolist.name, domainname_found_list = dolist)
      return redirect('website:domain_name',id)

def edit_pages(request, id):
   if request.method == "GET":
      context = {}
      i = webservice_template.objects.get(id = id)
      ser = i.webservice
      
      no = []
      key_list=list(i.Jsonfield.keys())
      table_key=list(i.Jsonfield['table_data'].keys())
      no.append(key_list)
      no.append(i.Jsonfield)
      no.append(i.id)
      no.append(table_key)
      no.append(i.Jsonfield['table_data'])

      
      context['file'] = ser
      context['dettemp'] = i
      context['notif'] = notiffication.objects.filter(client = request.user, active = True)
      context['temp'] = webservice_template.objects.filter(webservice = ser)
      context['data'] = no
      context['fileloc'] = "/media/deployedlist/"+ser.name+"/web"
      context['webid'] = ser.id
      context['host'] = "http://localhost:"+ser.port
      return render(request,"home/edit_temp.html",context)



def dataentrypage(request, id):
   if request.method == "GET":
      context = {}
      i = webservice_template.objects.get(id = id)
      ser = i.webservice
      no = []
      key_list=list(i.Jsonfield.keys())
      table_key=list(i.Jsonfield['table_data'].keys())
      no.append(key_list)
      no.append(i.Jsonfield)
      no.append(i.id)
      no.append(table_key)
      no.append(i.Jsonfield['table_data'])

      
      context['file'] = ser
      context['dettemp'] = i
      context['notif'] = notiffication.objects.filter(client = request.user, active = True)
      context['temp'] = webservice_template.objects.filter(webservice = ser)
      context['data'] = no
      context['fileloc'] = "/media/deployedlist/"+ser.name+"/web"
      context['webid'] = ser.id
      context['host'] = "http://localhost:"+ser.port
      return render(request,"home/test.html",context)

def update_selected_service(id):
   yup = webservice.objects.get(id = id)
   payment_request_item.objects.filter(webservice = yup).delete()
   
   try:
      sp = service_payment.objects.get(webservice = yup)
      qunt = sp.payment_type.nodays/30
      try:
         pri = payment_request_item.objects.get(webservice = yup,service_payment = sp)
         pri.total = float(yup.template_type.price) * float(qunt)
         pri.name = "Website deployment"
         pri.amount = yup.template_type.price
         pri.qunt = str(qunt) + " Month"
         pri.save()
      except payment_request_item.DoesNotExist:
         pri = payment_request_item.objects.create(webservice = yup, name = "Website deployment",service_payment = sp,total = float(yup.template_type.price) * float(qunt),amount = yup.template_type.price,qunt = str(qunt) + " Month")

      #---------------------------------------------
      # domain name payment 
      dlist = domainname_list.objects.filter(webservice = yup)
      dcost = domainname_cost.objects.all()
      cosy = 0
      if len(dlist) > 0:
         cosy = dcost[0].cost
         try:
            pri = domainname_selected.objects.get(webservice = yup)
         except domainname_selected.DoesNotExist:
            pri = domainname_selected.objects.create(webservice = yup)


         try:
            se = selected_email.objects.get(webservice = yup)
            try:
               prie = payment_request_item.objects.get(webservice = yup,selected_email = se)
               prie.total = float(se.cost) * float(qunt)
               prie.name = "Email service"
               prie.amount = se.cost
               prie.info = se.info
               prie.qunt = str(qunt) + " Month"
               prie.save()
            except payment_request_item.DoesNotExist:
               prie = payment_request_item.objects.create(name = "Email service",info = se.info, webservice = yup,selected_email = se,total = float(se.cost) * float(qunt),amount = se.cost,qunt = str(qunt) + " Month")
         
         except selected_email.DoesNotExist:
            pass
            #se = selected_email.objects.create(webservice = yup,info ="no email addres request")
         try:
            priw = payment_request_item.objects.get(webservice = yup,domainname_selected = pri)
            priw.total = float(cosy)
            priw.name = "Domainame service"
            priw.amount = float(cosy)
            priw.info = pri.info
            priw.qunt = "1 year"
            priw.save()
         except payment_request_item.DoesNotExist:
            pri = payment_request_item.objects.create(name = "Domainame service",info = "for purchase of domain name",webservice = yup,domainname_selected = pri,total = float(cosy),amount = float(cosy),qunt = "1 year")
            
         
      #-----------------------------------------------
      try:
         ps = promo_selected.objects.get(webservice = yup)
         try:
            pri = payment_request_item.objects.get(webservice = yup,promo_selected = ps)
            pri.total = float(ps.cost) * float(qunt)
            pri.name = "Promotion service"
            pri.amount = ps.cost
            pri.info = ps.info
            pri.qunt = str(qunt) + " Month"
            pri.save()
         except payment_request_item.DoesNotExist:
            pri = payment_request_item.objects.create(name = "Promotion service",info = ps.info,webservice = yup,promo_selected = ps,total = float(ps.cost) * float(qunt),amount = ps.cost,qunt = str(qunt) + " Month")
            
      except promo_selected.DoesNotExist:
         pass

   except service_payment.DoesNotExist:
      return redirect('website:dataentrypage_main', yup.id)
#final payment
def payment(request, id):
   if request.method == "GET":
      context = {}
      try:
         yup = webservice.objects.get(id = id)
         if yup.paid:
            return redirect('website:dataentrypage_main', yup.id)
         else:
            if yup.active_pay == False:
               update_selected_service(id)
            eachit = payment_request_item.objects.filter(webservice = yup)
            dis = discount.objects.filter(webservice = yup)
            total = 0
            di = 0
            for io in dis:
               if io.valid and io.eday > io.rday:
                  total = total + io.rate
            for i in eachit:
               total = total + i.total
            dis = float(total) * float(di)
            pai = float(total) - float(dis)
            va = pai * 0.15
            amu = pai + va
            try:
               payme = payment_request.objects.get(webservice = yup, valid = False)
            except payment_request.DoesNotExist:
               payme = payment_request.objects.create(webservice = yup)
            payme.total = total
            payme.amount = amu
            payme.descount = dis
            payme.vat = va
            payme.save() 
            context["payment"] = payme
            context['list'] = eachit
            context['client'] = yup.client
            context['file'] = yup
            context['webid'] = yup.id

            #paypal
            host = request.get_host()
            rate = exchange_rate_usd.objects.all()[0]
            dr = float(total) / float(rate.amount)
            price = round((dr - (dr * 0.05)),2)
            billing_cycle = 1
            billing_cycle_unit = "Y"

            context['dtotal'] = round(dr,2)
            context['descou'] = price

            context['host'] = host
            context['price']=price
            context['billing_cycle']=billing_cycle
            context['billing_cycle_unit']=billing_cycle_unit


            paypal_dict  = {
               "cmd": "_xclick-subscriptions",
               'business': settings.PAYPAL_RECEIVER_EMAIL,
               "a3": price,  # monthly price
               "p3": billing_cycle,  # duration of each unit (depends on unit)
               "t3": billing_cycle_unit,  # duration unit ("M for Month")
               "src": "10",  # make payments recur
               "sra": "5",  # reattempt payment on payment error
               "no_note": "1",  # remove extra notes (optional)
               'item_name': 'Content subscription',
               'custom': payme.id,     # custom data, pass something meaningful here
               'currency_code': 'USD',
               'notify_url': 'http://{}{}'.format(host,
                                                   reverse('paypal-ipn')),
               'return_url': 'http://{}{}'.format(host,
                                                   reverse('payment:payment_done', kwargs={'id':payme.id})),
               'cancel_return': 'http://{}{}'.format(host,
                                                      reverse('payment:payment_cancelled')),
            }

            form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")

            context['form'] = form
            context['paypal_dict'] = paypal_dict


            return render(request,'home/paymetchose.html', context)
      except webservice.DoesNotExist:
         #error page 
         return render(request,'home/templatelist.html', context)

   if request.method == "POST":
      yup = webservice.objects.get(id = id)
      yup.active_pay = True
      yup.save()

      return redirect('website:payment',yup.id)


def setup_promo(request, id):
   yup = webservice.objects.get(id = id)
   if yup.active_pay == False:
      if request.method == "GET":
         context = {}
         ema = promo_selected.objects.filter(webservice = yup)
         context["servis"] = yup
         context['client'] = yup.client
         context['file'] = yup
         context['selec'] = len(ema)
         if len(ema) == 1:
            context['selectid'] = ema[0].promo_type.id
            context['servid'] = ema[0].id
         context['promo'] = promo_type.objects.all()
         return render(request,'home/selectpromo.html', context)
      if request.method == "POST":
         idd= request.POST['id']
         pro = promo_type.objects.get(id = idd)
         try:
            ema = promo_selected.objects.get(webservice = yup)
            ema.promo_type = pro
            ema.cost = pro.cost
            ema.save()
         except promo_selected.DoesNotExist:
            ema = promo_selected.objects.create(promo_type = pro, webservice = yup, cost = pro.cost)
         return redirect('website:setup_promo',yup.id)

   else:
      return redirect('website:payment',yup.id)

def remove_promo(request, id):
   if request.method == "POST":
      id1= request.POST['id']
      yup = webservice.objects.get(id = id)
      dolist = promo_selected.objects.get(id =id1)
      dolist.delete()
      return redirect('website:setup_promo',yup.id)

def select_domain(request, id):
   yup = webservice.objects.get(id = id)
   if yup.active_pay == False:
      if request.method == "GET":
         context = {}
         dolist = domainname_list.objects.filter(webservice = yup)
         emai = selected_email.objects.filter(webservice = yup)
         context["servis"] = yup
         context['dlist'] = dolist
         context['avel'] = len(dolist)
         context['client'] = yup.client
         context['file'] = yup
         context['emailtype'] = email_type.objects.all()
         context['webid'] = yup.id
         context['email'] = emai
         context['email_t'] = len(emai)
         return render(request,'home/domainview.html', context)
      if request.method == "POST":
         name= request.POST['name']
         dolist = domainname_list.objects.create(name=name, webservice = yup)
         return redirect('website:select_domain',yup.id)
   else:
      return redirect('website:payment',yup.id)


def register_email(request, id):
   if request.method == "POST":
      id1= request.POST['etype']
      yup = webservice.objects.get(id = id)
      dolist = email_type.objects.get(id =id1)
      try:
         ema = selected_email.objects.get(webservice = yup)
         ema.email_type = dolist
         ema.cost = dolist.cost
         ema.save()
      except selected_email.DoesNotExist:
         ema = selected_email.objects.create(email_type = dolist, webservice = yup, cost = dolist.cost)
      return redirect('website:select_domain',yup.id)

def remove_email(request, id):
   if request.method == "POST":
      id1= request.POST['id']
      yup = webservice.objects.get(id = id)
      dolist = selected_email.objects.get(id =id1)
      dolist.delete()
      return redirect('website:select_domain',yup.id)


def select_domain_remove(request, id):
   if request.method == "POST":
      id1= request.POST['id']
      yup = webservice.objects.get(id = id)
      dolist = domainname_list.objects.get(id =id1)
      dolist.delete()
      dol = domainname_list.objects.filter(webservice = yup)
      if len(dol) == 0:
         klp = selected_email.objects.filter(webservice = yup)
         klp.delete()
      return redirect('website:select_domain',yup.id)


def cheack(request):
   if request.method == "POST":
      name= request.POST['name']
      if webservice.objects.filter(name = name).exists():
         return HttpResponse('<div id="erroe_view" style="color: red;" class="valid-feedback">Websit name taken </div> ')
      else:
         return HttpResponse('<div id="erroe_view"o class="valid-feedback">Looks good! </div> ')


def update(request, id):
   if request.method == "POST":
      
      hj = webservice_template.objects.get(id = id)
      key_list=list(hj.Jsonfield.keys())

      for i in key_list:
         try:
            name= request.POST[i]
            hj1 = hj.Jsonfield
            hj1[i]['text'] = name
            hj.Jsonfield = hj1
            hj.save()
            return HttpResponse(name)
         except:
            pass

def updatetable(request, id):
   if request.method == "POST":
      
      hj = webservice_template.objects.get(id = id)
      key_list=list(hj.Jsonfield.keys())

      for i in key_list:
         if i[0] == 't':
            try:
               name= request.POST[i]
               hj1 = hj.Jsonfield
               hj1[i]['text'] = name
               hj.Jsonfield = hj1
               hj.save()
               return HttpResponse(name)
            except:
               pass
         else:
            pass
      return redirect('website:dataentrypage',hj.webservice.id)

def updatetable(request, id):
   if request.method == "POST":
      name= request.POST["tablename"]
      hj = webservice_template.objects.get(id = id)
      data = hj.Jsonfield['table_data'][name]["table_order"]
      table = hj.Jsonfield['table_data'][name]["data"]
      idd = hj.Jsonfield['table_data'][name]["cunt"]+1
      store = {}
      store['id'] = idd
      for i in data:
         nko = {}
         if i == "img":
            fs = FileSystemStorage()
            newpath = r'/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/'+str(hj.webservice.name)+'/web/'
            try:
               myfile = request.FILES[i]
               print(myfile)
               storlocation = newpath + "newimage"
               if not os.path.exists(storlocation):
                  os.makedirs(storlocation)
               opy = myfile.name
               zxc = os.path.splitext(opy)
               if zxc[1] == '.png':
                  nko['text'] = "newimage/" + zxc[0]+str(idd)+zxc[1]
                  kop1 = storlocation+"/" + zxc[0]+str(idd)+zxc[1]
               elif zxc[1] == '.jpg':
                  nko['text'] = "newimage/" + zxc[0]+str(idd)+zxc[1]
                  kop1 = storlocation +"/" + zxc[0]+str(idd)+zxc[1]
               elif zxc[1] == '.jpeg':
                  nko['text'] = "newimage/" + zxc[0]+str(idd)+zxc[1]
                  kop1 = storlocation + "/" + zxc[0]+str(idd)+zxc[1]
               store['img'] = nko

               #width = 279 # size.split('*')[0]
               #hight = 235 #size.split('*')[1]
               fs.save(kop1, myfile)
               #size = ( width, hight)
               #in_memory_image = Image.open(kop1, 'r')
               #image45 = in_memory_image.resize(size, Image.ANTIALIAS)
               #image45.save(kop)     
            except:
               pass
         else:
            nam= request.POST[i]
            nko['text'] = nam
            store[i] = nko
      
      table.append(store)
      hj.Jsonfield['table_data'][name]["data"] = table
      hj.Jsonfield['table_data'][name]["cunt"] = idd
      hj.save()

      return redirect('website:dataentrypage',hj.id)


def removtable(request, id):
   if request.method == "POST":
      name= request.POST["tablename"]
      tid= request.POST["tableid"]
      hj = webservice_template.objects.get(id = id)
      data = hj.Jsonfield['table_data'][name]["data"]
      store = []
      for i in data:
         if i['id'] != int(tid):
            store.append(i)
      hj.Jsonfield['table_data'][name]["data"] = store
      hj.save()

      return redirect('website:dataentrypage',hj.id)

def resat(request, id):
   if request.method == "POST":
      web = webservice.objects.get(id = id)
      web_data = webservice_template.objects.filter(webservice = web)
      web_data.delete()
      newpath = r'/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/'+str(web.name)+'/web'  
    
      shutil.rmtree(newpath, ignore_errors=True)
      print("GGGGGGGGGGGGGGGGGGGGGGG")
      newpath = newpath + "/"
      with zipfile.ZipFile(web.deploy, 'r') as zip_ref:
         zip_ref.extractall(newpath)
      
      temp = template_name.objects.filter(web_templates = web.web_templates)
      for i in temp:
         with open(newpath + i.json_name) as file:
               data = json.load(file)
         webservice_template.objects.create(template_name = i, webservice = web, Jsonfield = data, name = i.json_name)
      stopproject(web.name)
      restart(web.name)

      return redirect('website:webeditpage',web.id)


def imupdate(request, id):
   if request.method == "POST":
      fs = FileSystemStorage()
      hj = webservice_template.objects.get(id = id)
      key_list=list(hj.Jsonfield.keys())
      newpath = r'/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/'+str(hj.webservice.name)+'/web/'
     

      for i in key_list:
         if i[0] == "i":
            print(i)
            try:
               myfile = request.FILES[i]
               kop = newpath + hj.Jsonfield[i]['text']
               dire = os.path.dirname(hj.Jsonfield[i]['text'])
               print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSssssss")
               print(kop)
               print(dire)
               opy = myfile.name
               newname = dire + "/"+opy
               if os.path.splitext(opy)[1] == '.png':
                  kop1 = newpath + newname#hj.Jsonfield[i]['text']
               elif os.path.splitext(opy)[1] == '.jpg':
                  kop1 = newpath + newname#hj.Jsonfield[i]['text']
               elif os.path.splitext(opy)[1] == '.jpeg':
                  kop1 = newpath + newname#hj.Jsonfield[i]['text']

               print(opy)
               print(newname)
               hj.Jsonfield[i]['text'] = newname
               hj.save()
               #size = newpath + hj.Jsonfield[i]['size']
               width = 279 # size.split('*')[0]
               hight = 235 #size.split('*')[1]
               try:
                  os.remove(kop)
               except:
                  pass
               fs.save(kop1, myfile)
               
               size = ( width, hight)
               in_memory_image = Image.open(kop1, 'r')
               image45 = in_memory_image.resize(Image.ANTIALIAS)
               image45.save(kop)
            
               
            except:
               pass
         else:
            pass

      return redirect('website:dataentrypage',hj.id)


def upload_first1(request, id):
   if request.method == "POST":
      hj = webservice_template.objects.get(id = id)
      newpath = r'/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/'+str(hj.webservice.name)+'/web/'+str(hj.name)

      jsonFile = open(newpath, "w")
      jsonFile.write(json.dumps(hj.Jsonfield))
      jsonFile.close()


      por = restart(hj.name)
  
      return redirect('website:edit_pages',hj.id)



def upload_first(request, id):
   if request.method == "POST":
      hj = webservice_template.objects.get(id = id)
      newpath = r'/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/'+str(hj.webservice.name)+'/web/'+str(hj.name)

      jsonFile = open(newpath, "w")
      jsonFile.write(json.dumps(hj.Jsonfield))
      jsonFile.close()


      por = restart(hj.name)
  
      return redirect('website:dataentrypage',hj.id)


def upload(request, id):
   if request.method == "POST":
      hj = webservice_template.objects.get(id = id)
      newpath = r'/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/'+str(hj.webservice.name)+'/web/'+str(hj.name)

      jsonFile = open(newpath, "w")
      jsonFile.write(json.dumps(hj.Jsonfield))
      jsonFile.close()
      
  
      return redirect('website:template_edit',hj.id)


def stop(request, id):
   if request.method == "POST":
      hj = webservice.objects.get(id = id)
      por = stopproject(hj.name)
      return redirect('website:webeditpage',hj.id)


def restart1(request, id):
   if request.method == "POST":
      hj = webservice.objects.get(id = id)
      por = restart(hj.name)
      return redirect('website:webeditpage',hj.id)


def reload1(request, id):
   if request.method == "POST":
      hj = webservice.objects.get(id = id)
      por = reload(hj.name)
      return redirect('website:webeditpage',hj.id)


@register.filter
def get_value(dictionary, key):
   return dictionary.get(key)


def billing(request,id):
   if request.method == "GET":
      
      context = {}
      ser = webservice.objects.get(id = id)
      context['payment'] = payment.objects.get(webservice = ser)
      context['payed'] = payment_confermation.objects.filter(webservice = ser)
      context['add'] = selected_add.objects.filter(webservice = ser)
      context['payed_add'] = add_payment_confermation.objects.filter(webservice = ser)
      context['file'] = ser
      context['webid'] = ser.id
      return render(request,"home/billing.html",context)


def livereport(request,id):
   if request.method == "GET":
      context = {}
      i = webservice.objects.get(id = id)
      context['file'] = i
      context['webid'] = id
      return render(request,"home/livereport.html",context)


def template_edit(request,id):
   if request.method == "GET":
      
      context = {}
      i = webservice_template.objects.get(id = id)
      ser = i.webservice
      no = []
      key_list=list(i.Jsonfield.keys())
      table_key=list(i.Jsonfield['table_data'].keys())
      no.append(key_list)
      no.append(i.Jsonfield)
      no.append(i.id)
      no.append(table_key)
      no.append(i.Jsonfield['table_data'])

      
      context['file'] = ser
      context['dettemp'] = i
      context['notif'] = notiffication.objects.filter(client = request.user, active = True)
      context['temp'] = webservice_template.objects.filter(webservice = ser)
      context['data'] = no
      context['fileloc'] = "/media/deployedlist/"+ser.name+"/web"
      context['webid'] = ser.id
      return render(request,"home/edittem.html",context)


def webeditpage(request,mid):
   if request.method == "GET":
      ser = webservice.objects.get(id = mid)
      if ser.paid == True:
         context = {}
         lid = []
         hj = webservice_template.objects.filter(webservice = ser)
         for i in hj:

            no = []
            key_list=list(i.Jsonfield.keys())
            table_key=list(i.Jsonfield['table_data'].keys())
            no.append(key_list)
            no.append(i.Jsonfield)
            no.append(i.id)
            no.append(table_key)
            no.append(i.Jsonfield['table_data'])
            lid.append(no)
         context['file'] = ser
         context['notif'] = notiffication.objects.filter(client = request.user, active = True)
         context['temp'] = webservice_template.objects.filter(webservice = ser)
         context['data'] = lid
         context['fileloc'] = "/media/deployedlist/"+ser.name+"/web"
         context['webid'] = mid
         
         da = daily_data.objects.filter(webservice = ser)[:7]
         date1 = []
         valu = []
         sumsev = 0
         cunt = 0
         for i in da:
            cunt = cunt+1
            print(i.rday)
            print(i.count)
            date1.append(i.rday)
            valu.append(i.count)
            sumsev = sumsev + i.count

         last_week = datetime.today() - timedelta(days=7)
         vs = vister_data.objects.filter(webservice = ser, rday__gte=last_week)
         cunt4 = []
         cunt1 = []
         ref = []
         ref1 = []
         sum = 0
         for v in vs:
            sum = sum + 1
            if v.country in cunt4:
               for u in cunt1:
                  if u[0] == v.cun:
                     u[1] = u[1] + 1
            else:
               cunt4.append(v.country)
               cunt1.append([v.cun,1])
            if v.ref in ref:
               for u in ref1:
                  if u[0] == v.ref:
                     u[1] = u[1] + 1
            else:
               ref.append(v.ref)
               ref1.append([v.ref,1])
         for u in ref1:
            u.append(round(u[1]*100/sumsev,2))
         for u in cunt1:
            u.append(round(u[1]*100/sumsev,2))

         context['country'] = cunt1
         context['refferal'] = ref1
         try:
            context['email'] = user_data.objects.get(webservice = ser).data['data']
         except user_data.DoesNotExist:
            context['email'] = []
         dai =da[cunt-1].count
         dai1 =da[cunt-2].count
         if dai > dai1:
            per =round(dai*100/(dai1+dai),2)
            context['day'] = dai
            context['daprog'] = per
            context['prog'] = True
         else:
            per = round(dai1*100/(dai1+dai),2)
            context['day'] = dai
            context['daprog'] = per
            context['prog'] = False
         context['svendaytotal'] = sumsev
         dataDictionary = {
            'hello': date1,
            'geeks':  valu
         }
         context['data'] =dataDictionary
         return render(request,"home/dashboard.html",context)

      else:
          return redirect('website:payment', ser.id )

   if request.method == "POST":
      ser = webservice.objects.get(id = mid)
      #start the server
      por = setupserver(ser.name)
      #set up subdomain for the project
      ser.port = por
      
      hop = createsubdomain(ser.name, por)
     
      if hop:
         print("subdomian created")
         ser.sbdname = ser.name +".zufan.com"
      else:
         #need a way to recored all problem occered on the system
         print("subdomian not created")

      

      ser.state = True
      ser.active = True
      ser.save()

      #stopproject(ser.name)
      #restart(ser.name)
      #reload(ser.name)
      return redirect('website:webeditpage',mid)

def offerlist(request,mid):
   web = web_templates.objects.get(id = int(mid))
   parent_dir = "/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/"
   pat = parent_dir+str(mid)+"/index.html"
   return render(request,pat,{"i":web})


def offerlist_in(request,mid,temp):
   web = web_templates.objects.get(id = int(mid))
   parent_dir = "/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/"
   pat = parent_dir+str(mid)+"/"+temp
   return render(request,pat,{"ikl":web})