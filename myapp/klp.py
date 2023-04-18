import asyncio
import datetime
import json
import time
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from promotion.models import *
from asgiref.sync import sync_to_async
from datetime import datetime, timedelta
from .consumers import *
from django.db.models.signals import post_save
from django.dispatch import receiver

async def send_message(chid):
    web = webservice.objects.get(id = chid)
    chat = message_setup.objects.filter(webservice = web, online = True)
    messsa = []
    for i in chat:
        if [] != i.message['data']:
            jop={}
            jop['name'] = i.name
            jop['message'] = i.message['data'][-1]['message']
            jop['id'] = i.id
            jop['date'] = str(i.message['data'][-1]['date'])
            jop['online'] = i.online
            messsa.append(jop)
    for m in chat:
        connection = connectionsmesage.get(m.websocket_id)
        if connection:
            await connection.send(text_data=json.dumps({ "type": "listview","message": messsa}))



def remove(id):
    try:
        vis = message_setup.objects.get(websocket_id = id)
        vis.online = False
        vis.save()
    except message_setup.DoesNotExist:
        pass



def messagemain(id, socid):
    web = webservice.objects.get(unique_field = id['id'])
    try:
        cht = message_setup.objects.get(webservice = web, online = False)
        cht.websocket_id = socid
        cht.save()
    except message_setup.DoesNotExist:
        cht = message_setup.objects.create(webservice = web,websocket_id = socid, online = True)

    chat = chat_message.objects.filter(webservice = web)
    messsa = []
    for i in chat:
        if [] != i.message['data']:
            jop={}
            jop['name'] = i.name
            jop['message'] = i.message['data'][-1]['message']
            jop['id'] = i.id
            jop['date'] = str(i.message['data'][-1]['date'])
            jop['online'] = i.online
            messsa.append(jop)

    return messsa

def chatstarted(mas, socid):
    lko = vister_data.objects.get(websocket_id = socid)
    web = lko.webservice
    try:
        cht = chat_message.objects.get(email = mas['email'], webservice = web)
        cht.websocket_id = socid
        cht.count = cht.count + 1
        cht.save()
        if cht.message['data'] != []:
            return cht.message['data']
        else:
            return []
    except chat_message.DoesNotExist:
        cht = chat_message.objects.create(email = mas['email'],websocket_id = socid,name = mas['name'], webservice = web, online = True,message={"data":[]})
        return []


def clientmessage(ms, socid):
    try:
        cht = chat_message.objects.get(websocket_id = socid)
        if ms != "message open":
            cht.message['data'].append(ms)
            cht.save()
    except chat_message.DoesNotExist:
        return 'reload'

class MessageBot(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.id = str(id(self))
        connection = connectionsmesage.get(self.id)
        if connection == False:
            connectionsmesage[self.id] = self

    async def disconnect(self, close_code):
        await sync_to_async(remove, thread_sensitive=True)(self.id)
        del connectionsmesage[self.id]

    async def receive(self, text_data):
        # Receive a message from the client
        message = json.loads(text_data)
        if message['type'] == "message_setup":
            mess =await sync_to_async(messagemain, thread_sensitive=True)(message['data'], self.id)
            connection = connectionsmesage.get(self.id)
            if connection:
                if mess != []:
                    await connection.send(text_data=json.dumps({ "type": "listview","message": mess}))
                else:
                    await connection.send(text_data=json.dumps({ "type": "message_setup",'message': "Wellcoming meassage from the company"}))
        elif message['type'] == 'chat_started':
            mess = await sync_to_async(chatstarted, thread_sensitive=True)(message['data'], self.id)
            connection = connectionsmesage.get(self.id)
            if connection:
                if mess != []:
                    await connection.send(text_data=json.dumps({ "type": "update_message","message": mess}))
        elif message['type'] == 'client_message':
            mess = await sync_to_async(clientmessage, thread_sensitive=True)(message['data'], self.id)
            if mess == 'reload':
                connection = connectionsmesage.get(self.id)
                if connection:
                    await connection.send(text_data=json.dumps({ "type": "reload",'message': "reload"}))


    async def update123(self, message,id ):

        connection = connectionsmesage.get(id)
        if connection:
            await connection.send(text_data=json.dumps({ "type": "websocket.send",'message': message}))

connectionsmesage = {}