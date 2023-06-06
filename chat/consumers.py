from channels.generic.websocket import WebsocketConsumer
import random
import json
import uuid

from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(WebsocketConsumer):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.user_id = str(uuid.uuid4())

    def connect(self):

        self.accept()
        self.user_id = str(uuid.uuid4())
        self.room_group_name ='test'

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.send(json.dumps({
            'type':'user_id',
            'user_id':self.user_id
        }))
        # self.send(json.dumps({
        #     'type': 'initial_data',
        #     'data': user_key
        # }))


    # def disconnect(self, close_code):
        # pass

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        senderId = text_data_json['senderId']
        time = text_data_json['time']

        # received_data = json.loads(text_data)
        # user_key = received_data.get('userKey')
        
        # print(f"User ID: {self.user_id}")
        # print(f"User Key: {sender}")
        # print(message)
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':'chat_message',
                'message':message,
                'sender': sender,
                'senderId':senderId,
                'time':time
            }
        )
        # Handle received WebSocket 
    
    def chat_message(self,event):
        message = event['message']
        sender = event['sender']
        senderId = event['senderId']
        time = event['time']
        # print(f"Sender:{sender}")
        print(time)

        self.send(text_data=json.dumps({'type':'chat',
        'message':message,
        'sender': sender,
        "senderId":senderId,
        "time":time
        }))

    async def send_message(self, event):
        # Send WebSocket message to the connected client(s)
        pass
