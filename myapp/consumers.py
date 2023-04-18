import asyncio
import datetime
import json
import time
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from promotion.models import *
from asgiref.sync import sync_to_async
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


def remove(id):
    try:
        vis = connection_setup.objects.get(websocket_id = id)
        vis.online = False
        vis.save()
    except connection_setup.DoesNotExist:
        pass

def my_sync_function(id,id1):
    web = webservice.objects.get(id = int(id))
    try:
        vis = connection_setup.objects.get(webservice = web)
        vis.websocket_id = id1
        vis.online = True
        vis.save()
    except connection_setup.DoesNotExist:
        vis = connection_setup.objects.create(webservice = web,websocket_id = id1,online = True)

    mes = vister_data.objects.filter(webservice = web, online = True, rday = datetime.today())
    me = []
    lock = []
    for i in mes:
        geto = False
        if len(me)>0:
            if i.location in lock:
                for k in me:
                    loc = i.location.split(",")
                    if k['location'][0] == float(loc[0]) and k['location'][1] == float(loc[1]):
                        k['size'] = k['size'] + 0.01
                        break
            else:
                loc = i.location.split(",")
                lock.append(i.location)
                hop = {}
                hop["location"] = [float(loc[0]),float(loc[1])]
                hop["size"] = 0.05
                me.append(hop)
        else:
            loc = i.location.split(",")
            hop = {}
            hop["location"] = [float(loc[0]),float(loc[1])]
            hop["size"] = 0.05
            me.append(hop)
    context={}
    da1 = daily_data.objects.filter(webservice = web, rday = datetime.today()-timedelta(days=1))
    if len(da1)>0: 
        da1count = da1[0].count
    else:
        da1count = 0

    try:
        da = daily_data.objects.get(webservice = web, rday = datetime.today())
        context['today_vister'] = da.count
        context['yester_vister'] = da1count
        context['polte_chart'] = da.time_stamp['data'][-1]
    except daily_data.DoesNotExist:
        context['today_vister'] = 0
        context['polte_chart'] = [0,0]
        context['yester_vister'] = da1count
   
   
    context['onlinenow'] = len(mes)
    context["map"] = me
    return str(context)



class TimeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

        # Register the connection in a dictionary with a unique ID
        self.id = str(id(self))
        connections[self.id] = self

    async def disconnect(self, close_code):
        # Remove the connection from the dictionary when it's closed
        await sync_to_async(remove, thread_sensitive=True)(self.id)
        del connections[self.id]

    async def receive(self, text_data):
        # Receive a message from the client
        message = json.loads(text_data)
        message = await sync_to_async(my_sync_function, thread_sensitive=True)(message['data'], self.id)
        # Send the message to a specific connection based on its ID
        connection = connections.get(self.id)
        if connection:
            await connection.send(text_data=json.dumps({ "type": "websocket.send",'message': message}))

    async def update123(self, message,id ):
        # When the "mymodel_update" event is received, send a message to the WebSocket
        connection = connections.get(id)
        if connection:
            await connection.send(text_data=json.dumps({ "type": "websocket.send",'message': message}))


connections = {}


def update_data(id):
    web1 = connection_setup.objects.get(id = int(id))
    web = web1.webservice
    mes = vister_data.objects.filter(webservice = web1.webservice, online = True, rday = datetime.today())
    me = []
    lock = []
    for i in mes:
        geto = False
        if len(me)>0:
            if i.location in lock:
                for k in me:
                    loc = i.location.split(",")
                    if k['location'][0] == float(loc[0]) and k['location'][1] == float(loc[1]):
                        k['size'] = k['size'] + 0.01
                        break
            else:
                loc = i.location.split(",")
                lock.append(i.location)
                hop = {}
                hop["location"] = [float(loc[0]),float(loc[1])]
                hop["size"] = 0.05
                me.append(hop)
        else:
            loc = i.location.split(",")
            hop = {}
            hop["location"] = [float(loc[0]),float(loc[1])]
            hop["size"] = 0.05
            me.append(hop)
    context={}
    da1 = daily_data.objects.filter(webservice = web, rday = datetime.today()-timedelta(days=1))
    if len(da1)>0: 
        da1count = da1[0].count
    else:
        da1count = 0

    try:
        da = daily_data.objects.get(webservice = web, rday = datetime.today())
        context['today_vister'] = da.count
        context['yester_vister'] = da1count
        context['polte_chart'] = da.time_stamp['data'][-1]
    except daily_data.DoesNotExist:
        context['today_vister'] = 0
        context['polte_chart'] = [0,0]
        context['yester_vister'] = da1count
    context['onlinenow'] = len(mes)
    context["map"] = me

    hop = TimeConsumer()
    async_to_sync(hop.update123)(str(context),web1.websocket_id)



@receiver(post_save, sender=connection_setup)
def my_model_updated(sender, instance, **kwargs):
    update_data(instance.id)
     
