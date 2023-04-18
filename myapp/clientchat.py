import asyncio
import datetime
import json
import time
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from promotion.models import *
from asgiref.sync import sync_to_async
from datetime import datetime, timedelta
from .onlinemessage import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync

def remove(id):
    try:
        hk = chat_message.objects.get(websocket_id = id)
        hk.online = False
        hk.save()
    except chat_message.DoesNotExist:
        pass
    try:
        vis = vister_data.objects.get(websocket_id = id, online=True)
        vis.online = False
        vis.save()
    except vister_data.DoesNotExist:
        pass
def chatsetupmain(id, socid):
    web = webservice.objects.get(unique_field = id['id'])
    try:
        cht = vister_data.objects.get(ip = id['ip'], webservice = web, rday = datetime.today())
        cht.websocket_id = socid
        cht.save()
        try:
            hk = chat_message.objects.get(websocket_id = socid)
            hk.online = True
            hk.save()
            if hk.message['data'] != []:
                return hk.message['data']
            else:
                return []
        except chat_message.DoesNotExist:
            return []
    except vister_data.DoesNotExist:
        return [] 

def chatstarted(mas, socid):
    try:
        lko = vister_data.objects.get(websocket_id = socid)
        web = lko.webservice
    except vister_data.DoesNotExist:
        web = webservice.objects.get(unique_field = mas['id'])
    try:
        cht = chat_message.objects.get(email = mas['email'], webservice = web)
        cht.websocket_id = socid
        cht.count = cht.count + 1
        cht.online = True
        cht.save()
        if cht.message['data'] != []:
            return cht.message['data']
        else:
            return []
    except chat_message.DoesNotExist:
        cht = chat_message.objects.create(email = mas['email'],websocket_id = socid,name = mas['name'], webservice = web, online = True,message={"data":[]})
        return []


def clientmessage1(ms, socid):
    print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
    try:
        cht = chat_message.objects.get(websocket_id = socid)
        if ms != "message open":
            cht.message['data'].append(ms)
            cht.openmessage = False
            cht.save()
    except chat_message.DoesNotExist:
        return 'reload'

class ChatSetup(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

        # Register the connection in a dictionary with a unique ID
        self.id = str(id(self))
        onlinechat[self.id] = self

    async def disconnect(self, close_code):
        # Remove the connection from the dictionary when it's closed
        await sync_to_async(remove, thread_sensitive=True)(self.id)
        del onlinechat[self.id]

    async def receive(self, text_data):
        # Receive a message from the client
        message = json.loads(text_data)
        if message['type'] == "chat_setup":
            mess =await sync_to_async(chatsetupmain, thread_sensitive=True)(message['data'], self.id)
            connection = onlinechat.get(self.id)
            if connection:
                if mess != []:
                    await connection.send(text_data=json.dumps({ "type": "update_message","message": mess}))
                else:
                    await connection.send(text_data=json.dumps({ "type": "connection_setup",'message': "Wellcoming meassage from the company"}))
        elif message['type'] == 'chat_started':
            mess = await sync_to_async(chatstarted, thread_sensitive=True)(message['data'], self.id)
            connection = onlinechat.get(self.id)
            if connection:
                if mess != []:
                    await connection.send(text_data=json.dumps({ "type": "update_message","message": mess}))
        elif message['type'] == 'client_message':
            mess = await sync_to_async(clientmessage1, thread_sensitive=True)(message['data'], self.id)
            if mess == 'reload':
                connection = onlinechat.get(self.id)
                if connection:
                    await connection.send(text_data=json.dumps({ "type": "reload",'message': "reload"}))
            
    async def update_client12(self, message,mess ):
        connection = onlinechat.get(mess)
        if connection:
            await connection.send(text_data=json.dumps({ "type": "updateclient_chat","message": message}))  

    async def update_owner132(self, message,mess ):
        connection = connectionsmesage.get(mess)
        if connection:
            await connection.send(text_data=json.dumps({ "type": "updateclient_owner","message": message}))                                                                                        


    async def update_owner(self, message,mess ):
        for m in mess:
            connection = connectionsmesage.get(m)
            if connection:
                await connection.send(text_data=json.dumps({ "type": "listview","message": message}))


@receiver(post_save, sender=chat_message)
def ownerupdate(sender, instance, **kwargs):
    web = instance.webservice
    chat = chat_message.objects.filter(webservice = web)
    if instance.online:
        if instance.openmessage:
            if onlinechat != {}:
                jop={}
                jop['name'] = instance.name
                jop['message'] = instance.message['data'][-1]['message']
                jop['id'] = instance.id
                jop['date'] = str(instance.message['data'][-1]['date'])
                jop['online'] = instance.online
                hop = ChatSetup()
                async_to_sync(hop.update_client12)(jop,instance.websocket_id)

        else:
            if connectionsmesage != {}:
                hop = ChatSetup()
                try:
                    chtqw = message_setup.objects.get(chat_message = instance, online = True)
                    jop={}
                    jop['name'] = instance.name
                    jop['message'] = instance.message['data']#[-1]['message']
                    jop['id'] = instance.id
                    jop['date'] = str(instance.message['data'][-1]['date'])
                    jop['online'] = instance.online
                    hop = ChatSetup()
                    async_to_sync(hop.update_owner132)(jop,chtqw.websocket_id)
                except message_setup.DoesNotExist:
                    pass

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
                lis1 = []
                for k in lis:
                    #if k.online:
                    lis1.append(k.websocket_id)
                async_to_sync(hop.update_owner)(messsa,lis1)
    

onlinechat = {}
