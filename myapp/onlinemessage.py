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


def get_onlmesage(id):
    web = webservice.objects.get(id = id)
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
    lis = message_setup.objects.filter(webservice = web)
    return [messsa, lis]
    

async def send_message(chid):
    if connectionsmesage != {}:
        mess = await sync_to_async(get_onlmesage, thread_sensitive=True)(chid)
        for m in mess[1]:
            connection = connectionsmesage.get(m.websocket_id)
            if connection:
                await connection.send(text_data=json.dumps({ "type": "listview","message": messsa[0]}))



def remove13(id):
    try:
        vis = message_setup.objects.get(websocket_id = id)
        vis.delete()
    except message_setup.DoesNotExist:
        pass



def messagemain(id, socid):
    web = webservice.objects.get(unique_field = id['id'])
    try:
        cht = message_setup.objects.get(webservice = web)
        cht.websocket_id = socid
        cht.online = True
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
    print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    print(ms['id'])
    try:
        cht = chat_message.objects.get(id = ms['id'])
        print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
        if ms != "message open":
            cht.message['data'].append(ms['message'])
            cht.newmes = True
            cht.openmessage = True
            cht.save()
    except chat_message.DoesNotExist:
        print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
        return 'reload'

def getsinglemass(id):
    try:
        cht = chat_message.objects.get(id = id)
        cht.newmes = True
        cht.write = True
        cht.save()

        try:
            cht1 = message_setup.objects.get(webservice = cht.webservice, online = True)
            cht1.chat_message = cht
            cht1.save()
        except message_setup.DoesNotExist:
            pass


        return {'id':id,'name':cht.name, 'date':str(cht.rday), 'online':cht.online, 'message': cht.message['data']}
    except chat_message.DoesNotExist:
        return 'reload'

class MessageBot(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.id = str(id(self))
        connectionsmesage[self.id] = self

    async def disconnect(self, close_code):
        await sync_to_async(remove13, thread_sensitive=True)(self.id)
        del connectionsmesage[self.id]

    async def receive(self, text_data):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
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

        elif message['type'] == 'open_chat':
            mess = await sync_to_async(getsinglemass, thread_sensitive=True)(message['data'])
            connection = connectionsmesage.get(self.id)
            if connection:
                await connection.send(text_data=json.dumps({ "type": "display_chat",'message': mess}))

        elif message['type'] == 'owner_message':
            print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
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