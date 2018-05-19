from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Room
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            self.room_name = Room.objects.get(
                label=self.scope['url_route']['kwargs']['label'])
            self.room_group_name = 'chat_{}'.format(self.room_name)
            
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        except: 
            print('Deu Ruim na conexão')
            return

    async def disconnect(self, close_code):
        try:
            Room.objects.get(label=self.room_name)
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except:
            pass

    # Receive message from websocket
    async def receive(self, text_data):
        try:
            room = Room.objects.get(label=self.room_name)
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            m = room.messages.create(user=self.scope['user'], message=message)
           
        except:
            return


        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': json.dumps(m.as_dict())
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # send message to websocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
