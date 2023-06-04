from channels.generic.websocket import WebsocketConsumer
import random
import json
import uuid

from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.user_id = str(uuid.uuid4())

    def connect(self):
        
        self.user_id = str(uuid.uuid4())
        self.room_group_name ='test'

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()

        self.send(json.dumps({
            'type':'user_id',
            'user_id':self.user_id
        }))


    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        
        print(f"User ID: {self.user_id}")
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':'chat_message',
                'message':message,
                'sender': sender
            }
        )
        # Handle received WebSocket 
    
    def chat_message(self,event):
        message = event['message']
        sender = event['sender']
        print(f"Sender:{sender}")
        print(event)

        self.send(text_data=json.dumps({'type':'chat',
        'message':message,
        'sender': sender
        }))

    async def send_message(self, event):
        # Send WebSocket message to the connected client(s)
        pass
